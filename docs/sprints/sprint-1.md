# Sprint 1

**Dates:** 15.11. - 18.11.2026
**Milestone:** Sprint 1

## Sprint planning

**Sprint goal:** Set up a professional development workflow (branches, protected main, CI, Docker) and build the backend API for the core features, so that the frontend can be built on top of it in Sprint 2.

Decisions made in the planning:

- Backend with **FastAPI** (Python), because the AI part in Phase 3 will also be in Python.
- **PostgreSQL** as database and **Qdrant** as vector database. Qdrant is only started in this phase, it will be used for RAG in Phase 3.
- Login with **JWT tokens**, passwords hashed with **bcrypt**.
- Uploaded files are stored on a Docker volume, the information about them in the database.
- Tests with **pytest**, linting with **ruff**.
- Backend first, frontend in Sprint 2.

## Sprint backlog

| Issue | Title | Type | Planned result |
|---|---|---|---|
| #27 | Set up Git workflow and protect the main branch | task | done |
| #28 | Docker setup for all services | task | backend, PostgreSQL, Qdrant (frontend follows in Sprint 2) |
| #29 | GitHub Actions CI pipeline | task | done |
| #19 | US-19 Register and log in | story | backend part |
| #12 | US-12 Users and roles | story | backend part |
| #1 | US-01 Upload documents | story | backend part |
| #20 | US-20 Document type, notes, several documents per application | story | backend part |
| #3 | US-03 Status of documents | story | backend part |
| #8 | US-08 Reviewer work queue | story | backend part |
| #9 | US-09 Accept, reject or request documents | story | backend part |
| #13 | US-13 Document types and rules | story | backend part |
| #14 | US-14 Audit log | story | backend part |

## Pull requests (planned order)

1. `chore/project-setup` - .gitignore, example environment file, sprint documentation
2. `feature/docker-and-ci` - backend skeleton, Dockerfile, docker compose, CI pipeline
3. `feature/auth-and-roles` - registration, login, roles, audit log
4. `feature/document-upload` - applications and document upload
5. `feature/review-and-admin-api` - reviewer queue, decisions, admin endpoints
6. `docs/sprint-1-review` - sprint review and retrospective
