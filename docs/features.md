# Features (MoSCoW)

The user story numbers (US-xx) refer to the issues on the project board.

## Must have
- Registration, login and authentication (US-19)
- Roles and user management (US-12)
- Document upload with type, notes and file check (US-01, US-20)
- Applications with several linked documents (US-20, US-03)
- OCR / PDF text extraction and document classification (US-06, US-20)
- Field extraction with the LLM as JSON (US-06)
- RAG knowledge base (US-23, US-21)
- AI verification checks: completeness, validity, consistency, compliance, authenticity (US-07, US-11, US-21)
- Verification report with confidence score and sources (US-21, US-07)
- Reviewer dashboard and queue (US-08)
- Human review: accept, override, correct, request documents (US-09, US-10, US-06)
- Status tracking and notifications for applicants (US-03, US-04)
- Managing document types and rules (US-13)
- Audit log (US-14)
- GDPR: consent, data export, automatic deletion (US-05, US-16)

## Should have
- Check if an upload is readable (blurry, dark, cut off) (US-02)
- AI assistant chat with sources (US-22)
- Prompt management and versions (US-24)
- Analytics dashboard (US-15)

## Could have
- Export report as PDF (US-25)
- Batch upload (US-26)
- English and German (US-18)
- Public REST API (US-17)

## Won't have (in this project)
- Automatic approval without a human, because the reviewer should always decide
- QR-code / digital signature check, because formats are very different
- Checking directly with the universities' databases, because there is no common interface
- Native mobile app, because the web app works on phones
