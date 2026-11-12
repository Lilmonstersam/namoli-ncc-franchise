# Namoli: Office Cleaning Franchise page mockup

Client review mockup for the Namoli `/franchise/` page, optimised for **"office cleaning franchise"**.
Pricing is **gated behind the Franchise Information Guide form**: the public page shows no pricing, and
submitting the form leads to a thank-you page with a link to the 2026 pricing. No account is needed.

| Step | File | What it shows |
|---|---|---|
| 1. Franchise page (public) | `site/index.html` | No dollar figures. The cost section teases a blurred tier table with a "Get the 2026 pricing" button that opens the guide form |
| 2. Thank-you page | `site/thank-you.html` | Shown after the guide form is submitted. Confirms the guide is on its way and links to the 2026 pricing |
| 3. 2026 pricing page | `site/pricing-2026.html` | Full 10-tier investment table, ongoing fees, worked example and the 5-step path |

`no-pricing.html` and `member.html` redirect to the new pages for old review links.

The review bar at the top steps through the flow. It, the "Preview: submit form" button in the guide modal,
the "Mockup:" notes, the "form preview only" overlay and the `noindex` tags are mockup-only and are **not**
part of the live pages.

### Live implementation (WordPress + LeadConnector)

1. Publish `/franchise/` from the public version (no pricing).
2. Create two pages: `/franchise-thank-you/` and `/franchise-pricing-2026/`. Set both to **noindex**, leave them
   out of menus and the XML sitemap.
3. In LeadConnector, set the Franchise Information Guide form's on-submit action to **redirect to
   `/franchise-thank-you/`**. The current modal's download link is a placeholder
   (`yourdomain.com/.../YOUR-FILE.pdf`), so the redirect also fixes the guide delivery.
4. Point the "Get the 2026 pricing" button at the same guide form (it uses the existing `open-form-btn` modal).
5. The pricing URL can be shared once someone has it. Treat it as soft-gated, and confirm all figures in the
   Disclosure Document.

## Structure

```
.github/workflows/deploy.yml   GitHub Actions: builds both versions and deploys /site to Pages
scripts/build_page.py          Builds the public or priced page from the source capture
scripts/build_gated_pages.py   Builds the thank-you and 2026 pricing pages
source/franchise-original.html Saved capture of the live page (input)
site/                          Deployed output (index.html, thank-you.html, pricing-2026.html, assets/)
```

## Build locally

```bash
python3 scripts/build_page.py source/franchise-original.html site/index.html nopricing
python3 scripts/build_page.py source/franchise-original.html /tmp/priced.html
python3 scripts/build_gated_pages.py site/index.html /tmp/priced.html site
```

Open `site/index.html` in a browser to preview.

The build also strips tracking (GTM, MarketingCloudFX, Nutshell, Wordfence) and the WordPress admin bar
from the capture, so review visits never reach the client's analytics or CRM.

## Deploy

Every push to `main` runs `.github/workflows/deploy.yml`, which rebuilds both views and publishes `site/`.
Repository setting required once: **Settings → Pages → Source: GitHub Actions**.

Pricing source: Namoli Form 115 Franchise Tier Pricing (November 2024). Prepared by Digilari Media.
