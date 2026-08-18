# Contributing Guide

## Scope

이 저장소는 생성형 AI 파트의 코드와 문서만 관리합니다.

- 소비자 수요 Embedding 및 Vector DB 기반 Cluster 생성
- 필요 시 정형 조건을 결합한 Hybrid Clustering
- Demand Cluster–Seller Offer 후보 탐색, Filtering, Scoring, Ranking
- 판매자용 소비자 수요 분석
- 매칭 후 판매자 제공 정보 기반 RAG 챗봇
- AI 평가와 기술 문서

소비자/판매자 자연어 처리 및 LLM 핑퐁은 현재 핵심 범위가 아닙니다. 프론트엔드, 백엔드, 클라우드/인프라 구현은 이 저장소에 포함하지 않습니다.

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
- 테스트와 데이터 근거를 추가하거나, 불가능한 이유를 작성합니다.
- 작성자가 아닌 리뷰어 1명 이상을 지정합니다.
- 모든 리뷰 대화를 해결합니다.
- 검증 작업이 통과한 뒤 squash merge합니다.
- 백엔드 Schema/API 계약 변경은 PR에 명시하고 관련 담당자에게 공유합니다.

## AI-specific rules

- AI 구현의 기준 순서는 Cluster 생성 → 판매자 매칭 → 판매자용 수요 분석 → 매칭 후 소비자 RAG 챗봇입니다.
- Consumer/Seller Schema는 백엔드 계약을 따르며, Schema 의존 코드는 교체 가능한 어댑터 뒤에 둡니다.
- 중요도/가중치는 필수가 아니며 성능 개선이 확인될 때만 도입합니다.
- LLM에게 최종 판매자를 임의로 선택시키지 않습니다.
- 수요 분석의 수치와 사실은 실제 데이터 집계 결과에서 산출합니다.
- RAG 챗봇의 지식 소스는 해당 판매자가 제공한 정보로 제한합니다.
- 근거가 부족하거나 판매자 정보에 없는 내용은 추론하지 않고 확인 불가로 응답합니다.
- 모델, Vector DB, Embedding 표현, Ranking 공식은 실험 결과에 따라 교체 가능하게 유지합니다.
- 평가 데이터와 실험 결과를 재현 가능하게 기록합니다.
