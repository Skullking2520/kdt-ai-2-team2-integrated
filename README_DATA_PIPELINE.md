# A 담당 Data / Facet Discovery V0

이 파이프라인은 다음 두 데이터 흐름을 분리합니다.

- Naver Shopping Search API: 전체 전자상거래 Category/Product Catalog seed
- 식품안전나라 MFDS I0030/I2710: 건강기능식품 Product Fact와 Category/Reference

Naver 상품과 MFDS 상품을 Product ID로 직접 Join하지 않습니다. V0에서는 Category 수준 연결만 후속 단계에서 검토합니다.

## 실행

```powershell
Copy-Item .env.example .env
$env:NAVER_CLIENT_ID = "..."
$env:NAVER_CLIENT_SECRET = "..."
$env:MFDS_API_KEY = "..."
./run_today_pipeline.ps1
```

API Key가 없으면 수집 단계는 명확한 오류로 중단하며, 가짜 데이터로 성공 처리하지 않습니다. 외부 API 없이 기존 raw 파일만 처리하려면:

```powershell
$env:PYTHONPATH = "$PWD/src"
python -m moongcheap_ai.pipeline --root $PWD --no-collect
```

Raw 응답은 `data/raw`에 보존하고, CSV는 Excel 호환을 위해 UTF-8-SIG로 출력합니다. `product_catalog`의 `list_price`는 Naver 최저가와 의미가 다르므로 기본적으로 비워 둡니다.

## 주요 산출물

- `data/interim/catalog/naver_products_staging.csv`
- `data/processed/db_seed/category_seed.csv`
- `data/processed/db_seed/product_catalog_seed.csv`
- `data/interim/facet_discovery/i0030_products_clean.csv`
- `data/interim/facet_discovery/i2710_reference.csv`
- `data/interim/facet_discovery/repeated_terms.csv`
- `data/interim/facet_discovery/structured_value_distribution.csv`
- `data/processed/facet_discovery/facet_review_queue.csv`
- `data/processed/facet_discovery/facet_taxonomy_v0.json`
- `data/reports/*.json`

Taxonomy는 Human Review 전 초안이며 `category.facet` DB 반영은 이 파이프라인에서 수행하지 않습니다.
