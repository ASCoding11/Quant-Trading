"""Satellite activity at critical-raw-material processing sites: MODIS daily thermal anomalies.

Smelters, nickel pig-iron furnaces and refineries are hot enough for NASA's MODIS fire product to
see them from orbit; how many 1 km pixels flag as "fire" around a plant, and their fire radiative
power (FRP), tracks how hard it is running. ``MOD14A1`` / ``MYD14A1`` (Terra and Aqua, collection
6.1) come from Microsoft's Planetary Computer: no key, history back to 2000, readable from a
GitHub runner (NASA's own FIRMS server times out from there). Each file covers one 1200 x 1200 km
tile and 8 days, one band per day: ``FireMask`` (7-9 = fire, low/nominal/high confidence; 4 = cloud)
and ``MaxFRP`` (MW x 10).

``collect(start, end)`` returns one row per site and day: fire pixels, summed FRP (MW) and the
pixels observed clear of cloud within ``radius_km`` of the site. NASA data: public domain, stored
in the clear.

The site list is hand-made from public maps; coordinates are approximate, which is why each site
uses a window of several kilometres and the research reports how often each one is detected.
"""
from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from ..utils import LOG, setup_logging

STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
SIGN = "https://planetarycomputer.microsoft.com/api/sas/v1/sign"
COLLECTION = "modis-14A1-061"


@dataclass(frozen=True)
class Site:
    name: str
    commodity: str          # copper, nickel, pgm_palladium, pgm_platinum, aluminium, rare_earths
    lat: float
    lon: float
    radius_km: float = 8.0


SITES = [
    # copper smelters
    Site("Chuquicamata smelter (Chile)", "copper", -22.32, -68.92),
    Site("Potrerillos smelter (Chile)", "copper", -26.43, -69.46),
    Site("Caletones smelter (Chile)", "copper", -34.12, -70.45),
    Site("Altonorte smelter (Chile)", "copper", -23.78, -70.33),
    Site("Tongling copper (China)", "copper", 30.94, 117.80),
    Site("Guixi smelter (China)", "copper", 28.29, 117.24),
    Site("Olympic Dam (Australia)", "copper", -30.44, 136.89),
    Site("Mount Isa smelter (Australia)", "copper", -20.72, 139.48),
    Site("Kolwezi copper-cobalt (DRC)", "copper", -10.72, 25.47, 15.0),
    # nickel (Indonesian nickel pig iron / matte parks, Russia, Canada, Australia)
    Site("IMIP Morowali (Indonesia)", "nickel", -2.82, 122.15, 10.0),
    Site("IWIP Weda Bay (Indonesia)", "nickel", 0.47, 127.95, 10.0),
    Site("Obi Island (Indonesia)", "nickel", -1.53, 127.42, 10.0),
    Site("Konawe / Morosi (Indonesia)", "nickel", -3.85, 122.32, 10.0),
    Site("Sorowako (Indonesia)", "nickel", -2.53, 121.36),
    Site("Sudbury Copper Cliff (Canada)", "nickel", 46.47, -81.06),
    Site("Kalgoorlie nickel smelter (Australia)", "nickel", -30.81, 121.42),
    # platinum group metals
    Site("Norilsk Nadezhda (Russia)", "pgm_palladium", 69.32, 87.93, 10.0),
    Site("Norilsk Nickel plant (Russia)", "pgm_palladium", 69.35, 88.12, 10.0),
    Site("Rustenburg / Waterval smelters (S. Africa)", "pgm_platinum", -25.62, 27.28, 12.0),
    Site("Polokwane smelter (S. Africa)", "pgm_platinum", -23.91, 29.47),
    # aluminium
    Site("Hongqiao Zouping (China)", "aluminium", 37.23, 117.74, 12.0),
    Site("Xinfa Chiping (China)", "aluminium", 36.58, 116.25, 10.0),
    Site("EGA Jebel Ali (UAE)", "aluminium", 24.99, 55.06),
    Site("Krasnoyarsk aluminium (Russia)", "aluminium", 56.05, 92.98),
    # rare earths
    Site("Baotou rare earth / steel (China)", "rare_earths", 40.63, 109.85, 12.0),
]


def _session():
    import requests

    s = requests.Session()
    s.headers["User-Agent"] = "qtrade-satellite (research)"
    return s


def search_items(s, site: Site, start: str, end: str) -> list[dict]:
    """Every MOD14A1 / MYD14A1 item whose tile contains the site, between the dates."""
    body = {"collections": [COLLECTION], "intersects": {"type": "Point", "coordinates": [site.lon, site.lat]},
            "datetime": f"{start}/{end}", "limit": 500}
    out, url = [], f"{STAC}/search"
    for _ in range(100):
        r = s.post(url, json=body, timeout=120)
        r.raise_for_status()
        page = r.json()
        out += page.get("features", [])
        nxt = next((ln for ln in page.get("links", []) if ln.get("rel") == "next"), None)
        if not nxt:
            break
        url, body = nxt["href"], nxt.get("body", body)
    return out


_SAS: dict[str, tuple[str, float]] = {}        # storage container -> (SAS query string, fetched at)


