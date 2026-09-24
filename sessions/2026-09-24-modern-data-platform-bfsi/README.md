# Building a Modern Data Platform for Banking & Financial Services on AWS

- Archive date: 2026-09-24
- Training date: Not recorded
- Source: [SML slides](https://sml-slides.aws.yikyakyuk.com/slides/)
- Scenario: NovaBanco, a fictional retail bank

## Archived materials

| Module | Searchable notes | Original deck data |
| --- | --- | --- |
| 1. Modern Data Architecture Foundations | [Read](slides/module-1.md) | [JSON](source/decks/m1.json) |
| 2. SageMaker Catalog & Lakehouse | [Read](slides/module-2.md) | [JSON](source/decks/m2.json) |
| 3. Data Lake Use Cases for BFSI | [Read](slides/module-3.md) | [JSON](source/decks/m3.json) |
| 4. Wrap-Up, Patterns & Next Steps | [Read](slides/module-4.md) | [JSON](source/decks/m4.json) |
| 5. Redshift & RMS Deep Dive | [Read](slides/module-5.md) | [JSON](source/decks/m5.json) |

Demo guides: [Phase 1 — Foundations](source/docs/phase1.md), [Phase 2 — Open Data Platform](source/docs/phase2.md), [Phase 3 — BFSI Use Cases](source/docs/phase3.md).

The `source/` directory is a snapshot of the public site, including its HTML viewers, images, and narration MP3s. [source-manifest.json](source-manifest.json) records each source file's size and SHA-256. The Markdown slide files are derived from the original JSON for searching and AI review; use the original images and JSON for exact slide content.

The linked hands-on workshop, **Accelerating Financial Analytics: Lakehouse, Amazon SageMaker Unified Studio & Amazon Quick**, opens at [AWS Workshop Studio](https://catalog.us-east-1.prod.workshops.aws/join). The site does not provide a workshop ID or downloadable lab files at that link, so they are not in this snapshot.

To view the archived site locally, run `python3 -m http.server 8000 --directory sessions/2026-09-24-modern-data-platform-bfsi/source` from the repository root, then open `http://localhost:8000/`. The viewer loads public JavaScript/CSS libraries from external CDNs; the archived JSON, Markdown, images, audio, and demo guides remain readable without it.

To refresh this source snapshot, run `python3 scripts/import_sml_slides.py` from the repository root and review the diff before committing.

## Personal review

Add your own observations and follow-up questions to [notes.md](notes.md).
