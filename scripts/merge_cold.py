"""Merge the hand-labelled cold20.csv into labels.csv (keeping its note column).

Run once, after filling in every label in cold20.csv.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
LABELS = {"analysis", "hot_take", "reaction", "trash_talk"}

cold = pd.read_csv(ROOT / "cold20.csv")
cold["label"] = cold["label"].fillna("").str.strip()
bad = cold[~cold["label"].isin(LABELS)]
if len(bad):
    raise SystemExit(f"Fix these rows in cold20.csv first (label must be one of {sorted(LABELS)}):\n"
                     + bad[["label", "text"]].to_string())

labels = pd.read_csv(ROOT / "labels.csv")
labels = labels[~labels["text"].isin(cold["text"])]
cold = cold[["text", "label", "note"]]
merged = pd.concat([cold, labels], ignore_index=True)
merged.to_csv(ROOT / "labels.csv", index=False)
print(f"{len(merged)} rows in labels.csv")
print(merged["label"].value_counts(normalize=True).round(3).to_string())
