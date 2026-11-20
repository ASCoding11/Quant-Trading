"""Satellite SO2 over critical-raw-material plants: Sentinel-5P TROPOMI.

Copper and nickel smelters roast sulphide ore and vent sulphur dioxide; Norilsk is the largest
single SO2 source on Earth, and smelter output shows up as an SO2 plume that TROPOMI (on
Sentinel-5P, 5.5 x 3.5 km pixels, daily global coverage since May 2018) measures directly - unlike
MODIS fire pixels, which only see the hottest plants (``qtrade.data.satellite``).

Source: the ``sentinel-5p-l2-netcdf`` collection on Microsoft's Planetary Computer (no key, readable
from a GitHub runner). Each item is one orbit (OFFL / RPRO, about 4,000 x 450 pixels) or a 5-minute
near-real-time slice of one (NRTI). Only a few variables of each NetCDF file are read, over HTTP range
requests: latitude, longitude, ``qa_value`` and the SO2 column for a 1 km plume
(``sulfurdioxide_total_vertical_column_1km``, the product for low-altitude industrial sources).

Per site and overpass: the mean SO2 column (Dobson units) over good pixels (qa >= 0.5) within
``radius_km`` of the plant, and over a background ring 60-120 km away; the enhancement is the
difference. One orbit file serves every site under it. ESA Copernicus data: free, stored in the clear.
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import time
from multiprocessing.connection import wait as mp_wait
from pathlib import Path

import numpy as np
import pandas as pd

from ..utils import LOG, setup_logging
from .satellite import SITES, Site

STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
SIGN = "https://planetarycomputer.microsoft.com/api/sas/v1/sign"
COLLECTION = "sentinel-5p-l2-netcdf"
FIRST_DAY = "2018-05-01"
RADIUS_KM = 25.0                 # plume window (TROPOMI pixels are ~5 km)
RING_KM = (60.0, 120.0)          # background ring
MOL_M2_TO_DU = 2241.15
FILL = 1e10                      # anything larger is a fill value
VAR = "PRODUCT/SUPPORT_DATA/DETAILED_RESULTS/sulfurdioxide_total_vertical_column_1km"
MODE_RANK = {"RPRO": 0, "OFFL": 1, "NRTI": 2}
COLS = ["date", "time", "site", "commodity", "orbit", "mode", "n_plume", "n_ring", "so2_plume_du", "so2_ring_du",
        "so2_enh_du"]


def _session():
    import requests

    s = requests.Session()
    s.headers["User-Agent"] = "qtrade-satellite (research)"
    return s


def search_items(s, site: Site, start: str, end: str) -> list[dict]:
    """Every SO2 item whose footprint contains the site, between the dates (all processing modes)."""
    body = {"collections": [COLLECTION], "intersects": {"type": "Point", "coordinates": [site.lon, site.lat]},
            "datetime": f"{start}/{end}", "limit": 500, "query": {"s5p:product_name": {"eq": "so2"}}}
    out, url = [], f"{STAC}/search"
    for _ in range(200):
        for attempt in range(4):
            try:
                r = s.post(url, json=body, timeout=120)
                r.raise_for_status()
                break
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(5 * (attempt + 1))
        page = r.json()
        out += page.get("features", [])
        nxt = next((ln for ln in page.get("links", []) if ln.get("rel") == "next"), None)
        if not nxt:
            break
        url, body = nxt["href"], nxt.get("body", body)
    return out


def best_items(items: list[dict]) -> list[dict]:
    """One processing mode per orbit: reprocessed, else offline, else the near-real-time slices."""
    by_orbit: dict[int, list[dict]] = {}
    for it in items:
        by_orbit.setdefault(int(it["properties"].get("sat:absolute_orbit", -1)), []).append(it)
    keep = []
    for orbit, its in by_orbit.items():
        best = min(MODE_RANK.get(i["properties"].get("s5p:processing_mode", "NRTI"), 3) for i in its)
        keep += [i for i in its if MODE_RANK.get(i["properties"].get("s5p:processing_mode", "NRTI"), 3) == best]
    return keep


_SAS: dict[str, tuple[str, float]] = {}


def nc_href(item: dict) -> str:
    return next(a["href"] for a in item["assets"].values() if a["href"].endswith(".nc"))


def _signed(s, href: str) -> str:
    container = "/".join(href.split("/")[:4])
    tok = _SAS.get(container)
    if tok is None or time.time() - tok[1] > 1800:
        for attempt in range(6):
            r = s.get(SIGN, params={"href": href}, timeout=60)
            if r.status_code != 429:
                break
            time.sleep(min(60.0, float(r.headers.get("Retry-After") or 5 * 2 ** attempt)))
        r.raise_for_status()
        tok = (r.json()["href"].split("?", 1)[1], time.time())
        _SAS[container] = tok
    return f"{href}?{tok[0]}"


def distance_km(lat: np.ndarray, lon: np.ndarray, site: Site) -> np.ndarray:
    """Great-circle distance (haversine) from the site to every pixel."""
    p1, p2 = np.radians(site.lat), np.radians(lat)
    dl = np.radians((lon - site.lon + 180.0) % 360.0 - 180.0)
    a = np.sin((p2 - p1) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 6371.0 * 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def site_stats(lat, lon, so2, qa, site: Site, radius_km: float = RADIUS_KM) -> dict | None:
    """Plume / ring means (DU) for one site from one overpass; None when the site isn't under the swath."""
    d = distance_km(lat, lon, site)
    if not np.isfinite(d).any() or np.nanmin(d) > radius_km:
        return None
    good = (qa >= 50) & np.isfinite(so2) & (np.abs(so2) < FILL)
    plume, ring = good & (d <= radius_km), good & (d >= RING_KM[0]) & (d <= RING_KM[1])
    if plume.sum() == 0:
        return {"n_plume": 0, "n_ring": int(ring.sum()), "so2_plume_du": np.nan, "so2_ring_du": np.nan,
                "so2_enh_du": np.nan}
    p = float(so2[plume].mean()) * MOL_M2_TO_DU
    r = float(so2[ring].mean()) * MOL_M2_TO_DU if ring.sum() else np.nan
    return {"n_plume": int(plume.sum()), "n_ring": int(ring.sum()), "so2_plume_du": p, "so2_ring_du": r,
            "so2_enh_du": p - r if np.isfinite(r) else np.nan}


