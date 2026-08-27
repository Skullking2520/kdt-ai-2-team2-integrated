# Contributing Guide

이 문서는 이 저장소의 모든 개발과 CI/CD 연동에 적용되는 공통 규칙입니다. AI 내부 Directory 구조와 Commit Convention은 기존 AI Convention을 따르되, 아래 브랜치·PR·빌드·런타임 규칙은 반드시 준수합니다.

## Repository scope

이 저장소는 생성형 AI 파트의 코드와 문서만 관리합니다.

- 소비자 수요 Embedding 및 Vector DB 기반 Cluster 생성
- 필요 시 정형 조건을 결합한 Hybrid Clustering
- Demand Cluster–Seller Offer 후보 탐색, Filtering, Scoring, Ranking
- 판매자용 소비자 수요 분석
- 매칭 후 판매자 제공 정보 기반 RAG 챗봇
- AI 평가와 기술 문서

프론트엔드, 백엔드, 클라우드/인프라 구현은 이 저장소에 포함하지 않습니다.

## Branch convention

| Branch | 용도 |
| --- | --- |
| `main` | 최종 검증 및 Demo/Production 배포 기준 |
| `develop` | 개발 통합 및 Dev 환경 배포 기준 |
| `hotfix/*` | 현재 `main` 배포 버전의 긴급 수정 |

일반 작업 Branch(`feat/*`, `fix/*`, `refactor/*` 등)는 기존 AI Convention을 따릅니다.

### 일반 흐름

```text
작업 Branch → PR → develop → CI/CD → Dev 검증
                                  ↓
                                main → CI/CD → Demo/Production
```

- `main`, `develop`에 직접 Push하지 않습니다.
- 일반 PR은 Build/Test만 수행하고 Image Build/배포는 수행하지 않습니다.
- `develop` Merge 후 Dev 배포, `main` Merge 후 Demo/Production 배포를 기본으로 합니다.
- 실제 자동 배포 범위는 클라우드 파트와 협의하여 확정합니다.

### Hotfix

``main``에서 ``hotfix/<short-description>``를 생성하여 수정하고 PR로 ``main``에 반영합니다. 긴급 배포 후 동일 변경사항을 ``develop``에도 반드시 동기화합니다.

## Pull Requests

- PR 템플릿을 사용합니다.
- 작성자가 아닌 팀원 1명 이상의 승인을 받습니다.
- PR 대상 Branch에 맞는 검증을 통과합니다.
- 모든 리뷰 대화를 해결합니다.
- 하나의 논리적 변경만 포함합니다.
- CI/CD 연동에 영향을 주는 변경은 PR에 영향 범위를 명시합니다.
- Merge는 squash merge를 기본으로 합니다.

## Commits

Commit Convention은 기존 AI 파트 Convention을 따릅니다. CI/CD 설정이나 공통 문서 변경도 의미가 드러나는 Commit Message를 사용합니다.

## CI/CD

기본 흐름은 다음과 같습니다.

```text
GitHub → Jenkins(Build/Test) → Docker Image Build → ECR Push
       → GitOps 배포 정보 변경 → ArgoCD → EKS
```

- `develop` 대상 PR: CI만 수행
- `develop` Merge: CI + Image Build + ECR Push + Dev 배포
- `main` 대상 PR: CI만 수행
- `main` Merge: CI + Image Build + ECR Push + Demo/Production 배포
- `hotfix/* → main`: CI + 긴급 Image Build/배포

## Container image

Application별 Image Name을 클라우드 파트와 사전에 공유합니다.

```text
<service-name>:<git-commit-sha>
```

예: `ai-api:a82f91c`

Image Tag는 Git Commit SHA를 기본으로 사용합니다. `latest` Tag에만 의존하지 않으며, Tag 생성과 ECR Push는 Jenkins가 처리합니다.

## Environment variables and secrets

- 필요한 환경변수의 이름과 용도를 클라우드 파트에 공유합니다.
- 가능하면 `.env.example` 또는 CI/CD handoff 문서로 목록을 관리합니다.
- 실제 Password, API Key, Access Key, Token 등 Secret 값은 Git에 Commit하지 않습니다.
- Secret 저장 및 주입 방식은 클라우드/보안 파트와 협의합니다.

## CI/CD handoff information

최초 Pipeline 구축 전 또는 아래 항목이 변경될 때 [handoff template](docs/ci-cd-application-handoff.template.yml)을 갱신하고 클라우드 파트에 공유합니다.

- Repository / Branch
- Build / Test Command
- Dockerfile Path
- Container Image Name
- Application Port
- Health Check Path
- Metrics Path
- Environment Variables / Secret Variables
- CPU / Memory / GPU 요구사항
- DB, Redis, AI API 등 외부 의존성

## AI-specific rules

- AI 기능 기준 순서는 Cluster 생성 → 판매자 매칭 → 판매자용 수요 분석 → 매칭 후 소비자 RAG 챗봇입니다.
- Consumer/Seller Schema는 백엔드 계약을 따릅니다.
- 중요도/가중치는 성능 개선이 확인될 때만 도입합니다.
- 최종 판매자 매칭을 LLM의 임의 판단에 맡기지 않습니다.
- 수요 분석의 수치와 사실은 실제 데이터 집계 결과에서 산출합니다.
- RAG 지식 소스는 해당 판매자가 제공한 정보로 제한합니다.
- 근거가 부족하거나 판매자 정보에 없는 내용은 추론하지 않고 Abstention 처리합니다.
- 모델, Vector DB, Embedding 표현, Ranking 공식은 교체 가능하게 유지합니다.
