from __future__ import annotations

import html
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd


def clean_title(value: Any) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", "", text)
    text = unicodedata.normalize("NFKC", text)
    return re.sub(r"\s+", " ", text).strip()


def category_path(item: dict[str, Any]) -> str:
    return " > ".join(clean_title(item.get(f"category{i}")) for i in range(1, 5) if clean_title(item.get(f"category{i}")))


def read_naver_items(raw_dir: Path) -> list[dict[str, Any]]:
    items = []
    for path in sorted(raw_dir.glob("query_*/page_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for item in payload.get("items", []):
            row = dict(item)
            row["source_query"] = path.parent.name.removeprefix("query_")
            row["source_page"] = path.stem
            items.append(row)
    return items


def preprocess_naver(raw_dir: Path, output_csv: Path, conflict_csv: Path) -> dict[str, int]:
    items = read_naver_items(raw_dir)
    by_id: dict[str, dict[str, Any]] = {}
    provenance: defaultdict[str, list[str]] = defaultdict(list)
    conflicts = []
    for item in items:
        source_id = str(item.get("productId") or "").strip()
        if not source_id:
            continue
        provenance[source_id].append(str(item.get("source_query", "")))
        normalized = clean_title(item.get("title"))
        candidate = {
            "source_product_id": source_id, "product_type": item.get("productType"),
            "raw_title": item.get("title", ""), "name_normalized": normalized,
            "brand": clean_title(item.get("brand")), "maker": clean_title(item.get("maker")),
            "category1": clean_title(item.get("category1")), "category2": clean_title(item.get("category2")),
            "category3": clean_title(item.get("category3")), "category4": clean_title(item.get("category4")),
            "category_path": category_path(item), "naver_lprice": item.get("lprice"),
            "naver_hprice": item.get("hprice"), "thumbnail_url": item.get("image"),
            "mall_name": item.get("mallName"), "source_url": item.get("link"),
            "source_query": item.get("source_query"), "source_page": item.get("source_page"),
        }
        if source_id in by_id:
            old = by_id[source_id]
            if (old["name_normalized"], old["category_path"]) != (normalized, candidate["category_path"]):
                conflicts.append({"source_product_id": source_id, "old_name": old["name_normalized"],
                                  "new_name": normalized, "old_category": old["category_path"],
                                  "new_category": candidate["category_path"]})
        else:
            by_id[source_id] = candidate
    rows = list(by_id.values())
    for row in rows:
        row["provenance_queries"] = "|".join(sorted(set(provenance[row["source_product_id"]])))
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_csv, index=False, encoding="utf-8-sig")
    pd.DataFrame(conflicts).to_csv(conflict_csv, index=False, encoding="utf-8-sig")
    return {"raw_rows": len(items), "processed_rows": len(rows), "duplicate_count": len(items) - len(rows), "conflict_count": len(conflicts)}


def category_seeds(staging_csv: Path, output_csv: Path, root_depth: int = 1) -> dict[str, int]:
    df = pd.read_csv(staging_csv, dtype=str).fillna("")
    paths: set[str] = set()
    for path in df.get("category_path", []):
        parts = [p.strip() for p in str(path).split(" > ") if p.strip()]
        paths.update(" > ".join(parts[:i]) for i in range(1, len(parts) + 1))
    ordered = sorted(paths, key=lambda p: (p.count(" > "), p))
    ids = {p: i + 1 for i, p in enumerate(ordered)}
    rows = []
    for path in ordered:
        parts = path.split(" > ")
        parent = " > ".join(parts[:-1]) or ""
        rows.append({"seed_category_id": ids[path], "category_key": path, "parent_category_key": parent,
                     "name": parts[-1], "depth": root_depth + len(parts) - 1, "source": "NAVER_SHOP_API",
                     "source_category_path": path})
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_csv, index=False, encoding="utf-8-sig")
    return {"category_count": len(rows)}


def product_catalog_seeds(staging_csv: Path, category_csv: Path, output_csv: Path,
                          use_lprice: bool = False) -> dict[str, int]:
    products = pd.read_csv(staging_csv, dtype=str).fillna("")
    categories = pd.read_csv(category_csv, dtype=str).fillna("")
    ids = dict(zip(categories["category_key"], categories["seed_category_id"]))
    rows = []
    for _, item in products.iterrows():
        path = item.get("category_path", "")
        rows.append({"source_product_id": item.get("source_product_id", ""), "name": item.get("name_normalized", ""),
                     "category_key": path, "seed_category_id": ids.get(path, ""),
                     "thumbnail_url": item.get("thumbnail_url", ""), "description": "",
                     "spec_summary": "", "list_price": item.get("naver_lprice", "") if use_lprice else "",
                     "status": "ACTIVE"})
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_csv, index=False, encoding="utf-8-sig")
    return {"catalog_count": len(rows)}
