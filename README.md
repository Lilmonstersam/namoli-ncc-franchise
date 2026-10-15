# Namoli: Office Cleaning Franchise page mockup

Client review mockup for the Namoli `/franchise/` page, optimised for **"office cleaning franchise"**.
Two versions are deployed so the client can decide how much pricing to show on the live page:

| Page | File | What it shows |
|---|---|---|
| With pricing | `site/index.html` | Full 10-tier investment table, ongoing fees, worked example |
| Without pricing | `site/no-pricing.html` | Same page with all dollar figures and percentages removed |

A **review toggle** at the top of each page switches between the two. The toggle, the
"form preview only" overlay and the `noindex` tag are mockup-only and are **not** part of the live page.

## Structure

```
.github/workflows/deploy.yml   GitHub Actions: builds both versions and deploys /site to Pages
scripts/build_page.py          Builds a version from the source capture
source/franchise-original.html Saved capture of the live page (input)
site/                          Deployed output (index.html, no-pricing.html, assets/)
```

## Build locally

```bash
python3 scripts/build_page.py source/franchise-original.html site/index.html
python3 scripts/build_page.py source/franchise-original.html site/no-pricing.html nopricing
```

Open `site/index.html` in a browser to preview.

The build also strips tracking (GTM, MarketingCloudFX, Nutshell, Wordfence) and the WordPress admin bar
from the capture, so review visits never reach the client's analytics or CRM.

## Deploy

Every push to `main` runs `.github/workflows/deploy.yml`, which rebuilds both pages and publishes `site/`.
Repository setting required once: **Settings → Pages → Source: GitHub Actions**.

Pricing source: Namoli Form 115 Franchise Tier Pricing (November 2024). Prepared by Digilari Media.
