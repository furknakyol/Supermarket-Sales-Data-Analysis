#!/usr/bin/env python3
"""
scripts/get_data.py

Basit bir sample oluşturma / veri taşıma script'i.
Kullanım:
  python scripts/get_data.py --source data/sales.csv --out data/sample_sales.csv --sample 1000
"""
import argparse
import os
import pandas as pd

def make_sample(source, out, n):
    if not os.path.exists(source):
        raise FileNotFoundError(f"Source file not found: {source}")
    df = pd.read_csv(source)
    n = min(n, len(df))
    sample = df.sample(n=n, random_state=42)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    sample.to_csv(out, index=False)
    print(f"Sample saved to {out} ({n} rows)")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Create a sample CSV from a larger CSV")
    p.add_argument("--source", required=True, help="Kaynak CSV dosyası")
    p.add_argument("--out", default="data/sample_sales.csv", help="Çıktı sample dosyası")
    p.add_argument("--sample", type=int, default=1000, help="Sample satır sayısı")
    args = p.parse_args()
    make_sample(args.source, args.out, args.sample)
