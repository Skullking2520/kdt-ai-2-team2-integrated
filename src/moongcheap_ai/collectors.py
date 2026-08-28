from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import requests


NAVER_URL = "https://openapi.naver.com/v1/search/shop.json"
MFDS_URL = "https://openapi.foodsafetykorea.go.kr/api"


class CollectionError(RuntimeError):
    pass


def _request_json(session: requests.Session, url: str, *, headers: dict[str, str] | None = None,
                 params: dict[str, Any] | None = None, timeout: int = 30) -> dict[str, Any]:
    response = session.get(url, headers=headers, params=params, timeout=timeout)
    if response.status_code in {401, 403}:
        raise CollectionError(f"Authentication/permission failed ({response.status_code}) for {url}")
    if response.status_code == 429 or response.status_code >= 500:
        raise requests.HTTPError(f"Retryable HTTP status {response.status_code}", response=response)
    response.raise_for_status()
    return response.json()


def collect_naver(queries: list[str], output_dir: Path, client_id: str | None, client_secret: str | None,
                  display: int = 100, max_pages: int = 2, max_requests: int = 50,
                  sleep_seconds: float = 0.2, session: requests.Session | None = None) -> dict[str, int]:
    if not client_id or not client_secret:
        raise CollectionError("NAVER_CLIENT_ID and NAVER_CLIENT_SECRET are required")
    display = min(display, 100)
    output_dir.mkdir(parents=True, exist_ok=True)
    session = session or requests.Session()
    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
    request_count = 0
    item_count = 0
    for query in queries:
        safe_query = query.replace("/", "_").replace(" ", "_")
        for page in range(1, max_pages + 1):
            if request_count >= max_requests:
                return {"requests": request_count, "items": item_count}
            start = (page - 1) * display + 1
            payload = None
            for attempt in range(3):
                try:
                    payload = _request_json(session, NAVER_URL, headers=headers,
                                            params={"query": query, "display": display, "start": start})
                    break
                except requests.HTTPError:
                    if attempt == 2:
                        raise
                    time.sleep(2 ** attempt)
            path = output_dir / f"query_{safe_query}" / f"page_{page:03d}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            request_count += 1
            item_count += len(payload.get("items", []))
            if len(payload.get("items", [])) < display:
                break
            time.sleep(sleep_seconds)
    return {"requests": request_count, "items": item_count}


def collect_mfds(service: str, api_key: str | None, output_dir: Path, *, max_pages: int | None = None,
                 rows_per_page: int = 100, session: requests.Session | None = None) -> dict[str, int]:
    if not api_key:
        raise CollectionError("MFDS_API_KEY is required")
    output_dir.mkdir(parents=True, exist_ok=True)
    session = session or requests.Session()
    pages = 0
    rows = 0
    while max_pages is None or pages < max_pages:
        start = pages * rows_per_page + 1
        url = f"{MFDS_URL}/{api_key}/{service}/json/{start}/{start + rows_per_page - 1}"
        payload = None
        for attempt in range(3):
            try:
                payload = _request_json(session, url)
                break
            except requests.HTTPError:
                if attempt == 2:
                    raise
                time.sleep(2 ** attempt)
        path = output_dir / f"page_{pages + 1:03d}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        page_rows = _extract_rows(payload, service)
        rows += len(page_rows)
        pages += 1
        if len(page_rows) < rows_per_page:
            break
    return {"pages": pages, "rows": rows}


def _extract_rows(payload: dict[str, Any], service: str) -> list[dict[str, Any]]:
    body = payload.get(service, payload)
    if isinstance(body, dict):
        rows = body.get("row", body.get("rows", []))
        if isinstance(rows, list):
            return rows
    return []
