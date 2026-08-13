# Contributing Guide

## Scope

이 저장소는 생성형 AI 파트의 코드와 문서만 관리합니다.

- 소비자 자연어 처리 및 LLM 핑퐁
- Demand Schema 변환
- Embedding 및 Hybrid Clustering
- Demand Cluster–Seller Offer Matching / Ranking
- AI 평가와 기술 문서

프론트엔드, 백엔드, 클라우드/인프라의 구현은 이 저장소에 포함하지 않습니다. 다른 파트와의 연동은 문서화된 인터페이스를 기준으로 합니다.

## Branches

- `main`: 통합 가능한 안정 브랜치
- 기능: `feat/<short-description>`
- 수정: `fix/<short-description>`
- 문서/설정: `chore/<short-description>`

`main`에 직접 push하지 않습니다.

## Commits

Conventional Commits 스타일의 접두사를 사용합니다.

- `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

## Pull Requests

- PR 템플릿을 사용합니다.
- 하나의 논리적 변경만 포함합니다.
- 테스트를 추가하거나 테스트하지 못한 이유를 작성합니다.
- 작성자가 아닌 리뷰어 1명 이상을 지정합니다.
- 모든 리뷰 대화를 해결합니다.
- 검증 작업이 통과한 뒤 squash merge합니다.
- 백엔드 연동에 영향을 주는 Schema/API 변경은 PR에 명시하고 관련 담당자에게 공유합니다.

## AI-specific rules

- 백엔드 최종 Schema가 확정되기 전까지 Schema 의존 코드를 어댑터 뒤에 둡니다.
- 초기 구현은 weight에 의존하지 않습니다.
- LLM에게 최종 Seller를 직접 선택시키지 않습니다.
- 정형 조건은 hard constraint와 soft preference를 구분할 수 있게 설계합니다.
- 모델, Vector DB, Embedding 표현은 교체 가능하게 유지합니다.
- 프롬프트, 평가 데이터, 실험 결과를 재현 가능하게 기록합니다.
