# Contributing Guide

이 문서는 이 저장소의 모든 개발과 CI/CD 연동에 적용되는 공통 규칙입니다. AI 내부 Directory 구조와 Commit Convention은 기존 AI Convention을 따르되, 아래 공통 규칙은 반드시 준수합니다.

## Repository scope

이 저장소는 생성형 AI 파트의 코드와 문서만 관리합니다.

- 상품 Facet Discovery 및 Demand Labeling
- Demand Clustering
- Seller Offer Matching
- Seller Demand Analysis

Consumer RAG 챗봇, 프론트엔드, 백엔드, 클라우드/인프라 구현은 이 저장소의 MVP 범위에 포함하지 않습니다.

## Branch convention

| Branch | 용도 |
| --- | --- |
| `main` | 최종 검증 및 Demo/Production 배포 기준 |
| `develop` | 개발 통합 및 Dev 환경 배포 기준 |
| `hotfix/*` | 현재 `main` 배포 버전의 긴급 수정 |

일반 작업 Branch(`feat/*`, `fix/*`, `refactor/*` 등)는 기존 AI Convention을 따릅니다.

- `main`, `develop`에 직접 Push하지 않습니다.
- 일반 PR은 Build/Test만 수행하고 Image Build/배포는 수행하지 않습니다.
- `develop` Merge 후 Dev 배포, `main` Merge 후 Demo/Production 배포를 기본으로 합니다.
- `hotfix/* → main` 완료 후 변경사항을 `develop`에도 동기화합니다.

## Pull Requests

- PR 템플릿을 사용합니다.
- 작성자가 아닌 팀원 1명 이상의 승인을 받습니다.
- PR 대상 Branch에 맞는 검증을 통과합니다.
- 모든 리뷰 대화를 해결합니다.
- 하나의 논리적 변경만 포함합니다.
- CI/CD 영향 변경은 클라우드 파트에 공유합니다.
- Merge는 squash merge를 기본으로 합니다.

## CI/CD

```text
GitHub → Jenkins(Build/Test) → Docker Image Build → ECR Push
       → GitOps 배포 정보 변경 → ArgoCD → EKS
```

- `develop` 대상 PR: CI만 수행
- `develop` Merge: CI + Image Build + ECR Push + Dev 배포
- `main` 대상 PR: CI만 수행
- `main` Merge: CI + Image Build + ECR Push + Demo/Production 배포
- `hotfix/* → main`: CI + 긴급 Image Build/배포

## Container, runtime, and secrets

- Image는 `<service-name>:<git-commit-sha>` 형식을 사용합니다. 예: `ai-api:a82f91c`
- `latest`에 의존하지 않으며 Tag 생성/ECR Push는 Jenkins가 담당합니다.
- Build/Test Command, Dockerfile Path, Image Name, Port, Health Check, Metrics Path, Environment/Secret, CPU/Memory/GPU, 외부 의존성을 클라우드 파트에 공유합니다.
- 실제 Password, API Key, Access Key, Token 등 Secret 값은 Git에 Commit하지 않습니다.
- 변경 시 [CI/CD handoff template](docs/ci-cd-application-handoff.template.yml)을 갱신합니다.

## AI-specific rules

- Backend와 동일 PostgreSQL을 사용하며 AI 전용 DB를 만들지 않습니다.
- 상품은 `catalog_id → product_catalog → category → category.facet` 경로로 확인합니다.
- `category.facet`은 TEXT JSON이므로 Python에서 파싱합니다.
- Demand Labeling은 `extra_requirement`를 대상으로 하는 비동기 Batch입니다.
- Cluster는 동일 `catalog_id`를 우선하며 `ALL`/Facet/가격/`is_substitutable` 호환성을 확인합니다.
- V0는 Rule 기반으로 시작하고 Embedding/Hybrid/Weight는 실험 결과로 결정합니다.
- Seller Matching은 `product_award_evaluation`에 재현 가능한 결과를 기록합니다.
- 판매자 분석 수치는 SQL/Python 집계에서 생성하고 LLM은 숫자를 계산하거나 변경하지 않습니다.
- AI는 인증·권한과 거래 상태를 변경하지 않습니다.
- 새로운 테이블·컬럼·상태·모델 서버는 문제와 대안을 먼저 공유한 뒤 결정합니다.
