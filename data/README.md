# Brightwave synthetic data

Every person, company operation, product record and research result in this directory is invented. Brightwave Outfitters and Brightwave Parcel Service are fictional. Emails use reserved example domains. The card-like number in a few tickets is a labelled test fixture, never a real payment credential.

| Dataset | Size | Purpose |
|---|---:|---|
| [products.csv](products.csv) | 60 | Product descriptions, prices, stock, categories and JSON specifications |
| [policies/](policies/) | 4 policies | Returns, shipping, warranty and privacy with checkable thresholds |
| [handbook PDF](handbook/employee_handbook.pdf) | 10 pages | PDF loading and one-based page citations |
| [handbook Markdown](handbook/employee_handbook.md) | 10 sections | Source parsed by the PDF generator |
| [faq.json](faq.json) | 40 | Questions and policy-backed answers |
| [support_tickets.jsonl](support_tickets.jsonl) | 100; 50 labelled | Triage, varied tone/urgency and redaction |
| [orders.db](orders.db) | 200 orders | Customers, products, orders, items, shipments and returns |
| [reviews.csv](reviews.csv) | 300 | Sentiment, themes and report generation |
| [eval/](eval/) | 8 RAG, 15 triage, 6 conversation cases | Held-out factual and behavior checks |
| [security fixture](security/poisoned_doc.md) | 1 | Controlled indirect prompt-injection demonstration |
| [research/](research/) | 3 documents | Offline research with explicit synthetic provenance |

## Reproducibility

Seed: **271828**. Reference date: **2026-01-15**. Examples should use the fixed reference date for date-dependent seed decisions. Product prices are display strings in CSV and integer cents in SQLite. Order totals are derived from line items; all foreign keys are checked. SQLite has an additional product table so later stock tools can use one database.

```text
uv run --group authoring python scripts/build_data.py
uv run --group authoring python scripts/build_data.py --output-dir .runtime/data-check
uv run --group authoring pytest tests/test_data.py
```

You do not need to regenerate data to take the course. Rebuilding replaces only generator-owned files. [manifest.json](manifest.json) records SHA-256 hashes. Two builds using the same locked environment must match byte-for-byte; PDF font/library or SQLite format changes across platforms can change bytes, so semantic counts, text and database integrity are tested independently.

## Important boundaries

- Seed database access through `common.data.orders_connection()` is read-only. Use `copy_orders()` outside `data/` when practicing writes; it refuses overwrites.
- A return is not approved merely because a model says so. The synthetic rule is manager approval **over $100**, with eligibility checked separately.
- Free standard shipping requires a subtotal **over $75**, not at least $75. Returns are within **30 calendar days after delivery**.
- Load only the intended corpus. The poisoned document is excluded from ordinary policy retrieval.
- Labelled tickets support teaching/debugging; evaluation questions use different wording. Do not put held-out evaluation inputs in few-shot prompts.
- The small golden sets are teaching fixtures, not a statistically representative production benchmark. The trajectory schemas include denied access and rejected approval; later modules expand them with positive and repeated-write cases.
