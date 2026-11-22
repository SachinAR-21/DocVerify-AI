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

## Sprint review (22.11.2026)

**Sprint goal reached:** yes.

What was done:

- Login and register pages. After login every role lands on its own start page.
- Applicant: list of applications, new application, upload with document type, notes and file check in the browser, checklist of missing documents, submit, status badges, message from the reviewer (US-01, US-03, US-19, US-20).
- Reviewer: queue with status and programme filter, sorting and "only mine", review page with documents, notes, history and the decision form (US-08, US-09).
- Admin: overview numbers, user list with role change and deactivate, create staff accounts, document types (required / active), audit log with filter (US-12, US-13, US-14).
- The frontend runs in its own nginx container. `docker compose up --build` now starts all four services: frontend, backend, PostgreSQL and Qdrant.
- The CI pipeline has a frontend job (ESLint, Vitest, build) and checks that the frontend and the `/api` forwarding work in the Docker setup.
- README with setup steps, demo accounts and the workflow.

Not finished / moved to the next phases:

- The AI verification report (Phase 3). The review page already has a place for it.
- Drag and drop and camera upload (US-01), CSV export of the audit log (US-14), extra read-only reviewer role (US-12), fields to extract per document type (US-13).
- Email notifications (US-04) and email confirmation (US-19).

## Sprint retrospective

**What went well**

- Because the API was finished in Sprint 1, the frontend was mostly just calling the endpoints.
- One small pull request per page was easier to check than one big one.
- Testing the whole flow (applicant uploads -> reviewer requests a document -> applicant sees the message) showed that the status changes work together.

**What did not go well**

- The reviewer and admin start pages did not exist yet in the first frontend pull request, so I needed placeholder pages to avoid broken links.
- In the first browser test the user name and the logout button in the top bar were stuck together, which needed a small CSS fix.
- I had to learn how nginx forwards requests to another container.

**For the next phase**

- Plan the AI service as a separate module in the backend, so it can be tested on its own.
- Create the synthetic test documents early, because they are needed for the evaluation in Phase 4.

## Individual contribution log

This is an individual project. I planned the sprints, selected the technologies, set up and operated the system with Docker, tested all features and managed the GitHub workflow (issues, pull requests, CI pipeline and project board). An AI assistant was used as a supporting tool where I faced difficulties and documentation. All results were reviewed and tested by me before being merged.

| Date | Work |
|---|---|
| 15.11.2026 | Project setup, sprint planning, branch protection |
| 15.11.2026 | Backend skeleton, Dockerfile, docker compose, CI pipeline |
| 16.11.2026 | Registration, login, roles, audit log + tests |
| 17.11.2026 | Applications and document upload + tests |
| 18.11.2026 | Reviewer and admin API + tests, sprint 1 review |
| 19.11.2026 | Frontend setup, login, register, applicant pages, nginx container |
| 20.11.2026 | Reviewer dashboard |
| 21.11.2026 | Admin pages |
| 22.11.2026 | README, sprint 2 review and retrospective |
