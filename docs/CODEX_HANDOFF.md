# Codex Handoff

## Current state

This repository is the AI part of MoongCheap. The current MVP is:

1. Consumer Demand Clustering
2. Demand Cluster–Seller Offer Matching
3. Seller Demand Analysis

This working branch implements the A-part data foundation: AI-Hub inspection, observed KAN category handling, product staging/identity resolution, MFDS collection/parsing, and Rule-based Facet Discovery V0. It does not implement Clustering or Seller Matching.

Implementation lives under `src/moongcheap_ai`; domain-owned additions belong under `src/moongcheap_ai/parts/<part_name>` with matching tests under `tests/<part_name>`.

## Source of truth

Read the latest project instructions supplied by the project owner before changing behavior. Do not revive Naver Shopping, GobizKorea, Open Icecat, K-FIND, Domeggook, Consumer RAG, or an AI-owned database.

- Backend and AI share PostgreSQL.
- `category.facet` is TEXT containing JSON; parse it in Python.
- Backend owns original Demand and transaction state.
- Raw data is immutable; never fabricate missing fields.
- Do not add DB migrations without reporting the problem and alternatives first.

## Local paths

```text
data/raw/aihub/logistics_product/  # user-provided AI-Hub files
data/raw/aihub/product_image/      # user-provided AI-Hub files
data/raw/kan/                      # optional official KAN codebook
data/raw/mfds/I0030/
data/raw/mfds/I2710/
```

## Run

```powershell
Copy-Item .env.example .env
$env:MFDS_API_KEY = "..."
./run_data_pipeline.ps1 -Stage all
```

If AI-Hub data is absent, catalog stages must remain `SKIPPED`. Do not create mock data to claim success. MFDS needs `MFDS_API_KEY`; existing raw pages can be reused.

## Important outputs

- `data/interim/products/product_staging.parquet`
- `data/processed/product_catalog/product_catalog_v1.parquet`
- `data/processed/product_catalog/product_catalog_source.csv`
- `data/interim/facet_discovery/i0030_products_clean.parquet`
- `data/interim/facet_discovery/i2710_reference.csv`
- `data/processed/facet_discovery/facet_review_queue.csv`
- `data/processed/facet_discovery/facet_taxonomy_v0.json`
- `data/reports/TODAY_RESULT.md`

Run `pytest -q` after changes. Keep implementation simple: Rule/SQL/Python for clear conditions and numbers, LLM only when a measured experiment justifies it.
