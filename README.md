# Namoli: Office Cleaning Franchise page mockup

Client review mockup for the Namoli `/franchise/` page, optimised for **"office cleaning franchise"**.
The page uses **gated pricing**: the public sees the page without pricing, and logged-in members see
the full investment schedule.

| View | File | What it shows |
|---|---|---|
| Logged out (public) | `site/index.html` | No dollar figures. Cost section shows a "Members only" login/register gate over a blurred teaser |
| Logged in (member) | `site/member.html` | Full 10-tier investment table, ongoing fees, worked example, priced FAQs |

`site/no-pricing.html` redirects to `index.html` for old review links.

A **review toggle** at the top switches between the two views and simulates the login. The toggle, the
"Mockup:" note under the gate buttons, the "form preview only" overlay and the `noindex` tag are mockup-only
and are **not** part of the live page. Title, meta description and FAQ schema are price-free in both views,
because search engines only see the logged-out page.

### Live implementation (WordPress)

Server-side, so pricing is never sent to logged-out visitors. Add as a WPCode PHP snippet:

```php
add_filter( 'render_block', function ( $html, $block ) {
    $class = $block['attrs']['className'] ?? '';
    if ( str_contains( $class, 'nm-members-only' ) && ! is_user_logged_in() ) { return ''; }
    if ( str_contains( $class, 'nm-guests-only' ) && is_user_logged_in() ) { return ''; }
    return $html;
}, 10, 2 );
```

Add the CSS class `nm-members-only` to the pricing blocks and `nm-guests-only` to the gate and no-pricing blocks.
Bypass page/Cloudflare cache when the `wordpress_logged_in_*` cookie is present. Fix `/register/` first (the
registration shortcode currently renders as plain text).

## Structure

```
.github/workflows/deploy.yml   GitHub Actions: builds both versions and deploys /site to Pages
scripts/build_page.py          Builds a version from the source capture
source/franchise-original.html Saved capture of the live page (input)
site/                          Deployed output (index.html = logged out, member.html = logged in, assets/)
```

## Build locally

```bash
python3 scripts/build_page.py source/franchise-original.html site/index.html nopricing
python3 scripts/build_page.py source/franchise-original.html site/member.html
```

Open `site/index.html` in a browser to preview.

The build also strips tracking (GTM, MarketingCloudFX, Nutshell, Wordfence) and the WordPress admin bar
from the capture, so review visits never reach the client's analytics or CRM.

## Deploy

Every push to `main` runs `.github/workflows/deploy.yml`, which rebuilds both views and publishes `site/`.
Repository setting required once: **Settings → Pages → Source: GitHub Actions**.

Pricing source: Namoli Form 115 Franchise Tier Pricing (November 2024). Prepared by Digilari Media.
