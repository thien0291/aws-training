# Accelerating Financial Analytics workshop

Captured 2026-09-24 from [AWS Workshop Studio](https://catalog.us-east-1.prod.workshops.aws/event/dashboard/en-US/workshop) during the 16-hour event. This is a private, static study snapshot of the workshop instructions.

## Lessons

- [Accelerating Financial Analytics: Lakehouse, Amazon SageMaker Unified Studio & Amazon Quick](pages/00-overview.md)
- [00. Join Workshop Event](pages/01-join-workshop-event.md)
- [01. User administration & set up](pages/02-user-administration-and-setup.md)
- [02. Create catalogs and connections](pages/03-create-catalogs-and-connections.md)
- [03. Create a zero-ETL integration](pages/04-create-zero-etl-integration.md)
- [04. Federated Data Query](pages/05-federated-data-query.md)
- [05. Zero-ETL Query](pages/06-zero-etl-query.md)
- [06. Natural Language Data Analysis with Amazon Quick](pages/07-amazon-quick.md)
  - [6.1. Perform Dashboard Q&A in Quick Sight](pages/07-01-dashboard-qa.md)
  - [6.2. Create and use Quick Suite Spaces with default chat agent](pages/07-02-default-chat-agent.md)
  - [6.3 Build a personalized Risk Assessment Chat agents (Optional)](pages/07-03-personalized-chat-agent.md)
- [Workshop Summary](pages/08-workshop-summary.md)

## Source files

- [Original Workshop Studio manifest](source/manifest.json) and [metadata](source/metadata.json)
- [Original instruction pages](source/content/), unchanged from the served Markdown
- [Images and diagrams](source/static/images/) (81 files)
- [Lab 05 permissions quick fix](source/static/LAB05_PERMISSIONS_QUICK_FIX.md), [detailed guide](source/static/fix_glue_permissions.md), and [CLI helper](source/static/fix_glue_permissions_cli.sh)
- [SHA-256 inventory](source-manifest.json)

The `pages/` copies only rewrite local image and lesson links for GitHub reading. The `source/` tree preserves the original Markdown and assets. Workshop Studio-specific directives such as `::alert` remain as text in the GitHub view.

## Capture limits

- The original Module 05 `TROUBLESHOOTING.md` link was inaccessible (HTTP 403); [see the local note](pages/troubleshooting-unavailable.md).
- Event dashboard outputs, temporary AWS credentials, passwords, and active lab resources are not archived. The original event and its AWS account access expire.
- External AWS documentation and console links remain external; the instructions and their embedded images are stored locally.
