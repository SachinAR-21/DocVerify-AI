# Sprint process

For Phase 2 I use a light version of Scrum with two short sprints. Because I work alone on this project, I am product owner, developer and reviewer at the same time, so the meetings are short notes that I write at the start and the end of each sprint.

## Tools

- **GitHub Project board** (https://github.com/users/SachinAR-21/projects/1) with the columns *Todo*, *In Progress* and *Done*. The board is used like a Kanban board during the sprint.
- **Milestones** "Sprint 1" and "Sprint 2" in the repository. Every issue that is planned for a sprint gets the milestone, so it is easy to see the sprint backlog.
- **Issues** for user stories (US-01 to US-26 from Phase 1) and for technical tasks (labelled `task`).
- **Pull requests**: every change goes through a pull request that is linked to its issue with `Closes #..` (story is finished) or `Refs #..` (story is only partly done in this PR).

## Workflow for one issue

1. Move the issue to *In Progress*.
2. Create a branch from `main`, for example `feature/document-upload`.
3. Make small commits with clear messages (what was changed, in present tense).
4. Push the branch and open a pull request with a short description and the linked issue.
5. Wait for the CI pipeline (lint, tests, Docker build). It must be green.
6. Review my own changes in the "Files changed" tab, then merge and delete the branch.
7. The issue moves to *Done* automatically when it is closed by the pull request.

## Definition of Done

A story or task is done when:

- the acceptance criteria that belong to this phase are met
- the code is in `main` through a pull request
- linting and all tests pass in GitHub Actions
- new backend endpoints have tests
- the system still starts with `docker compose up`
- the README is updated if something changed for the setup

## Sprints

| Sprint | Dates | Goal |
|---|---|---|
| [Sprint 1](sprint-1.md) | 15.11. - 18.11.2026 | Project setup, Docker, CI and the complete backend API |
| [Sprint 2](sprint-2.md) | 19.11. - 22.11.2026 | Frontend for all three roles and documentation |