def _signed(s, href: str) -> str:
    """The asset URL with a Planetary Computer SAS token; one token per container, renewed every 30 min."""
    import time

    container = "/".join(href.split("/")[:4])
    tok = _SAS.get(container)
    if tok is None or time.time() - tok[1] > 1800:
        r = s.get(SIGN, params={"href": href}, timeout=60)
        r.raise_for_status()
        tok = (r.json()["href"].split("?", 1)[1], time.time())
        _SAS[container] = tok
    return f"{href}?{tok[0]}"


def read_item(s, item: dict, sites: list[Site]) -> list[dict]:
    """Per site and per day of the item's 8 days: fire pixels, FRP (MW) and clear pixels in the window."""
    import rasterio
    from rasterio.warp import transform

    props = item["properties"]
    start = pd.Timestamp(props.get("start_datetime") or props["datetime"]).tz_localize(None).normalize()
    mask_href, frp_href = _signed(s, item["assets"]["FireMask"]["href"]), _signed(s, item["assets"]["MaxFRP"]["href"])
    rows = []
    with rasterio.open(mask_href) as dm, rasterio.open(frp_href) as df:
        for site in sites:
            xs, ys = transform("EPSG:4326", dm.crs, [site.lon], [site.lat])
            row, col = dm.index(xs[0], ys[0])
            r = int(np.ceil(site.radius_km / abs(dm.res[0] / 1000.0)))       # pixels (~0.93 km each)
            if not (0 <= row < dm.height and 0 <= col < dm.width):
                continue
            win = ((max(row - r, 0), min(row + r + 1, dm.height)), (max(col - r, 0), min(col + r + 1, dm.width)))
            m = dm.read(window=win)                       # (days, h, w)
            f = df.read(window=win).astype(float) / 10.0  # MW
            yy, xx = np.mgrid[win[0][0]:win[0][1], win[1][0]:win[1][1]]
            disk = ((yy - row) ** 2 + (xx - col) ** 2) <= r * r
            for d in range(m.shape[0]):
                md, fd = m[d][disk], f[d][disk]
                fire = md >= 7
                rows.append({"date": start + pd.Timedelta(days=d), "site": site.name, "commodity": site.commodity,
                             "satellite": "Aqua" if item["id"].startswith("MYD") else "Terra",
                             "fire_pixels": int(fire.sum()), "frp_mw": float(fd[fire].sum()),
                             "clear_pixels": int(((md == 5) | fire).sum())})
    return rows


def collect(start: str, end: str, sites: list[Site] | None = None, workers: int = 16) -> pd.DataFrame:
    """Daily per-site rows between ``start`` and ``end`` (both satellites)."""
    sites = sites or SITES
    s = _session()
    by_item: dict[str, tuple[dict, list[Site]]] = {}
    for site in sites:
        try:
            for it in search_items(s, site, start, end):
                by_item.setdefault(it["id"], (it, []))[1].append(site)
        except Exception as exc:
            LOG.warning("satellite search %s: %s", site.name, exc)
    LOG.info("satellite: %d items for %d sites, %s to %s", len(by_item), len(sites), start, end)

    def job(pair):
        it, ss = pair
        for attempt in range(3):
            try:
                return read_item(_session(), it, ss)
            except Exception as exc:
                last = exc
        LOG.warning("satellite item %s failed: %s", it["id"], last)
        return []

    rows = []
    with ThreadPoolExecutor(workers) as ex:
        for r in ex.map(job, by_item.values()):
            rows += r
    cols = ["date", "site", "commodity", "satellite", "fire_pixels", "frp_mw", "clear_pixels"]
    df = pd.DataFrame(rows, columns=cols)
    df = df[(df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))]
    return df.sort_values(["date", "site", "satellite"]).reset_index(drop=True)


def daily_by_site(raw: pd.DataFrame) -> pd.DataFrame:
    """Terra and Aqua combined: per site and day, the larger fire count / FRP of the two overpasses."""
    g = raw.groupby(["date", "site", "commodity"])
    return g.agg(fire_pixels=("fire_pixels", "max"), frp_mw=("frp_mw", "max"),
                 clear_pixels=("clear_pixels", "max")).reset_index()


def collect_cached(start: str, end: str, cache: Path) -> pd.DataFrame:
    """``collect`` in yearly chunks, each kept as ``cache/modis_<year>.parquet`` (past years are final;
    the current year is refreshed every time)."""
    cache.mkdir(parents=True, exist_ok=True)
    this_year = pd.Timestamp.now().year
    frames = []
    for y in range(pd.Timestamp(start).year, pd.Timestamp(end).year + 1):
        f = cache / f"modis_{y}.parquet"
        if f.exists() and y < this_year:
            frames.append(pd.read_parquet(f))
            continue
        a, b = max(pd.Timestamp(start), pd.Timestamp(f"{y}-01-01")), min(pd.Timestamp(end), pd.Timestamp(f"{y}-12-31"))
        df = collect(f"{a:%Y-%m-%d}", f"{b:%Y-%m-%d}")
        df.to_parquet(f)
        frames.append(df)
        LOG.info("satellite %d: %d rows", y, len(df))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--cache", default="data/satellite")
    args = ap.parse_args(argv)
    setup_logging()
    df = collect_cached(args.start, args.end, Path(args.cache))
    print(json.dumps({"rows": len(df), "sites_detected": int((df.groupby("site")["fire_pixels"].sum() > 0).sum())
                      if len(df) else 0}))


if __name__ == "__main__":
    main()
