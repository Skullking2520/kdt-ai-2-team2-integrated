# 뭉치 (MoongCheap)

수요 주도형 공동구매 플랫폼 모노레포입니다.

## Repository structure

- `apps/frontend`: Next.js web client
- `apps/backend`: Spring Boot API
- `apps/ai`: FastAPI 기반 AI 서비스
- `infra`: Terraform, Helm, Kubernetes 및 배포 설정
- `docs`: 프로젝트 문서
- `.github`: PR/이슈 템플릿 및 CI 설정

## Development workflow

1. `main`에서 작업 브랜치를 생성합니다.
2. 작은 단위로 커밋합니다.
3. Pull Request를 생성합니다.
4. 작성자가 아닌 팀원 1명의 승인과 CI 통과 후 `main`에 squash merge합니다.

자세한 규칙은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참고하세요.
