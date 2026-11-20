"""Probe: Sentinel-5P SO2 on the Planetary Computer - item layout, file sizes, partial-read speed."""
import json, time
import requests

STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
SIGN = "https://planetarycomputer.microsoft.com/api/sas/v1/sign"
s = requests.Session()

for coll in ["sentinel-5p-l2-netcdf"]:
    r = s.get(f"{STAC}/collections/{coll}", timeout=60)
    print(coll, r.status_code)
    if r.ok:
        c = r.json()
        print(json.dumps({k: c.get(k) for k in ("extent", "summaries")}, default=str)[:3000])

body = {"collections": ["sentinel-5p-l2-netcdf"], "intersects": {"type": "Point", "coordinates": [87.93, 69.32]},
        "datetime": "2024-06-01/2024-06-03", "limit": 50, "query": {"s5p:product_name": {"eq": "so2"}}}
r = s.post(f"{STAC}/search", json=body, timeout=120)
print("search", r.status_code, r.text[:500] if not r.ok else "")
feats = r.json().get("features", []) if r.ok else []
print("items:", len(feats))
if not feats:
    body.pop("query")
    r = s.post(f"{STAC}/search", json=body, timeout=120)
    feats = r.json().get("features", [])
    print("items without filter:", len(feats))
    for f in feats[:40]:
        print(f["id"], {k: v for k, v in f["properties"].items() if k.startswith("s5p")})
for f in feats[:3]:
    print(json.dumps(f["properties"], default=str)[:1500])
    for name, a in f["assets"].items():
        print(" asset", name, a.get("href"), a.get("type"))
so2 = [f for f in feats if "SO2" in f["id"]]
print("SO2 items:", len(so2), [f["id"] for f in so2][:10])
if so2:
    href = next(iter(so2[0]["assets"].values()))["href"]
    for a in so2[0]["assets"].values():
        if a["href"].endswith(".nc"):
            href = a["href"]
    tok = s.get(SIGN, params={"href": href}, timeout=60).json()["href"]
    h = s.head(tok, timeout=60)
    print("size MB", int(h.headers.get("Content-Length", 0)) / 1e6)
    import fsspec, h5py
    t = time.time()
    f = fsspec.open(tok, block_size=2**20).open()
    hf = h5py.File(f, "r")
    def walk(g, pre=""):
        for k, v in g.items():
            if isinstance(v, h5py.Dataset):
                if v.ndim >= 2:
                    print(" ds", pre + k, v.shape, v.dtype, "chunks", v.chunks, "comp", v.compression)
            else:
                walk(v, pre + k + "/")
    walk(hf["PRODUCT"], "PRODUCT/")
    print("open+walk s", round(time.time() - t, 1))
    t = time.time()
    lat = hf["PRODUCT/latitude"][0]
    lon = hf["PRODUCT/longitude"][0]
    print("lat/lon read s", round(time.time() - t, 1), lat.shape)
    import numpy as np
    d = (lat - 69.32) ** 2 + ((lon - 87.93) * np.cos(np.radians(69.32))) ** 2
    i, j = np.unravel_index(np.argmin(d), d.shape)
    print("nearest pixel", i, j, float(np.sqrt(d[i, j])) * 111, "km")
    t = time.time()
    so2v = hf["PRODUCT/sulfurdioxide_total_vertical_column"][0, max(i - 10, 0):i + 10, max(j - 10, 0):j + 10]
    qa = hf["PRODUCT/qa_value"][0, max(i - 10, 0):i + 10, max(j - 10, 0):j + 10]
    print("window read s", round(time.time() - t, 1), np.nanmax(so2v), qa.max())
