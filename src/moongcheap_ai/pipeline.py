from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import pandas as pd

from .collectors import CollectionError, collect_mfds, collect_naver
from .config import Settings, ensure_dirs, paths
from .facet import preprocess_i0030, preprocess_i2710, repeated_terms, structured_distribution, taxonomy_v0
from .preprocess import category_seeds, preprocess_naver, product_catalog_seeds


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
LOGGER = logging.getLogger(__name__)


def _report(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def run(root: Path, collect: bool = True) -> None:
    settings = Settings()
    ensure_dirs(root)
    p = paths(root)
    if collect:
        queries = json.loads((root / "config/naver_seed_queries.json").read_text(encoding="utf-8"))
        naver = collect_naver(queries, p["raw_naver"], settings.naver_client_id, settings.naver_client_secret,
                              settings.naver_display, settings.naver_max_pages_per_query,
                              settings.naver_max_requests, settings.naver_sleep_seconds)
        _report(p["reports"] / "naver_collection_summary.json", naver)
        for service in ("I0030", "I2710"):
            result = collect_mfds(service, settings.mfds_api_key, p["raw_mfds"] / service,
                                   max_pages=settings.mfds_max_pages)
            _report(p["reports"] / f"mfds_{service.lower()}_summary.json", result)
    staging = preprocess_naver(p["raw_naver"], p["interim_catalog"] / "naver_products_staging.csv",
                               p["reports"] / "naver_product_conflicts.csv")
    _report(p["reports"] / "naver_preprocessing_summary.json", staging)
    categories = category_seeds(p["interim_catalog"] / "naver_products_staging.csv",
                                p["processed_db"] / "category_seed.csv", settings.category_root_depth)
    catalog = product_catalog_seeds(p["interim_catalog"] / "naver_products_staging.csv",
                                    p["processed_db"] / "category_seed.csv",
                                    p["processed_db"] / "product_catalog_seed.csv",
                                    settings.use_naver_lprice_as_list_price)
    _report(p["reports"] / "category_summary.json", categories | catalog)
    i0030 = preprocess_i0030(p["raw_mfds"] / "I0030", p["interim_facet"] / "i0030_products_clean.csv")
    _report(p["reports"] / "mfds_i0030_preprocessing_summary.json", i0030)
    i2710 = preprocess_i2710(p["raw_mfds"] / "I2710", p["interim_facet"] / "i2710_reference.csv")
    _report(p["reports"] / "mfds_i2710_preprocessing_summary.json", i2710)
    mfds = pd.read_csv(p["interim_facet"] / "i0030_products_clean.csv", dtype=str).fillna("")
    terms = repeated_terms(mfds, ["name", "main_functionality", "functional_ingredients", "other_ingredients"],
                           settings.min_term_documents, settings.min_term_document_ratio)
    terms.to_csv(p["interim_facet"] / "repeated_terms.csv", index=False, encoding="utf-8-sig")
    structured = structured_distribution(mfds, ["product_form", "product_type", "intake_method", "storage_method", "functional_ingredients", "main_functionality"])
    structured.to_csv(p["interim_facet"] / "structured_value_distribution.csv", index=False, encoding="utf-8-sig")
    result = taxonomy_v0("SEED", "pilot", terms)
    (p["processed_facet"] / "facet_taxonomy_v0.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    terms.rename(columns={"term": "evidence_terms"}).assign(category_id="SEED", category_name="pilot",
        facet_candidate="PENDING", value_candidate=lambda d: d["evidence_terms"], aliases="",
        review_decision="", review_note="").to_csv(p["processed_facet"] / "facet_review_queue.csv", index=False, encoding="utf-8-sig")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--no-collect", action="store_true", help="Use existing raw files")
    args = parser.parse_args()
    try:
        run(args.root, collect=not args.no_collect)
    except CollectionError as exc:
        raise SystemExit(f"Collection stopped: {exc}") from exc


if __name__ == "__main__":
    main()
