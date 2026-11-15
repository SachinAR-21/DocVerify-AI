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

## Sprint review (18.11.2026)

**Sprint goal reached:** yes.

What was done:

- `main` is protected. Changes are only possible with a pull request and green CI checks.
- `docker compose up --build` starts PostgreSQL, Qdrant and the backend. The backend waits until the database is healthy.
- The CI pipeline runs ruff, the pytest tests (against a real PostgreSQL service) and builds and starts the Docker setup, then checks `/api/health`.
- Backend API:
  - register, login, `/me`, password rules, account lock after 5 failed logins (US-19)
  - roles applicant, reviewer, admin; denied access is written to the audit log (US-12)
  - applications, upload with type, notes, file type and size check, checklist of missing required documents, submit (US-01, US-20, US-03)
  - reviewer queue with filters and sorting, start review, accept / reject / request documents with comment (US-08, US-09)
  - admin: users and roles, document types, audit log, statistics (US-12, US-13, US-14)
- 35 backend tests.

Not finished / moved:

- US-19: email confirmation is not done because there is no mail server yet. Moved to later.
- US-12: the extra role "Reviewer (read-only)" from Phase 1 is not done. Moved to later.
- US-01: drag and drop and the camera upload belong to the frontend (Sprint 2). Encrypting the stored files is moved to later.

## Sprint retrospective

**What went well**

- Writing the tests together with the endpoints helped, because every endpoint was checked right away, including the cases where a user is not allowed to do something.
- Because the CI pipeline was set up in the second pull request, every later pull request was checked automatically.

**What did not go well**

- The email validator does not accept `.local` addresses, so the first demo accounts did not work. I changed them to `example.com`.
- The tests take around 40 seconds because bcrypt is slow on purpose. This is okay for now.
- At first the tests only ran against SQLite. Because the real system uses PostgreSQL, I added a PostgreSQL service to the CI job.

**What I will do differently in Sprint 2**

- Keep the pull requests smaller (one page per pull request).
- Test the frontend in the browser with all three roles before merging.
