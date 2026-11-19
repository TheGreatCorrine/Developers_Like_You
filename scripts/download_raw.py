"""Download the raw Stack Overflow Developer Survey results (2023-2025) and verify them.
Source: official StackExchange/Survey archive on GitHub, commit 32a1145 (same files and SHA-256 as the team's Drive copy)."""
import hashlib, urllib.request
from pathlib import Path

BASE = "https://media.githubusercontent.com/media/StackExchange/Survey/32a114542da67e3759479637343718502742adfd/packages/archive/{y}/results.csv"
SHA = {2023: "828874a3cf0fa1bbb4c3da6a87e5822b8563bbc04b21f9869479480dbcff410c",
       2024: "7f2c2dbf6989d00b80a7351de4bb3af4b52b21cc52d5c947891bbc4f4e5cbe49",
       2025: "2d1f65308877282edfb4470520eabbc08cb499118432a3dcec6a66c086aa2baa"}
RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
for y, h in SHA.items():
    f = RAW / f"results_{y}.csv"
    if not f.exists():
        print("downloading", y); urllib.request.urlretrieve(BASE.format(y=y), f)
    ok = hashlib.sha256(f.read_bytes()).hexdigest() == h
    print(y, "sha256 ok" if ok else "SHA-256 MISMATCH")
