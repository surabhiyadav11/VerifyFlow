VerifyFlow: Product Requirements Document (v1)
1. Overview

VerifyFlow is an AI-powered document verification and review platform. Users upload documents, the system extracts key information, checks required fields and supporting documents, and produces an understandable report of potential issues.

VerifyFlow is one platform. It supports two document types: Invoices and KYC documents. The upload, extraction, and report pipeline is shared. Only the validation rules differ per document type.

2. Problem Statement

Manual checking of invoices and KYC documents is slow and error-prone. Common mistakes such as wrong totals, missing GSTIN, mismatched names, or expired IDs are easily missed.

3. Target Users
Small businesses and accountants (invoice checking)
Onboarding and compliance teams (KYC checking)
4. Goals
Reduce time spent on manual document review
Catch missing fields, mismatches, and invalid data automatically
Explain issues in plain language with suggested fixes
5. Non-Goals (for now)
Forgery or tampering detection
Official government API verification (e.g. live PAN/Aadhaar validation)
Payments
Mobile app
6. Features
6.1 Must-have (MVP)

Shared pipeline

Select document type (Invoice / KYC)
Upload PDF or image
OCR and AI-based field extraction
Rule-based validation
Report with issues, severity, and suggested fix

Invoice checks

Extract: invoice number, date, vendor, GSTIN, line items, tax, total
Required fields present
Line items sum to total
Tax calculation correct
GSTIN format valid
Duplicate invoice number
Date sanity check

KYC checks

Documents: PAN, Aadhaar, address proof, photo/selfie
Extract: name, DOB, ID number, address, expiry
Required documents present
ID number format valid
Name and DOB match across documents
Document not expired
Image is readable

Report

Issue list with severity (High / Medium / Low), reason, and suggested fix
Overall status: Pass / Needs review / Fail
6.2 Nice-to-have
User login and authentication
History of past checks
PDF export of the report
Dashboard
Batch upload
Human review queue
7. User Flow

Upload > Extract > Review/Edit > Validate > Report

User opens VerifyFlow and chooses document type (Invoice or KYC)
User uploads the document(s). For KYC, user labels each file with a dropdown (PAN / Aadhaar / Address proof / Passport / Driving licence / Selfie)
System extracts data (OCR + AI). The raw file is deleted right after extraction
User reviews the extracted values and edits any that are wrong
System runs validation rules for that document type
User views the report
User edits values and re-runs the checks, or re-uploads if needed
8. Tech Stack
Frontend: React.js
Backend: FastAPI (Python)
Database: PostgreSQL
OCR: Tesseract or PaddleOCR
AI: LLM API for extraction and plain-language explanations
Validation: rules written as plain Python code (not LLM guesses) for consistent results
9. Success Criteria
Extracts key fields correctly on 90%+ of sample documents
Catches all deliberately planted errors in test files
Report is understandable to a non-technical person
10. Risks and Privacy
KYC data is sensitive. Use only fake/sample documents during development.
Mask ID numbers in the UI (e.g. XXXX-XXXX-1234).
Do not store raw uploaded files longer than needed.
OCR and AI extraction can be wrong, so show extracted values to the user for confirmation.
11. Build Phases
Idea and problem (done)
PRD (this document)
Design: database schema, API endpoints, folder structure, rule list
Setup: GitHub repo, frontend and backend init, README, PRD in /docs
Build MVP: shared pipeline, then Invoice module, then KYC module
Testing and fixes
Deploy and document
12. Decisions

Review/Edit: Users can edit extracted values and re-run the checks.

Duplicate invoices: Compare against all invoices already saved in the database (match on invoice number + vendor GSTIN), and also within the same upload. No login in MVP.

Storage: Store extracted fields only, never raw files. Delete the raw file right after extraction. ID numbers are stored masked.

KYC case: One KYC case contains multiple files. The user labels each file with a dropdown (PAN / Aadhaar / Address proof / Passport / Driving licence / Selfie).

Selfie: Readability check only. No face matching (non-goal).

Expiry: No expiry check for PAN or Aadhaar. Address proof (utility bill) must be dated within the last 3 months. Passport and driving licence must not be expired, if uploaded.

Tax: Support both CGST+SGST (intra-state) and IGST (inter-state). Rounding tolerance is ±Rs 1.

Date checks: Invoice date in the future = High. Invoice date older than 1 year = Low. Due date before invoice date = Medium.

Overall status: Any High issue = Fail. No High but at least one Medium = Needs review. Only Low or no issues = Pass.

Name matching: Fuzzy (ignore case, handle initials and word order). Clear match = pass, partial match = Medium, mismatch = High.

LLM: Gemini API by default (or whichever provider has a key), kept behind one interface so it is swappable. A cloud API is acceptable because only fake data is used in development.

OCR: Tesseract only for the MVP. PaddleOCR comparison is deferred until after the MVP (the OCR interface stays swappable).

Deployment: Run locally for now. Later: backend on Railway/Render, frontend on Vercel, and add Docker. Authentication is required before any public deployment.

Test data: Generate synthetic fake invoices and KYC documents with planted errors. Never use real documents.

Address proof: Always required for the MVP. Accepting Aadhaar as an alternative comes later.

Address match: Skipped for the MVP. Add later as a Low rule.

GST rates: Configurable and dependent on the invoice date (rates changed in September 2025). Verify the slabs against CBIC notifications, not memory or the LLM.

Extraction: Synchronous, one request per file, with a per-file progress indicator on the frontend.

Retention: Keep invoice fields (needed for duplicate detection). Auto-delete KYC checks after a configurable number of days (default 7).

Privacy: ID numbers are found with local regex and redacted before any text is sent to the LLM.