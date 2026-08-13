# Contributing Guide

## Branches

- `main`: integration and demo-ready branch
- Feature branches: `feat/<short-description>`
- Fix branches: `fix/<short-description>`
- Chore branches: `chore/<short-description>`

Do not push directly to `main`.

## Commits

Use a short Conventional Commits-style prefix:

- `feat`: new functionality
- `fix`: bug fix
- `refactor`: behavior-preserving code change
- `test`: tests
- `docs`: documentation
- `chore`: tooling or configuration

Keep each commit focused and explain the reason when it is not obvious.

## Pull Requests

- Use the PR template.
- Link the related issue when applicable.
- Keep one logical change per PR.
- Add tests or explain why tests are not applicable.
- Request at least one reviewer other than the author.
- Resolve all review conversations before merging.
- PR checks must pass before merging.
- Use squash merge to keep `main` history readable.

## Ownership

Cross-domain changes should request review from the affected team. AI changes should involve the AI part lead; API contract changes should involve backend and the affected consumer.
