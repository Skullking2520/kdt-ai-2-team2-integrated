from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _int(name: str, default: int) -> int:
    value = os.getenv(name)
    return default if value in (None, "") else int(value)


def _optional_int(name: str) -> int | None:
    value = os.getenv(name)
    return None if value in (None, "") else int(value)


@dataclass(frozen=True)
class Settings:
    naver_client_id: str | None = os.getenv("NAVER_CLIENT_ID")
    naver_client_secret: str | None = os.getenv("NAVER_CLIENT_SECRET")
    mfds_api_key: str | None = os.getenv("MFDS_API_KEY")
    naver_display: int = _int("NAVER_DISPLAY", 100)
    naver_max_pages_per_query: int = _int("NAVER_MAX_PAGES_PER_QUERY", 2)
    naver_max_requests: int = _int("NAVER_MAX_REQUESTS", 50)
    naver_sleep_seconds: float = float(os.getenv("NAVER_SLEEP_SECONDS", "0.2"))
    mfds_max_pages: int | None = _optional_int("MFDS_MAX_PAGES")
    category_root_depth: int = _int("CATEGORY_ROOT_DEPTH", 1)
    min_term_documents: int = _int("MIN_TERM_DOCUMENTS", 3)
    min_term_document_ratio: float = float(os.getenv("MIN_TERM_DOCUMENT_RATIO", "0.05"))
    use_naver_lprice_as_list_price: bool = os.getenv("USE_NAVER_LPRICE_AS_LIST_PRICE", "false").lower() == "true"


def paths(root: Path = ROOT) -> dict[str, Path]:
    return {
        "root": root,
        "raw_naver": root / "data/raw/naver_shop",
        "raw_mfds": root / "data/raw/mfds_health",
        "interim_catalog": root / "data/interim/catalog",
        "interim_facet": root / "data/interim/facet_discovery",
        "processed_db": root / "data/processed/db_seed",
        "processed_facet": root / "data/processed/facet_discovery",
        "reports": root / "data/reports",
    }


def ensure_dirs(root: Path = ROOT) -> None:
    for path in paths(root).values():
        if path.suffix == "":
            path.mkdir(parents=True, exist_ok=True)
