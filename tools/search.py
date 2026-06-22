"""
tools/search.py
Python functions exposed to the LLM as callable tools.
Each function returns a dict that is JSON-serialisable.
"""

from __future__ import annotations
import sqlite3
from typing import Optional
from tools import get_conn


# ─────────────────────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────────────────────

def _rows_to_list(rows) -> list[dict]:
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────────────────────────
# Tool 1 – search_inventory
# ─────────────────────────────────────────────────────────────────────────────

def search_inventory(
    make: Optional[str] = None,
    model: Optional[str] = None,
    max_price: Optional[float] = None,
    min_price: Optional[float] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    condition: Optional[str] = None,
    cylinders: Optional[str] = None,
    fuel: Optional[str] = None,
    transmission: Optional[str] = None,
    drive: Optional[str] = None,
    color: Optional[str] = None,
    region: Optional[str] = None,
    state: Optional[str] = None,
    limit: int = 8,
) -> dict:
    """
    Search the vehicle inventory with optional filters.
    Returns up to `limit` matching vehicles as a list of dicts,
    plus a total count and the filters actually applied.
    """
    conn = get_conn()
    clauses: list[str] = []
    params: list = []

    def like(col: str, val: str) -> None:
        clauses.append(f"LOWER({col}) LIKE ?")
        params.append(f"%{val.lower().strip()}%")

    if make:
        like("manufacturer", make)
    if model:
        like("model", model)
    if color:
        like("paint_color", color)
    if region:
        like("region", region)
    if state:
        like("state", state)
    if condition:
        like("condition", condition)
    if cylinders:
        like("cylinders", cylinders)
    if fuel:
        like("fuel", fuel)
    if transmission:
        like("transmission", transmission)
    if drive:
        like("drive", drive)
    if min_price is not None:
        clauses.append("price >= ?")
        params.append(min_price)
    if max_price is not None:
        clauses.append("price <= ?")
        params.append(max_price)
    if min_year is not None:
        clauses.append("year >= ?")
        params.append(min_year)
    if max_year is not None:
        clauses.append("year <= ?")
        params.append(max_year)

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""

    count_row = conn.execute(
        f"SELECT COUNT(*) as n FROM vehicles {where}", params
    ).fetchone()
    total = count_row["n"]

    rows = conn.execute(
        f"""
        SELECT id, manufacturer, model, year, price, condition,
               cylinders, fuel, odometer, region, state, paint_color,
               transmission, drive, url
        FROM vehicles
        {where}
        ORDER BY price ASC
        LIMIT ?
        """,
        params + [limit],
    ).fetchall()
    conn.close()

    filters_used = {k: v for k, v in {
        "make": make, "model": model, "max_price": max_price,
        "min_price": min_price, "min_year": min_year, "max_year": max_year,
        "condition": condition, "color": color, "region": region,
        "state": state, "cylinders": cylinders, "fuel": fuel,
        "transmission": transmission, "drive": drive,
    }.items() if v is not None}

    return {
        "total_matches": total,
        "showing": len(rows),
        "filters_used": filters_used,
        "results": _rows_to_list(rows),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────────────────────

def _rows_to_list(rows) -> list[dict]:
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────────────────────────
# Tool 1 – search_inventory
# ─────────────────────────────────────────────────────────────────────────────

def search_inventory(
    make: Optional[str] = None,
    model: Optional[str] = None,
    max_price: Optional[float] = None,
    min_price: Optional[float] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    condition: Optional[str] = None,
    cylinders: Optional[str] = None,
    fuel: Optional[str] = None,
    transmission: Optional[str] = None,
    drive: Optional[str] = None,
    color: Optional[str] = None,
    region: Optional[str] = None,
    state: Optional[str] = None,
    limit: int = 8,
) -> dict:
    """
    Search the vehicle inventory with optional filters.
    Returns up to `limit` matching vehicles as a list of dicts,
    plus a total count and the filters actually applied.
    """
    conn = get_conn()
    clauses: list[str] = []
    params: list = []

    def like(col: str, val: str) -> None:
        clauses.append(f"LOWER({col}) LIKE ?")
        params.append(f"%{val.lower().strip()}%")

    if make:
        like("manufacturer", make)
    if model:
        like("model", model)
    if color:
        like("paint_color", color)
    if region:
        like("region", region)
    if state:
        like("state", state)
    if condition:
        like("condition", condition)
    if cylinders:
        like("cylinders", cylinders)
    if fuel:
        like("fuel", fuel)
    if transmission:
        like("transmission", transmission)
    if drive:
        like("drive", drive)
    if min_price is not None:
        clauses.append("price >= ?")
        params.append(min_price)
    if max_price is not None:
        clauses.append("price <= ?")
        params.append(max_price)
    if min_year is not None:
        clauses.append("year >= ?")
        params.append(min_year)
    if max_year is not None:
        clauses.append("year <= ?")
        params.append(max_year)

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""

    count_row = conn.execute(
        f"SELECT COUNT(*) as n FROM vehicles {where}", params
    ).fetchone()
    total = count_row["n"]

    rows = conn.execute(
        f"""
        SELECT id, manufacturer, model, year, price, condition,
               cylinders, fuel, odometer, region, state, paint_color,
               transmission, drive, url
        FROM vehicles
        {where}
        ORDER BY price ASC
        LIMIT ?
        """,
        params + [limit],
    ).fetchall()
    conn.close()

    filters_used = {k: v for k, v in {
        "make": make, "model": model, "max_price": max_price,
        "min_price": min_price, "min_year": min_year, "max_year": max_year,
        "condition": condition, "color": color, "region": region,
        "state": state, "cylinders": cylinders, "fuel": fuel,
        "transmission": transmission, "drive": drive,
    }.items() if v is not None}

    return {
        "total_matches": total,
        "showing": len(rows),
        "filters_used": filters_used,
        "results": _rows_to_list(rows),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Tool 2 – get_similar
# ─────────────────────────────────────────────────────────────────────────────

def get_similar(
    make: Optional[str] = None,
    max_price: Optional[float] = None,
    min_year: Optional[int] = None,
    limit: int = 5,
) -> dict:
    """
    Fuzzy fallback: find vehicles from the same maker (or any maker)
    within a relaxed price range (+20 %) and year range (-3 years).
    Used when search_inventory returns zero results.
    """
    relaxed_price = (max_price * 1.2) if max_price else None
    relaxed_year  = (min_year - 3)    if min_year  else None
    return search_inventory(
        make=make,
        max_price=relaxed_price,
        min_year=relaxed_year,
        limit=limit,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Tool 3 – get_makes
# ─────────────────────────────────────────────────────────────────────────────

def get_makes() -> dict:
    """Return a list of all distinct vehicle makes in the inventory."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT DISTINCT manufacturer FROM vehicles "
        "WHERE manufacturer IS NOT NULL "
        "ORDER BY manufacturer"
    ).fetchall()
    conn.close()
    return {"makes": [r["manufacturer"] for r in rows]}


# ─────────────────────────────────────────────────────────────────────────────
# Tool 4 – get_price_range
# ─────────────────────────────────────────────────────────────────────────────

def get_price_range(make: Optional[str] = None, model: Optional[str] = None) -> dict:
    """
    Return the min, max, and average price for a given make/model.
    Useful when the user asks 'what does a used Civic usually cost?'
    """
    conn = get_conn()
    clauses, params = [], []
    if make:
        clauses.append("LOWER(manufacturer) LIKE ?")
        params.append(f"%{make.lower()}%")
    if model:
        clauses.append("LOWER(model) LIKE ?")
        params.append(f"%{model.lower()}%")

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    row = conn.execute(
        f"SELECT MIN(price) as low, MAX(price) as high, "
        f"ROUND(AVG(price),0) as avg, COUNT(*) as n "
        f"FROM vehicles {where}",
        params,
    ).fetchone()
    conn.close()
    if not row or row["n"] == 0:
        return {"error": "No listings found for that make/model."}
    return {
        "make": make,
        "model": model,
        "count": row["n"],
        "min_price": row["low"],
        "max_price": row["high"],
        "avg_price": row["avg"],
    }

