# DocVerify AI

Senior IT Project (MIT 5.2), Winter Semester 2026/27
Sachin Adihalli Ravigowda

[![CI](https://github.com/SachinAR-21/DocVerify-AI/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/SachinAR-21/DocVerify-AI/actions/workflows/ci.yml)

DocVerify AI is a web platform that helps organisations like universities or employers check documents that applicants upload, for example transcripts, language certificates or ID documents. The idea is that the system reads the documents with OCR and an LLM, checks them against the rules (using RAG) and gives the reviewer a report with the problems it found. The reviewer still makes the final decision.

## Current state (Phase 2)

The core platform works, the AI part comes in Phase 3.

- Registration and login (JWT), password rules, account lock after 5 wrong passwords
- Three roles: Applicant, Reviewer, Admin
- Applicants create applications, upload documents (PDF, JPG, PNG, max 10 MB) with a type and notes, see a checklist of missing documents and submit
- Reviewers have a queue with filters, can start a review and accept, reject or request more documents with a comment
- Admins manage users and roles, document types (required or optional) and can see the audit log and some numbers
- Everything runs in Docker: frontend, backend, PostgreSQL and Qdrant (vector database for Phase 3)

## Tech stack

| Part | Technology |
|---|---|
| Frontend | React 18 + Vite, served by nginx |
| Backend | Python 3.12, FastAPI, SQLAlchemy |
| Database | PostgreSQL 16 |
| Vector database | Qdrant (used from Phase 3) |
| CI | GitHub Actions |

## Getting started

You only need [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
git clone https://github.com/SachinAR-21/DocVerify-AI.git
cd DocVerify-AI
docker compose up --build
```

Then open http://localhost:8080

Demo accounts (created on the first start):

| Role | Email | Password |
|---|---|---|
| Admin | admin@example.com | Admin12345 |
| Reviewer | reviewer@example.com | Review12345 |

Applicants register themselves on the login page.

Other URLs:
- API docs (Swagger): http://localhost:8000/docs
- Health check: http://localhost:8000/api/health
- Qdrant dashboard: http://localhost:6333/dashboard

To change passwords or the secret key, copy `.env.example` to `.env` and edit it before starting. Stop everything with `docker compose down` (add `-v` to also delete the data).

## Development without Docker

Backend (uses SQLite by default):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Frontend (in a second terminal, forwards `/api` to port 8000):

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173

## Tests and linting

```bash
# backend
cd backend
ruff check . && ruff format --check .
pytest

# frontend
cd frontend
npm run lint
npm test
```

The same checks run in GitHub Actions on every push and pull request (see `.github/workflows/ci.yml`). The pipeline also builds all Docker images, starts the system with docker compose and checks that every service answers.

## Project structure

```
backend/     FastAPI app (app/routers = API endpoints, tests = pytest tests)
frontend/    React app (src/pages = pages, src/test = vitest tests)
docs/        Phase 1 product definition and sprint documentation
docker-compose.yml
.github/workflows/ci.yml
```

## How I work

- `main` is protected: changes only go in through pull requests and the CI has to be green
- Every feature gets its own branch (`feature/...`, `docs/...`, `chore/...`)
- Pull requests are linked to the issues on the project board
- Work is planned in sprints, see [docs/sprints](docs/sprints/README.md)

Project board: https://github.com/users/SachinAR-21/projects/1

## Documentation

Phase 1 (product definition):
- [Motivation](docs/motivation.md)
- [Product Vision](docs/vision.md)
- [Personas](docs/personas.md)
- [Scenarios](docs/scenarios.md)
- [Features (MoSCoW)](docs/features.md)
- [Product Definition Document (PDF)](docs/Product_Definition_Document_DocVerify_AI.pdf)

Phase 2 (implementation):
- [Sprint process](docs/sprints/README.md)
- [Sprint 1](docs/sprints/sprint-1.md)
- [Sprint 2](docs/sprints/sprint-2.md)
