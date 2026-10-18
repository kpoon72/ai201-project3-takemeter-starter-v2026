"""Collect public r/nba comments from the Arctic Shift Reddit archive.

Writes data/nba_pool.csv: a pool of candidate posts to read and label from.
Timeboxed helper, not part of the model pipeline.
"""
import csv
import json
import time
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

API = "https://arctic-shift.photon-reddit.com/api/comments/search"
OUT = Path(__file__).resolve().parent.parent / "data" / "nba_pool.csv"
SKIP_AUTHORS = {"AutoModerator", "[deleted]"}


def fetch(day):
    params = {
        "subreddit": "nba",
        "after": day.isoformat(),
        "before": (day + timedelta(days=1)).isoformat(),
        "limit": 100,
        "fields": "id,body,score,author,link_id,created_utc",
    }
    req = urllib.request.Request(
        f"{API}?{urllib.parse.urlencode(params)}",
        headers={"User-Agent": "takemeter-class-project"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["data"] or []


def keep(c):
    body = (c.get("body") or "").strip()
    return (
        c.get("author") not in SKIP_AUTHORS
        and body not in ("[deleted]", "[removed]")
        and 40 <= len(body) <= 1200
        and "http" not in body
        and (c.get("score") or 0) >= 2
    )


def main():
    rows, seen = [], set()
    start = date(2026, 9, 20)
    for i in range(27):
        day = start + timedelta(days=i)
        try:
            batch = fetch(day)
        except Exception as e:
            print(day, "failed:", e)
            time.sleep(5)
            continue
        kept = [c for c in batch if keep(c) and c["id"] not in seen]
        for c in kept:
            seen.add(c["id"])
            rows.append({"id": c["id"], "date": day.isoformat(), "score": c["score"],
                         "text": " ".join(c["body"].split())})
        print(day, len(batch), "fetched,", len(kept), "kept")
        time.sleep(2)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "date", "score", "text"])
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "rows ->", OUT)


if __name__ == "__main__":
    main()
