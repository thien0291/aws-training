# AWS Personal Training Archive

Private, session-based archive of AWS training materials for later review with AI.

## Sessions

| Session | Material |
| --- | --- |
| [Modern Data Platform for Banking & Financial Services](sessions/2026-09-24-modern-data-platform-bfsi/README.md) | Five slide modules, three demo guides, slide images, narration, and [12 workshop lessons with 81 images](sessions/2026-09-24-modern-data-platform-bfsi/workshop/README.md) |

The date in a directory name is the **archive date** unless its README says otherwise. It does not imply the training took place on that date.

## Certification review

The [certification guide](certs/README.md) ranks the AWS certifications that fit the archived session and links each exam to selected training sections, flashcards, cheat sheets, original practice questions, and official AWS practice resources.

## Add a training

Run `python3 scripts/new_session.py "Training title"` to create a dated session directory. Add the original files under `source/`, list all source URLs in `README.md`, and put personal notes in `notes.md`. Keep one training event per directory. When a source is a website, preserve the original files where practical and add searchable Markdown or text alongside them.

Review materials before committing. Do not commit AWS keys, account IDs you consider private, passwords, signed URLs, session cookies, or personal data from labs. Use `.env` locally for any credentials.

This repository is for personal study. Each training source retains its own rights and attribution.
