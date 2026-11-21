# Sprint 2

**Dates:** 19.11. - 22.11.2026
**Milestone:** Sprint 2

## Sprint planning

**Sprint goal:** Build the frontend for applicants, reviewers and admins, add it to Docker and the CI pipeline, and finish the documentation for Phase 2.

Decisions made in the planning:

- **React with Vite**, because it is fast to set up and I already know React a bit.
- The built frontend is served by **nginx**. nginx also forwards `/api` to the backend, so the browser only talks to one address and there are no CORS problems.
- Tests with **Vitest** and **Testing Library**, linting with **ESLint**.
- No UI library, just one CSS file, to keep it simple.

## Sprint backlog

| Issue | Title | Type | Planned result |
|---|---|---|---|
| #28 | Docker setup for all services | task | add the frontend container |
| #30 | Sprint documentation for Phase 2 | task | done |
| #19 | US-19 Register and log in | story | login and register pages |
| #1 | US-01 Upload documents | story | upload page |
| #20 | US-20 Document type, notes, several documents per application | story | upload page |
| #3 | US-03 Status of documents | story | status and checklist |
| #8 | US-08 Reviewer work queue | story | queue page |
| #9 | US-09 Accept, reject or request documents | story | review page |
| #12 | US-12 Users and roles | story | admin page |
| #13 | US-13 Document types and rules | story | admin page |
| #14 | US-14 Audit log | story | admin page |

## Pull requests (planned order)

1. `feature/frontend-setup` - React app, login, register, applicant pages, nginx container, CI job
2. `feature/reviewer-dashboard` - review queue and review page
3. `feature/admin-pages` - users, document types, audit log, overview
4. `docs/readme-and-sprint-2` - README with setup steps, sprint review and retrospective
