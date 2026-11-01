# Motivation

Right now most document checks are done by hand. Someone in the admissions office opens every PDF, compares it with the application form and the rules, and decides if it is okay. This has a few problems:

- It takes a lot of time. One application with 4-5 documents can take around 15-25 minutes, and in application season there are thousands.
- Mistakes happen. After checking documents the whole day it is easy to miss a wrong date of birth, an expired certificate or a changed grade. Also different reviewers do not always apply the rules the same way.
- Fake documents are easy to make with normal editing tools and they are hard to see with the eye.
- Documents are often sent by email or kept in shared folders, which is not good for data protection (GDPR).
- Applicants don't know the status of their application and sometimes only find out after weeks that a scan was unreadable.

## Why AI?

Most of this work is reading and comparing, which AI can do well:

- OCR can read scanned documents and photos.
- An LLM can find the important fields (name, date of birth, grades, ...) even if every university uses a different layout.
- With RAG the system can check the data against the official rules and show which rule it used.
- It can compare all documents of one application and find inconsistencies or signs of manipulation.

The AI should only help the reviewer and not decide alone, because these decisions are important for people.
