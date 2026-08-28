# 오늘 결과

실제 외부 API Key가 제공된 뒤 `run_today_pipeline.ps1`을 실행합니다.

## 현재 구현

- Naver raw collector와 pagination 제한
- MFDS I0030/I2710 raw collector
- Naver title 정규화 및 productId dedup/conflict 기록
- Category/Product Catalog seed 생성
- MFDS Product Fact/Reference 최소 표준화
- repeated terms와 structured value distribution
- Rule 기반 Facet Taxonomy V0 초안 및 Human Review queue
- 재실행 가능한 report 출력

## 미실행 사유

- 현재 환경에 `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET`, `MFDS_API_KEY`가 없습니다.
- 따라서 실제 row count는 아직 기록하지 않았습니다.

## 다음 확인 항목

- MFDS 실제 응답 필드명과 표준 컬럼 매핑
- 건강기능식품 Pilot Category 선정
- Facet 후보 Human Review
- Naver Category와 MFDS Category 수준 Mapping