def read_item(s, item: dict, sites: list[Site]) -> list[dict]:
    """Per site under this orbit: the plume / ring statistics (reads only the needed variables and rows)."""
    import fsspec
    import h5py

    props = item["properties"]
    url = _signed(s, nc_href(item))
    rows = []
    import aiohttp

    # a stalled read must not hang the whole collection (2021-05 sat for 4 hours on one): time out and retry
    timeout = aiohttp.ClientTimeout(total=240, sock_connect=30, sock_read=60)
    with fsspec.open(url, block_size=4 * 2**20, client_kwargs={"timeout": timeout}).open() as f, h5py.File(f, "r") as h:
        lat, lon = h["PRODUCT/latitude"][0], h["PRODUCT/longitude"][0]
        reach = RING_KM[1] + 10.0
        boxes = []
        for site in sites:
            d = distance_km(lat, lon, site)
            near = np.argwhere(d <= reach)
            if len(near) == 0 or d.min() > RADIUS_KM:
                continue
            (r0, c0), (r1, c1) = near.min(0), near.max(0) + 1
            boxes.append((site, r0, r1, c0, c1))
        if not boxes:
            return []
        R0, R1 = min(b[1] for b in boxes), max(b[2] for b in boxes)
        so2 = h[VAR][0, R0:R1, :]
        qa = h["PRODUCT/qa_value"][0, R0:R1, :]
        t0 = pd.Timestamp(props.get("start_datetime") or props["datetime"]).tz_localize(None)
        for site, r0, r1, c0, c1 in boxes:
            sl = (slice(r0 - R0, r1 - R0), slice(c0, c1))
            st = site_stats(lat[r0:r1, c0:c1], lon[r0:r1, c0:c1], so2[sl], qa[sl], site)
            if st is None:
                continue
            rows.append({"date": t0.normalize(), "time": t0, "site": site.name, "commodity": site.commodity,
                         "orbit": int(props.get("sat:absolute_orbit", -1)),
                         "mode": props.get("s5p:processing_mode", ""), **st})
    return rows


MAX_FAILED_SHARE = 0.10          # a month with more failed files than this is not cached
ITEM_TIMEOUT_S = 600             # a read still running after this is killed (h5py can hang on a bad file)


def _read_child(conn, it: dict, ss: list[Site]) -> None:
    """Runs in a forked process: read one orbit file (3 tries) and send back its rows or the error."""
    last = None
    for attempt in range(3):
        try:
            conn.send(("ok", read_item(_session(), it, ss)))
            conn.close()
            return
        except Exception as exc:
            last = exc
            time.sleep(2 * (attempt + 1))
    conn.send(("err", str(last)))
    conn.close()


def run_isolated(jobs: list[tuple[dict, list[Site]]], workers: int, timeout_s: float = ITEM_TIMEOUT_S,
                 target=_read_child, before_fork=None, stats: dict | None = None):
    """Yield each job's rows, reading every file in its own forked process.

    h5py serialises all reads behind one global lock, so in a thread pool a single read that hangs
    (a damaged file, a dead connection) stalls every other thread - the 2021 run sat idle for five
    hours that way. A separate process per file can be killed when it overruns ``timeout_s``.
    ``before_fork(item)`` runs in the parent first (it fetches the storage token there, so the children
    inherit it instead of each asking the signing service). ``stats["failed"]`` counts failed files.
    """
    stats = stats if stats is not None else {}
    stats.setdefault("failed", 0)
    ctx = mp.get_context("fork")
    todo = list(jobs)
    running: dict = {}                      # parent conn -> (process, item id, start time)
    while todo or running:
        while todo and len(running) < workers:
            it, ss = todo.pop(0)
            if before_fork is not None:
                try:
                    before_fork(it)
                except Exception as exc:
                    LOG.warning("s5p item %s: %s", it["id"], exc)
                    stats["failed"] += 1
                    yield []
                    continue
            recv, send = ctx.Pipe(duplex=False)
            p = ctx.Process(target=target, args=(send, it, ss), daemon=True)
            p.start()
            send.close()
            running[recv] = (p, it["id"], time.time())
        for conn in mp_wait(list(running), timeout=5):
            p, iid, _ = running.pop(conn)
            try:
                status, val = conn.recv()
            except (EOFError, OSError):
                status, val = "err", f"worker exited with code {p.exitcode}"
            conn.close()
            p.join(10)
            if status == "ok":
                yield val
            else:
                LOG.warning("s5p item %s failed: %s", iid, val)
                stats["failed"] += 1
                yield []
        now = time.time()
        for conn, (p, iid, t0) in list(running.items()):
            if now - t0 > timeout_s:
                p.kill()
                p.join(10)
                conn.close()
                del running[conn]
                LOG.warning("s5p item %s killed after %.0f s", iid, now - t0)
                stats["failed"] += 1
                yield []


