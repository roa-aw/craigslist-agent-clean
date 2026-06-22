"""
db/setup.py
Loads the Craigslist vehicles CSV, cleans it, and writes it to SQLite.
Run once: python -m db.setup
"""

import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "inventory.db")
DEFAULT_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "vehicles.csv")

MANUFACTURER_FIXES = {
    "alfa-romeo": "alfa-romeo",
    "mercedes-benz": "mercedes-benz",
    "land rover": "land rover",
    "aston-martin": "aston-martin",
    "harley-davidson": "harley-davidson",
}

VALID_CONDITIONS = {"new", "like new", "excellent", "good", "fair", "salvage"}
VALID_CYLINDERS = {"3 cylinders", "4 cylinders", "5 cylinders", "6 cylinders",
                   "8 cylinders", "10 cylinders", "12 cylinders", "other"}


def clean(df: pd.DataFrame) -> pd.DataFrame:
    # Keep only useful columns
    cols = ["id", "url", "region", "price", "year", "manufacturer",
            "model", "condition", "cylinders", "fuel", "odometer",
            "title_status", "transmission", "drive", "type", "paint_color", "state"]
    cols = [c for c in cols if c in df.columns]
    df = df[cols].copy()

    # ── price ──────────────────────────────────────────────────────────────
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df[(df["price"] > 200) & (df["price"] < 300_000)]

    # ── year ───────────────────────────────────────────────────────────────
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df[(df["year"] >= 1900) & (df["year"] <= 2025)]
    df["year"] = df["year"].astype(int)

    # ── manufacturer ───────────────────────────────────────────────────────
    df["manufacturer"] = df["manufacturer"].astype(str).str.strip().str.lower()
    df["manufacturer"] = df["manufacturer"].replace("nan", pd.NA)
    df = df.dropna(subset=["manufacturer"])

    # ── model ──────────────────────────────────────────────────────────────
    df["model"] = df["model"].astype(str).str.strip().str.lower()
    df["model"] = df["model"].replace("nan", pd.NA)

    # ── condition ──────────────────────────────────────────────────────────
    df["condition"] = df["condition"].astype(str).str.strip().str.lower()
    df.loc[~df["condition"].isin(VALID_CONDITIONS), "condition"] = pd.NA

    # ── cylinders ──────────────────────────────────────────────────────────
    df["cylinders"] = df["cylinders"].astype(str).str.strip().str.lower()
    df.loc[~df["cylinders"].isin(VALID_CYLINDERS), "cylinders"] = pd.NA

    # ── odometer ───────────────────────────────────────────────────────────
    if "odometer" in df.columns:
        df["odometer"] = pd.to_numeric(df["odometer"], errors="coerce")
        df.loc[df["odometer"] > 500_000, "odometer"] = pd.NA

    # ── misc string cleaning ───────────────────────────────────────────────
    for col in ["fuel", "transmission", "drive", "type", "paint_color", "state", "region"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower().replace("nan", pd.NA)

    df = df.drop_duplicates(subset=["id"])
    df = df.reset_index(drop=True)
    return df


def build_db(csv_path: str = DEFAULT_CSV, db_path: str = DB_PATH) -> None:
    print(f"Reading CSV: {csv_path}")
    raw = pd.read_csv(csv_path, low_memory=False)
    print(f"  Raw rows : {len(raw):,}")

    df = clean(raw)
    print(f"  Clean rows: {len(df):,}")

    conn = sqlite3.connect(db_path)
    df.to_sql("vehicles", conn, if_exists="replace", index=False)

    # Indexes speed up common filter combos
    conn.execute("CREATE INDEX IF NOT EXISTS idx_manufacturer ON vehicles(manufacturer)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_price ON vehicles(price)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_year ON vehicles(year)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_condition ON vehicles(condition)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_region ON vehicles(region)")
    conn.commit()
    conn.close()
    print(f"  Database written: {db_path}")


if __name__ == "__main__":
    build_db()
