# 뭉치 AI (MoongCheap AI)

수요 주도형 공동구매 플랫폼의 AI 파트 저장소입니다.

## Repository structure

- `apps/ai`: FastAPI 기반 AI 서비스
  - 소비자 자연어 처리 및 LLM 핑퐁
  - Demand Embedding 및 유사 수요 탐색
  - Hybrid Demand Clustering
  - Demand Cluster–Seller Offer Matching / Ranking
- `docs`: AI 기술 문서, 평가 기준, 인터페이스 문서
- `.github`: PR/이슈 템플릿 및 협업 설정

프론트엔드, 백엔드, 클라우드/인프라는 각 담당 파트에서 관리합니다.

## Development workflow

1. `main`에서 작업 브랜치를 생성합니다.
2. 작은 단위로 커밋합니다.
3. Pull Request를 생성합니다.
4. 작성자가 아닌 팀원 1명의 승인과 검증 통과 후 `main`에 squash merge합니다.

자세한 규칙은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참고하세요.