def collect(start: str, end: str, sites: list[Site] | None = None, workers: int = 24) -> pd.DataFrame:
    """Per site and overpass, between ``start`` and ``end``."""
    sites = sites or SITES
    s = _session()
    items: dict[str, tuple[dict, list[Site]]] = {}
    found = []
    for site in sites:
        try:
            its = search_items(s, site, start, end)
        except Exception as exc:
            LOG.warning("s5p search %s: %s", site.name, exc)
            continue
        for it in its:
            found.append(it)
            items.setdefault(it["id"], (it, []))[1].append(site)
    keep = {it["id"] for it in best_items(list({i["id"]: i for i in found}.values()))}
    jobs = [v for k, v in items.items() if k in keep]
    LOG.info("s5p: %d orbit files for %d sites, %s to %s", len(jobs), len(sites), start, end)

    rows, t, stats = [], time.time(), {}
    for done, r in enumerate(run_isolated(jobs, workers, before_fork=lambda it: _signed(s, nc_href(it)),
                                          stats=stats), 1):
        rows += r
        if done % 500 == 0:
            LOG.info("s5p: %d / %d files (%.0f s)", done, len(jobs), time.time() - t)
    df = pd.DataFrame(rows, columns=COLS)
    df = df[(df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))]
    df = df.sort_values(["date", "site", "time"]).reset_index(drop=True)
    df.attrs["failed_share"] = stats["failed"] / len(jobs) if jobs else 0.0
    return df


def daily_by_site(raw: pd.DataFrame) -> pd.DataFrame:
    """Per site and day: the pixel-weighted mean over that day's overpasses (high-latitude plants get several)."""
    r = raw.dropna(subset=["so2_enh_du"]).copy()
    r = r[r["n_plume"] > 0]
    r["w_enh"] = r["so2_enh_du"] * r["n_plume"]
    g = r.groupby(["date", "site", "commodity"])
    out = g.agg(n_plume=("n_plume", "sum"), w_enh=("w_enh", "sum")).reset_index()
    out["so2_enh_du"] = out["w_enh"] / out["n_plume"]
    return out.drop(columns="w_enh")


def collect_cached(start: str, end: str, cache: Path, refresh_days: int = 45) -> pd.DataFrame:
    """``collect`` in monthly chunks kept as ``cache/s5p_<YYYY-MM>.parquet``. A month is fetched again
    while it ends less than ``refresh_days`` ago (offline products replace the near-real-time ones)."""
    cache.mkdir(parents=True, exist_ok=True)
    now = pd.Timestamp.now().normalize()
    frames = []
    a0 = max(pd.Timestamp(start), pd.Timestamp(FIRST_DAY))
    for m in pd.period_range(a0, pd.Timestamp(end), freq="M"):
        f = cache / f"s5p_{m}.parquet"
        m_end = m.end_time.normalize()
        if f.exists() and m_end < now - pd.Timedelta(days=refresh_days):
            frames.append(pd.read_parquet(f))
            continue
        a, b = max(a0, m.start_time), min(pd.Timestamp(end), m_end)
        df = collect(f"{a:%Y-%m-%d}", f"{b:%Y-%m-%d}")
        bad = df.attrs.get("failed_share", 0.0)
        if bad > MAX_FAILED_SHARE:
            LOG.warning("s5p %s: %.0f%% of files failed - not cached, the next run fetches it again", m, 100 * bad)
        elif len(df) or not f.exists():
            df.to_parquet(f)
        frames.append(df if len(df) else pd.read_parquet(f))
        LOG.info("s5p %s: %d rows", m, len(df))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=COLS)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default=FIRST_DAY)
    ap.add_argument("--end", default=None)
    ap.add_argument("--cache", default="data/satellite")
    args = ap.parse_args(argv)
    setup_logging()
    end = args.end or f"{pd.Timestamp.now():%Y-%m-%d}"
    df = collect_cached(args.start, end, Path(args.cache))
    print(json.dumps({"rows": len(df), "sites_seen": int(df.loc[df["n_plume"] > 0, "site"].nunique()) if len(df) else 0}))


if __name__ == "__main__":
    main()
