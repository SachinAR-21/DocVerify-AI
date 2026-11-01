# DocVerify AI – AI-Powered Document Verification System

**MIT 5.2 – Senior IT Project** · Winter Semester 2026/27 · Lecturer: Dr. Ali Alhosseini  
**Student:** Sachin Adihalli Ravigowda (111121997)

DocVerify AI is a web-based platform that helps universities, employers, public offices, banks and landlords verify the authenticity, completeness and consistency of documents submitted by applicants. It uses OCR, Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to extract data, check it against official rules and produce an explainable verification report. A human reviewer always makes the final decision.

## Project links

- 📄 **Product Definition Document (Phase 1):** [docs/Product_Definition_Document_DocVerify_AI.pdf](docs/Product_Definition_Document_DocVerify_AI.pdf)
- 📋 **Product Backlog (GitHub Project):** https://github.com/users/SachinAR-21/projects/1

## 1. Motivation

Document checks are still mostly done by hand. Reviewers open each file, compare it with rule sheets and the application form, and make a decision. This is:

- **Slow:** 15–25 minutes per application, which leads to long backlogs in peak season.
- **Error-prone and inconsistent:** tired reviewers miss mismatched names, expired certificates or edited grades, and different reviewers apply rules differently.
- **Risky:** manipulated documents are easy to create, and documents shared by email are a GDPR problem.
- **Frustrating:** applicants get no status updates and learn about problems weeks later.

AI is a good fit because the work is mostly reading, comparing and checking against rules: OCR reads the documents, LLMs extract structured fields, RAG checks them against the organisation's own rules with citations, and automated checks find inconsistencies and signs of manipulation. The reviewer stays in control.

## 2. Product Vision

> For **universities, employers, public offices, banks and landlords** who **need to verify large numbers of applicant documents quickly, reliably and in a GDPR-compliant way**, DocVerify AI is an **AI-powered document verification platform** that **automatically extracts, cross-checks and verifies documents against official rules and produces an explainable report, so that reviewers can make confident decisions in minutes instead of hours**. Unlike **manual checking via email and shared folders or generic OCR tools**, our product **explains every finding with citations to the rules it used, keeps a human in control of every decision, and gives applicants instant feedback on their uploads**.

## 3. Personas

| Persona | Role | Goals | Frustrations | Technical skills |
|---|---|---|---|---|
| **Priya Raman**, 26 | Applicant / Submitter – international student applying for a Master's in Germany | Submit a complete application on time, get instant feedback, track status | Late rejections for unreadable files, no status updates, unclear reasons | Comfortable with smartphones and web apps, not with PDF tools |
| **Jana Becker**, 41 | Reviewer / Verifier – admissions officer, 50–70 applications a day | Clear her queue without overtime, focus on suspicious cases, justify decisions with rules | Switching between many tools, bad scans, hard-to-spot forgeries, black-box tools | Confident office user, not technical |
| **Tobias Klein**, 34 | Administrator – IT admin for student services | Control roles, keep rules and knowledge base current, full audit trail, GDPR compliance | No proper roles, outdated rule PDFs, scattered personal data | High: user management, APIs, logs, GDPR, basic LLM knowledge |

## 4. Scenarios

- **Priya** registers, creates an application, photographs her degree certificate and gets instant feedback that the photo is too dark. She retakes it, adds her transcripts and IELTS certificate with a note, and later replaces only the one document the reviewer asked for. Her status changes to *Verified*.
- **Jana** opens 63 applications already processed by the AI. She accepts the clearly *Verified* ones quickly, confirms a *Rejected* transcript where the report highlights mismatched fonts and wrong totals, and asks the AI assistant whether an applicant meets the language requirement. The answer cites the admission rules, and she overrides the result with a justification.
- **Tobias** uploads updated admission rules to the knowledge base, archives the old version, adds a new document type and gives student assistants read-only reviewer access. When the data protection officer asks about an application, he exports the audit log showing who accessed it, which prompt version and sources were used, and who made the decision.

## 5. User Stories

All 26 user stories, each with acceptance criteria and a MoSCoW priority, are managed as GitHub issues on the [project board](https://github.com/users/SachinAR-21/projects/1).

## 6. Features (MoSCoW) and mapping to user stories

| ID | Feature | Priority | User stories |
|---|---|---|---|
| F-01 | User registration, login and authentication | Must | US-19 |
| F-02 | Role-based access control and user management | Must | US-12 |
| F-03 | Document upload with type selection, notes and file validation | Must | US-01, US-20 |
| F-04 | Application management (linking several documents) | Must | US-20, US-03 |
| F-05 | OCR / PDF text extraction and document classification | Must | US-06, US-20 |
| F-06 | LLM-based structured field extraction (JSON) | Must | US-06 |
| F-07 | RAG knowledge base (ingestion, embeddings, retrieval) | Must | US-23, US-21 |
| F-08 | AI verification checks (completeness, validity, consistency, compliance, authenticity) | Must | US-07, US-11, US-21 |
| F-09 | Explainable verification report with confidence and citations | Must | US-21, US-07 |
| F-10 | Reviewer dashboard and work queue | Must | US-08 |
| F-11 | Human review: accept, override, correct, request documents | Must | US-09, US-10, US-06 |
| F-12 | Applicant status tracking and notifications | Must | US-03, US-04 |
| F-13 | Document types and verification rule management | Must | US-13 |
| F-14 | Audit log and AI traceability | Must | US-14 |
| F-15 | GDPR consent, data export and retention rules | Must | US-05, US-16 |
| F-16 | Upload readability check (blur, lighting, cropping) | Should | US-02 |
| F-17 | AI assistant chat with cited answers | Should | US-22 |
| F-18 | Prompt management and versioning | Should | US-24 |
| F-19 | Analytics dashboard (volume, accuracy, time, override rate) | Should | US-15 |
| F-20 | Export of verification reports as PDF | Could | US-25 |
| F-21 | Batch upload and bulk verification | Could | US-26 |
| F-22 | Multi-language interface and documents (EN/DE) | Could | US-18 |
| F-23 | Public REST API for third-party integration | Could | US-17 |
| F-24 | Fully automatic approval without human review | Won't | – |
| F-25 | QR-code / digital signature verification | Won't | – |
| F-26 | Live verification with issuing institutions' databases | Won't | – |
| F-27 | Native iOS / Android app | Won't | – |

**Won't (this project):** fully automatic approval (the AI never decides alone), QR-code/digital signature verification, live verification with issuing institutions, native mobile apps.
