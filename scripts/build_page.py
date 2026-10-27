import re, json, sys, html as H
SRC = sys.argv[1]; OUT = sys.argv[2]
NP = len(sys.argv) > 3 and sys.argv[3] == 'nopricing'
h = open(SRC, encoding='utf-8', errors='ignore').read()

def rep(old, new, count=1):
    global h
    n = h.count(old)
    if n < 1:
        raise SystemExit('NOT FOUND: ' + old[:120])
    h = h.replace(old, new, count)

# strip Ahrefs SEO Toolbar overlay captured when the page was saved
_s = h.find('<div id="rcr-wrapper"')
if _s >= 0:
    _d = 0
    for _m in re.finditer(r'<(/?)div\b[^>]*>', h[_s:]):
        _d += -1 if _m.group(1) else 1
        if _d == 0:
            h = h[:_s] + h[_s+_m.end():]; break

# ---------------- deployment hygiene ----------------
# asset folder renamed for GitHub Pages
h = h.replace('./Franchise - Namoli_files/', 'assets/').replace('../site/assets/', 'assets/')
# remove trackers so reviewer visits never hit the client's analytics / CRM
TRACK = re.compile(r'googletagmanager|gtm\.js|mcfx|marketingcloudfx|nutshell|Nutsheller|WordfenceI18nStrings|WFAJAXWatcherVars|wpcode_admin_bar_info|admin-bar(\.min)?\.js|ajaxWatcher|wfi18n', re.I)
h = re.sub(r'<script\b[^>]*>.*?</script>', lambda m: '' if TRACK.search(m.group(0)) else m.group(0), h, flags=re.S)
h = re.sub(r'<noscript>\s*<iframe[^>]*googletagmanager.*?</noscript>', '', h, flags=re.S)
h = re.sub(r'<link\b[^>]*href="assets/(?:admin-bar[^"]*|adminbar-[^"]*)"[^>]*>\s*', '', h)
# remove the logged-in WordPress admin bar (admin links, logout nonce)
_s = h.find('<div id="wpadminbar"')
if _s >= 0:
    _d = 0
    for _m in re.finditer(r'<(/?)div\b[^>]*>', h[_s:]):
        _d += -1 if _m.group(1) else 1
        if _d == 0:
            h = h[:_s] + h[_s+_m.end():]; break
h = h.replace(' logged-in admin-bar ', ' ')
h = re.sub(r'_wpnonce=[0-9a-f]+', '_wpnonce=', h)
h = re.sub(r'"nonce":"[0-9a-f]+"', '"nonce":""', h)
# mockup must not be indexed
h = h.replace('</title>', '</title>\n\t<meta name="robots" content="noindex, nofollow">', 1)

# ---------------- data ----------------
tiers = [(1,1500),(2,2000),(3,3000),(4,4000),(5,5000),(6,6000),(7,7000),(8,8000),(9,9000),(10,10000)]
inv = {1:24400,2:26200,3:29800,4:33400,5:37000,6:40600,7:44200,8:47800,9:51400,10:55000}
f = lambda n: '${:,}'.format(n)

faqs = [
 ("What is the initial investment (start-up cost)? Any hidden costs?",
  "A Namoli franchise starts at $24,400 + GST (Tier 1). That includes client contracts worth $1,500 a month and the $3,500 commercial products start-up kit. Higher tiers run to $55,000 + GST for $10,000 a month in contracts. Ongoing fees are 15% of gross revenue plus $1,200 a year in marketing and IT levies. Outside the franchise, budget for your vehicle, insurance, wages if you hire staff, and accounting. All franchise fees are set out in the Disclosure Document before you sign."),
 ("What are the ongoing franchise fees?",
  "A 9% royalty, 3% account administration and 3% operations support, totalling 15% of gross revenue. On top of that is a $600 annual marketing fee and a $600 annual IT levy. All figures exclude GST."),
 ("Is an office cleaning franchise profitable?",
  "It can be, but profit depends on your pricing, hours and labour costs, not revenue alone. After Namoli's 15% fees and $1,200 in annual levies, the rest of your revenue covers wages, consumables, your vehicle, insurance and tax. Commercial contracts are recurring, which makes income more predictable than one-off residential jobs. Model your numbers with an accountant using the Disclosure Document."),
 ("Do I need cleaning or business experience?",
  "No. Every franchisee is trained in commercial cleaning, infection control, workplace health and safety, industry standards and running a small business, then supported by Namoli's systems, processes and leadership team."),
 ("How much control do franchisees have over their business?",
  "A great deal. You can hire your own staff, choose the contracts you accept and take on as much work as you want, backed by Namoli's systems, processes, experienced leadership team and ongoing training."),
 ("What's the defined franchise territory?",
  "There is no exclusive franchise territory. You can operate anywhere in Queensland, provided the locations sit within the state territory outlined in your Franchise Agreement and Namoli can reasonably support operations there."),
 ("How long is the initial term of the franchise agreement?",
  "The initial term is 10 years. You can then renew for two further 10-year periods with zero renewal costs."),
 ("Am I limited to office cleaning?",
  "No. Namoli franchisees service a wide range of commercial clients, including offices, medical centres, childcare facilities, schools, industrial sites, retail and hospitality venues, provided they meet any required compliance or industry-specific standards."),
]

faqs_guest = list(faqs)
faqs_guest[0] = (faqs[0][0], "Your investment depends on the tier you choose, which sets the value of client contracts you start with. Every tier includes the commercial products start-up kit. Ongoing fees are a percentage of gross revenue plus small annual marketing and IT levies. Outside the franchise, budget for your vehicle, insurance, wages if you hire staff, and accounting. Members can log in to view the full investment schedule, or request the Franchise Information Guide. All franchise fees are set out in the Disclosure Document before you sign.")
faqs_guest[1] = (faqs[1][0], "Ongoing fees cover a royalty, account administration and operations support, charged as a percentage of gross revenue, plus annual marketing and IT levies. The exact figures are in the Franchise Information Guide and the Disclosure Document.")
faqs_guest[2] = (faqs[2][0], "It can be, but profit depends on your pricing, hours and labour costs, not revenue alone. After franchise fees, the rest of your revenue covers wages, consumables, your vehicle, insurance and tax. Commercial contracts are recurring, which makes income more predictable than one-off residential jobs. Model your numbers with an accountant using the Disclosure Document.")
if NP:
    faqs = faqs_guest

# Gated model: search engines only ever see the logged-out page, so title, meta and FAQ schema are price-free in both views
TITLE = 'Office Cleaning Franchise Brisbane &amp; Queensland | Namoli'
DESC = "Own a Namoli office cleaning franchise anywhere in Queensland. Start with client contracts and a start-up kit included, specialist training and a 5-step path."

# ---------------- head ----------------
rep('<title>Franchise - Namoli</title>',
    '<title>' + TITLE + '</title>\n\t<meta name="description" content="' + DESC + '">')
rep('og:title" content="Franchise"', 'og:title" content="' + TITLE + '"')
h = re.sub(r'og:description" content="[^"]*"', lambda m: 'og:description" content="' + DESC + '"', h, count=1)

faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs_guest]}

CSS = r'''
<style id="nf-optimised">
/* Office cleaning franchise optimisation: scoped additions, brand palette only */
.nf-chips{display:flex;flex-wrap:wrap;gap:8px 28px;margin:4px 0 28px}
.nf-chip{display:inline-flex;align-items:center;gap:8px;padding:0;border:0;border-radius:0;background:none;color:#fff;font-size:15px;font-weight:600;line-height:1.3}
.kb-row-layout-id1508739_c2fcfd-3d .hero-headline{margin-top:70px}
/* We work with the best: one-line autoplay logo carousel */
main .wp-block-group.client-grid.nf-marquee{display:block !important;overflow:hidden;width:min(1140px, calc(100vw - 48px));position:relative;left:50%;transform:translateX(-50%);-webkit-mask-image:linear-gradient(to right,transparent,#000 7%,#000 93%,transparent);mask-image:linear-gradient(to right,transparent,#000 7%,#000 93%,transparent)}
.nf-marquee-track{display:flex;align-items:center;gap:56px;width:max-content;animation:nf-logo-scroll 38s linear infinite}
.nf-marquee:hover .nf-marquee-track,.nf-marquee:focus-within .nf-marquee-track{animation-play-state:paused}
main .wp-block-group.client-grid .nf-marquee-track > figure{flex:0 0 200px;width:200px;max-width:200px;margin:0 !important}
main .wp-block-group.client-grid .nf-marquee-track > figure img{width:100% !important;height:80px !important;object-fit:contain !important}
@keyframes nf-logo-scroll{to{transform:translateX(calc(-50% - 28px))}}
@media (max-width:767px){.nf-marquee-track{gap:32px;animation-duration:28s}main .wp-block-group.client-grid .nf-marquee-track > figure{flex-basis:140px;width:140px;max-width:140px}main .wp-block-group.client-grid .nf-marquee-track > figure img{height:56px !important}@keyframes nf-logo-scroll{to{transform:translateX(calc(-50% - 16px))}}}
@media (prefers-reduced-motion:reduce){.nf-marquee-track{animation:none;flex-wrap:wrap;justify-content:center;width:auto}.nf-marquee-track > [aria-hidden="true"]{display:none}main .wp-block-group.client-grid.nf-marquee{-webkit-mask-image:none;mask-image:none}}
/* Start Your Journey form: visual preview only in the mockup */
#contact-form .ep-iFrameContainer{position:relative}
#contact-form .ep-iFrameContainer::after{content:"Form preview only: submissions are disabled in this mockup";position:absolute;inset:0;display:flex;align-items:flex-start;justify-content:center;padding-top:10px;background:rgba(255,255,255,0);color:#003b5c;font-size:13px;font-weight:700;cursor:not-allowed}
html{margin-top:0 !important}
/* Gated pricing */
#franchise-cost{scroll-margin-top:calc(var(--nf-rt-h,52px) + 190px)}
.nf-gate{position:relative;max-width:980px;margin:0 auto;border-radius:16px;overflow:hidden;border:1px solid #d1dae2;background:#fff}
.nf-gate-teaser{filter:blur(5px);opacity:.55;pointer-events:none;user-select:none}
.nf-gate-teaser table.nf-table thead tr th{white-space:nowrap}
.nf-gate-card{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;background:linear-gradient(180deg,rgba(255,255,255,.55),rgba(255,255,255,.92))}
.nf-gate-lock{display:flex !important;align-items:center;justify-content:center;flex:0 0 48px;width:48px !important;height:48px !important;min-height:48px;box-sizing:border-box;border-radius:50%;background:#003b5c;color:#fff;margin-bottom:12px;line-height:1}
.nf-gate-lock svg{width:22px !important;height:22px !important;flex:0 0 22px}
.nf-gate-card .nf-k{color:#f45b69;font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase}
.nf-gate-card h3{color:#003b5c;font-size:22px;font-weight:700;margin:6px 0 8px}
.nf-gate-card p{color:#3a596e;font-size:15px;line-height:1.6;max-width:520px;margin:0 auto 16px}
.nf-gate-btns{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-bottom:14px}
.nf-btn{display:inline-block;padding:13px 20px;border-radius:5px;font-weight:700;font-size:16px;text-decoration:none;line-height:1.2;transition:background .2s,color .2s,border-color .2s}
.nf-btn-primary{background:#f45b69;color:#fff;border:1px solid #f45b69}
.nf-btn-primary:hover,.nf-btn-primary:focus{background:#003b5c;border-color:#003b5c;color:#fff}
.nf-btn-ghost{background:#fff;color:#003b5c;border:1px solid #003b5c}
.nf-btn-ghost:hover,.nf-btn-ghost:focus{background:#003b5c;color:#fff}
.nf-gate-card p.nf-gate-alt{font-size:14px;margin-bottom:6px}
.nf-gate-alt a{color:#d64d63;font-weight:700}
.nf-gate-card p.nf-mock-note{font-size:12px;color:#64748b;font-style:italic;margin:0}
.nf-member-banner{display:flex;align-items:center;justify-content:center;gap:8px;max-width:620px;margin:0 auto 22px;padding:10px 16px;border-radius:8px;background:#e8f5ec;color:#1f6b3a;font-weight:700;font-size:15px;text-align:center}
.nf-member-banner span{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:#1f6b3a;color:#fff;font-size:13px}
.nf-tag-row{text-align:center;margin:0 0 10px}
.nf-tag{display:inline-block;vertical-align:middle;padding:3px 10px;border-radius:999px;background:#fff1f3;color:#d64d63;font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase}
@media (max-width:767px){.nf-gate-card{position:relative;inset:auto;background:#fff}.nf-gate-teaser{display:none}.nf-gate-card h3{font-size:19px}}
/* Review toggle (mockup only) */
html{margin-top:var(--nf-rt-h,52px) !important}
header{top:var(--nf-rt-h,52px) !important}
#nf-review-toggle{position:fixed;top:0;left:0;right:0;z-index:2147483000;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:6px 18px;padding:8px 16px;background:#002a42;color:#fff;font-size:14px;line-height:1.3;border-bottom:3px solid #f45b69}
#nf-review-toggle .nf-rt-label{font-weight:700;letter-spacing:.06em;text-transform:uppercase;font-size:12px;color:#f45b69}
#nf-review-toggle .nf-rt-switch{display:inline-flex;background:rgba(255,255,255,.1);border-radius:6px;padding:3px}
#nf-review-toggle .nf-rt-switch a{color:#fff;text-decoration:none;font-weight:700;padding:7px 14px;border-radius:4px;font-size:14px}
#nf-review-toggle .nf-rt-switch a[aria-current="page"]{background:#f45b69;color:#fff}
#nf-review-toggle .nf-rt-switch a:not([aria-current]):hover{background:rgba(255,255,255,.15)}
#nf-review-toggle .nf-rt-note{color:#c9d6df;font-size:13px}
@media (max-width:767px){#nf-review-toggle{gap:4px 10px;padding:6px 10px}#nf-review-toggle .nf-rt-label{display:none}#nf-review-toggle .nf-rt-switch a{padding:6px 10px;font-size:13px}#nf-review-toggle .nf-rt-note{font-size:11.5px;text-align:center;width:100%}}
.nf-chip b{color:#f45b69}
.nf-section{padding:4rem 1.5rem}
.nf-section.nf-tint{background:#f8fafc}
.nf-wrap{max-width:1200px;margin:0 auto}
.nf-eyebrow{color:#f45b69;font-weight:700;font-size:13px;letter-spacing:.08em;text-transform:uppercase;text-align:center;margin:0 0 8px}
.nf-wrap h2.nf-h2{color:#003b5c;text-align:center;font-size:25px;font-weight:700;margin:0 0 14px;line-height:1.25}
.nf-wrap h3.nf-h3{color:#003b5c;font-size:20px;font-weight:700;margin:48px 0 12px;text-align:center}
.nf-lead{max-width:780px;margin:0 auto 34px;text-align:center;color:#475569;font-size:17px;line-height:1.7}
.nf-cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px;margin:0 0 44px}
.nf-card{background:#fff;border:1px solid #f1f5f9;border-radius:16px;padding:26px;box-shadow:0 4px 20px rgba(0,0,0,.05);transition:border-color .3s ease}
.nf-card:hover{border-color:#f45b69}
.nf-card .nf-k{display:block;color:#f45b69;font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:10px}
.nf-card h3{color:#003b5c;font-size:17px;font-weight:700;margin:0 0 10px;line-height:1.3}
.nf-card p{color:#475569;font-size:15px;line-height:1.65;margin:0}
.nf-table-wrap{overflow-x:auto;border-radius:12px;border:1px solid #d1dae2;background:#fff;-webkit-overflow-scrolling:touch}
table.nf-table{width:100%;border-collapse:collapse;margin:0;font-size:15px;border:0}
table.nf-table thead tr th{background:#003b5c;color:#fff;text-align:left;padding:14px 18px;font-weight:700;border:0;white-space:nowrap}
table.nf-table tbody tr,table.nf-table tbody tr td{background:#fff}
table.nf-table tbody tr:nth-child(even),table.nf-table tbody tr:nth-child(even) td{background:#f8fafc}
table.nf-table td{padding:12px 18px;border:0;border-top:1px solid #e2e8f0;color:#1a2e3a;vertical-align:top;line-height:1.55}
table.nf-table td.nf-num{font-variant-numeric:tabular-nums;white-space:nowrap}
table.nf-table td strong{color:#003b5c}
table.nf-table tr.nf-total td{background:#fff1f3 !important;font-weight:700;color:#003b5c}
.nf-fine{color:#64748b;font-size:13px;line-height:1.6;margin:12px 0 0;text-align:center}
.nf-stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin:32px 0 0}
.nf-stat{background:#f8fafc;border:1px solid #f1f5f9;border-radius:16px;padding:24px}
.nf-stat strong{display:block;color:#003b5c;font-size:28px;line-height:1.15;margin-bottom:8px}
.nf-stat span{color:#475569;font-size:15px;line-height:1.6}
.nf-split{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:32px;align-items:start}
.nf-example{background:#003b5c;color:#fff;border-radius:16px;padding:28px 30px}
.nf-example .nf-k{color:#f45b69;font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;display:block;margin-bottom:10px}
.nf-example p{color:#fff;margin:0 0 12px;font-size:15px;line-height:1.7}
.nf-example ul{margin:0 0 14px;padding:0;list-style:none}
.nf-example li{display:flex;justify-content:space-between;gap:16px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.15);font-size:15px}
.nf-example li:last-child{border-bottom:0;font-weight:700;color:#f45b69}
.nf-ctas{display:flex;flex-wrap:wrap;gap:16px 28px;align-items:center;justify-content:center;margin-top:36px}
.nf-ctas .wp-block-kadence-advancedbtn{margin:0}
.nf-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:20px;counter-reset:nfstep}
.nf-steps li{counter-increment:nfstep;background:#fff;border:1px solid #f1f5f9;border-radius:16px;padding:24px 22px;box-shadow:0 4px 20px rgba(0,0,0,.05)}
.nf-steps li::before{content:counter(nfstep);display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:#f45b69;color:#fff;font-weight:700;margin-bottom:16px}
.nf-steps h3{color:#003b5c;font-size:16px;font-weight:700;margin:0 0 8px;line-height:1.3}
.nf-steps p{color:#475569;font-size:14px;line-height:1.6;margin:0}
.nf-steps a{color:#d64d63;font-weight:700}
.nf-note{max-width:780px;margin:24px auto 0;background:#e6ebf0;border-radius:12px;padding:16px 22px;color:#3a596e;font-size:15px;line-height:1.6;text-align:center}
@media (max-width:1024px){.nf-cards{grid-template-columns:repeat(2,minmax(0,1fr))}.nf-steps{grid-template-columns:repeat(2,minmax(0,1fr))}.nf-split{grid-template-columns:1fr}}
@media (max-width:767px){.nf-section{padding:3rem 1rem}.nf-cards,.nf-stats,.nf-steps{grid-template-columns:1fr}.nf-wrap h2.nf-h2{font-size:22px}table.nf-table{font-size:14px}.nf-tiers th:nth-child(3),.nf-tiers td:nth-child(3){display:none}.nf-tiers td:first-child{white-space:nowrap}table.nf-table thead tr th{white-space:normal}table.nf-table td,table.nf-table thead tr th{padding:10px 12px}}
</style>
<script type="application/ld+json" id="nf-faq-schema">''' + json.dumps(faq_ld, ensure_ascii=False) + '''</script>
'''
rep('</head>', CSS + '</head>')

# ---------------- hero ----------------
h, _n = re.subn(r'<div style="\s*display:inline-flex;(?:(?!<h1).)*?<span>Available in Brisbane</span>\s*</div>\s*', '', h, count=1, flags=re.S)
assert _n == 1, 'pill not removed'
if NP:
    HERO_P = 'Own a commercial cleaning business anywhere in Queensland, starting with client contracts and a commercial products start-up kit included. No cleaning experience needed: just a proven system, specialist training and a support team behind every contract.</p>\n<div class="nf-chips"><span class="nf-chip"><b>&#10003;</b> Client contracts from day one</span><span class="nf-chip"><b>&#10003;</b> No experience needed</span><span class="nf-chip"><b>&#10003;</b> 10-year term, 2 free renewals</span></div>'
else:
    HERO_P = 'Own a commercial cleaning business from $24,400 + GST, with client contracts worth $1,500 a month and a commercial products start-up kit included. No cleaning experience needed: just a proven system, specialist training and a support team behind every contract.</p>\n<div class="nf-chips"><span class="nf-chip"><b>&#10003;</b> From $24,400 + GST</span><span class="nf-chip"><b>&#10003;</b> $1,500/month in contracts included</span><span class="nf-chip"><b>&#10003;</b> 10-year term, 2 free renewals</span></div>'

rep('''<h1 class="hero-headline">
  Build a Scalable Commercial Cleaning Business,
  <span class="highlight-text">Backed by Data.</span>
</h1>''', '''<h1 class="hero-headline">
  Build a Scalable Office Cleaning Franchise,
  <span class="highlight-text">Backed by Data.</span>
</h1>''')
rep('Join a franchise network that prioritises compliance, transparency, and high-value contracts. No generic cleaning: just professional, systemised facility management.</p>',
    HERO_P)

# ---------------- cost section (after trust strip) ----------------
rows = ''.join('<tr><td><strong>Tier {}</strong></td><td class="nf-num">{}</td><td class="nf-num">{}</td><td class="nf-num"><strong>{}</strong></td></tr>'.format(t, f(m), f(m*12), f(inv[t])) for t,m in tiers)
btn_primary = '<div class="wp-block-kadence-advancedbtn kb-buttons-wrap kb-btns1508739_763ee9-e3"><a class="kb-button kt-button button kb-btn1508739_e7e403-87 kt-btn-size-small kt-btn-width-type-auto kb-btn-global-fill kt-btn-has-text-true wp-block-kadence-singlebtn" href="#contact-form"><span class="kt-btn-inner-text">Request a discovery call</span></a></div>'
guide_link = '<div class="guide-link-wrap" style="width:auto"><a href="https://www.namoli.com.au/franchise/#" class="open-form-btn"><span>Download the Franchise Information Guide &gt;</span></a></div>'

COST = f'''
<section class="nf-section" id="franchise-cost" aria-labelledby="nf-cost-h">
<div class="nf-wrap">
<p class="nf-member-banner"><span>&#10003;</span> You&rsquo;re logged in. The full investment schedule is unlocked.</p>
<p class="nf-eyebrow">Your investment</p>
<h2 class="nf-h2" id="nf-cost-h">How Much Does an Office Cleaning Franchise Cost?</h2>
<p class="nf-lead">Most cleaning franchisors publish a &ldquo;from&rdquo; price with an asterisk. We publish the full schedule. Choose how much client revenue you start with and your initial investment scales with it. Every tier includes the same four things:</p>

<div class="nf-cards">
<div class="nf-card"><span class="nf-k">Day one</span><h3>Starter client contracts</h3><p>Contracts worth $1,500 to $10,000 a month, matched to your tier, so you start with paying clients rather than a cold-call list.</p></div>
<div class="nf-card"><span class="nf-k">$3,500 value</span><h3>Commercial products start-up kit</h3><p>Hospital-grade, eco-friendly chemicals and commercial products to service sites from your first shift. Included in every tier.</p></div>
<div class="nf-card"><span class="nf-k">No experience needed</span><h3>Specialist training</h3><p>Commercial cleaning methods, infection control, workplace health and safety, industry standards and how to run a small business.</p></div>
<div class="nf-card"><span class="nf-k">Built into your fees</span><h3>Admin and operations backing</h3><p>Account administration and operations support sit behind every contract, so you focus on the work and the client relationship.</p></div>
</div>

<p class="nf-tag-row"><span class="nf-tag">Members only</span></p>
<div class="nf-table-wrap">
<table class="nf-table nf-tiers">
<caption class="screen-reader-text">Namoli franchise tier pricing schedule, all figures exclude GST</caption>
<thead><tr><th scope="col">Tier</th><th scope="col">Starting monthly contracts</th><th scope="col">Annual contract value</th><th scope="col">Initial investment (incl. start-up kit)</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
<p class="nf-fine">All figures exclude GST. Contract values are the client work allocated at each tier, not a forecast of profit or personal income. Source: Namoli Form 115 Franchise Tier Pricing, November 2024.</p>

<div class="nf-stats">
<div class="nf-stat"><strong>+$3,600</strong><span>for every extra $1,000 a month of starting contracts you add.</span></div>
<div class="nf-stat"><strong>$1.36 &rarr; $0.46</strong><span>Investment per dollar of annual contract value at Tier 1 versus Tier 10. Bigger tiers buy revenue more cheaply.</span></div>
<div class="nf-stat"><strong>14 days</strong><span>Minimum gap between your disclosure meeting and investing. Time to get independent advice, by design.</span></div>
</div>

<h3 class="nf-h3">Ongoing Franchise Fees, in Plain Numbers <span class="nf-tag">Members only</span></h3>
<div class="nf-split">
<div class="nf-table-wrap">
<table class="nf-table">
<thead><tr><th scope="col">Fee</th><th scope="col">Amount</th></tr></thead>
<tbody>
<tr><td>Royalty</td><td class="nf-num">9% of gross revenue</td></tr>
<tr><td>Account administration</td><td class="nf-num">3% of gross revenue</td></tr>
<tr><td>Operations support</td><td class="nf-num">3% of gross revenue</td></tr>
<tr class="nf-total"><td>Total service fees</td><td class="nf-num">15% of gross revenue</td></tr>
<tr><td>Marketing fee</td><td class="nf-num">$600 per year</td></tr>
<tr><td>IT levy</td><td class="nf-num">$600 per year</td></tr>
</tbody>
</table>
</div>
<div class="nf-example">
<span class="nf-k">Worked example: Tier 5</span>
<p>$60,000 a year in contracts, before GST:</p>
<ul>
<li><span>Service fees (15%)</span><span>$9,000</span></li>
<li><span>Marketing fee + IT levy</span><span>$1,200</span></li>
<li><span>Total franchise fees</span><span>$10,200</span></li>
</ul>
<p style="margin:0">That leaves $49,800 to cover your labour, consumables, vehicle, insurance and tax before profit. Run the numbers with your accountant before you choose a tier.</p>
</div>
</div>

<div class="nf-ctas">{btn_primary}{guide_link}</div>
</div>
</section>
'''
TEASER = ''.join('<tr><td>Tier {}</td><td>$#,###</td><td>$##,###</td><td>$##,###</td></tr>'.format(t) for t in range(1, 9))
if NP:
    COST = f'''
<section class="nf-section" id="franchise-cost" aria-labelledby="nf-cost-h">
<div class="nf-wrap">
<p class="nf-eyebrow">Your investment</p>
<h2 class="nf-h2" id="nf-cost-h">How Much Does an Office Cleaning Franchise Cost?</h2>
<p class="nf-lead">Your investment scales with the value of client contracts you choose to start with, across 10 tiers, so you decide the size of the business you launch. Every tier includes the same four things:</p>
<div class="nf-cards">
<div class="nf-card"><span class="nf-k">Day one</span><h3>Starter client contracts</h3><p>Contracts matched to your investment tier, so you start with paying clients rather than a cold-call list.</p></div>
<div class="nf-card"><span class="nf-k">Every tier</span><h3>Commercial products start-up kit</h3><p>Hospital-grade, eco-friendly chemicals and commercial products to service sites from your first shift.</p></div>
<div class="nf-card"><span class="nf-k">No experience needed</span><h3>Specialist training</h3><p>Commercial cleaning methods, infection control, workplace health and safety, industry standards and how to run a small business.</p></div>
<div class="nf-card"><span class="nf-k">Built into your fees</span><h3>Admin and operations backing</h3><p>Account administration and operations support sit behind every contract, so you focus on the work and the client relationship.</p></div>
</div>
<div class="nf-gate">
<div class="nf-gate-teaser" aria-hidden="true"><table class="nf-table"><thead><tr><th>Tier</th><th>Starting monthly contracts</th><th>Annual contract value</th><th>Initial investment</th></tr></thead><tbody>{TEASER}</tbody></table></div>
<div class="nf-gate-card">
<span class="nf-gate-lock" aria-hidden="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg></span>
<span class="nf-k">Members only</span>
<h3>See the full investment schedule</h3>
<p>Log in or create a free account to view all 10 investment tiers, the ongoing fee breakdown and a worked example.</p>
<div class="nf-gate-btns"><a class="nf-btn nf-btn-primary" href="member.html#franchise-cost">Log in to view pricing</a><a class="nf-btn nf-btn-ghost" href="member.html#franchise-cost">Create an account</a></div>
<p class="nf-gate-alt">Prefer to talk it through? <a href="#contact-form">Request a discovery call</a> or download the Franchise Information Guide.</p>
<p class="nf-mock-note">Mockup: both buttons preview the logged-in view. Live: /member-login/ and /register/.</p>
</div>
</div>
<div class="nf-ctas">{btn_primary}{guide_link}</div>
</div>
</section>
'''
anchor_4r = '<div class="kb-row-layout-wrap kb-row-layout-id1508739_c579f6-2e'
rep(anchor_4r, COST + anchor_4r)

# soften the guarantee claim (ACL risk) without changing the message
rep('Generic cleaning models rely on volume. We rely on a system. At Namoli, we guarantee your operational success through our strict 4 R’s Framework:',
    'Generic cleaning models rely on volume. We rely on a system. Every Namoli office cleaning franchise runs on our strict 4 R’s Framework:')

# ---------------- specialist paths: office first ----------------
office_col_start = h.find('<div class="wp-block-kadence-column kadence-column1508739_cd7a5a-8c">')
med_col_start = h.find('<div class="wp-block-kadence-column kadence-column1508739_016d8a-98 kb-section-dir-vertical">')
edu_col_start = h.find('<div class="wp-block-kadence-column kadence-column1508739_15bd91-6a">')
assert 0 < med_col_start < office_col_start < edu_col_start
med_block = h[med_col_start:office_col_start]
office_block = h[office_col_start:edu_col_start]
# swap only inner cards so Kadence column classes (widths) stay in place
med_card = re.search(r'<div class="special-card blue">.*?</div>\n</div>', med_block, re.S).group(0)
off_card = re.search(r'<div class="special-card blue">.*?</div>\n</div>', office_block, re.S).group(0)
new_med_block = med_block.replace(med_card, off_card)
new_office_block = office_block.replace(off_card, med_card)
h = h[:med_col_start] + new_med_block + new_office_block + h[edu_col_start:]
rep('Enhance workplace hygiene and productivity. Our security-cleared teams provide consistent, non-disruptive cleaning tailored to corporate schedules and high-traffic areas.',
    'The backbone of commercial cleaning: recurring, after-hours contracts for corporate offices. Security-cleared teams deliver consistent, non-disruptive cleaning built around client schedules and high-traffic areas.')
rep('Namoli franchisees are trained to operate in high-stakes environments, allowing you to secure higher-value contracts than general cleaners.',
    'Start with office cleaning, then add sectors as you grow. Namoli franchisees are trained to operate in high-stakes environments, allowing you to secure higher-value contracts than general cleaners.')

# ---------------- comparison + steps (before logo row) ----------------
if NP:
    VS_CLIENTS, VS_UPFRONT, VS_ONGOING = ('Client contracts allocated to match your tier', 'Tiered investment, start-up kit included', 'Percentage-based service fees plus small annual marketing and IT levies')
else:
    VS_CLIENTS, VS_UPFRONT, VS_ONGOING = ('Contracts worth $1,500 to $10,000 a month, by tier', '$24,400 to $55,000 + GST, start-up kit included', '15% of gross revenue + $1,200 a year')
VS = '''
<section class="nf-section nf-tint" id="franchise-vs-independent" aria-labelledby="nf-vs-h">
<div class="nf-wrap">
<p class="nf-eyebrow">The honest trade-off</p>
<h2 class="nf-h2" id="nf-vs-h">Office Cleaning Franchise vs Starting From Scratch</h2>
<p class="nf-lead">Going independent costs less up front. A franchise costs more, but removes the slowest, riskiest part of year one: finding clients who sign recurring contracts.</p>
<div class="nf-table-wrap">
<table class="nf-table">
<thead><tr><th scope="col"></th><th scope="col">Namoli franchise</th><th scope="col">Independent start-up</th></tr></thead>
<tbody>
<tr><td><strong>Clients on day one</strong></td><td>' + VS_CLIENTS + '</td><td>None. You build a client list from zero</td></tr>
<tr><td><strong>Up-front cost</strong></td><td>' + VS_UPFRONT + '</td><td>Lower, but equipment, insurance, branding and software are all on you</td></tr>
<tr><td><strong>Ongoing cost</strong></td><td>' + VS_ONGOING + '</td><td>No franchise fees, but you fund your own sales, admin and marketing</td></tr>
<tr><td><strong>Training and compliance</strong></td><td>Infection control, WHS and industry standards; Working With Children Check vetting for education sites</td><td>Self-sourced and self-funded</td></tr>
<tr><td><strong>Credibility with buyers</strong></td><td>ISSA, FCA, BSCAA and DHA memberships, plus established commercial clients</td><td>Built job by job</td></tr>
<tr><td><strong>Agreement term</strong></td><td>10 years, plus two 10-year renewals at no renewal cost</td><td>Not applicable</td></tr>
</tbody>
</table>
</div>
</div>
</section>

<section class="nf-section" id="become-a-franchisee" aria-labelledby="nf-steps-h">
<div class="nf-wrap">
<p class="nf-eyebrow">Your path to ownership</p>
<h2 class="nf-h2" id="nf-steps-h">How to Become a Namoli Franchisee in 5 Steps</h2>
<p class="nf-lead">A transparent process with independent advice built in, so you sign knowing exactly what you are buying.</p>
<ol class="nf-steps">
<li><h3>Enquire</h3><p>Call <a href="tel:1300626654">1300 626 654</a> or complete the form below.</p></li>
<li><h3>Meet the Franchise Manager</h3><p>A presentation on the Namoli franchise opportunity and the tier that fits your goals.</p></li>
<li><h3>Attend a disclosure meeting</h3><p>Receive the Franchise Disclosure Document, Franchise Agreement and supporting documents.</p></li>
<li><h3>Get independent advice</h3><p>Have a solicitor explain the documents. We also recommend an accountant or business adviser.</p></li>
<li><h3>Sign and start</h3><p>Sign the Franchise Agreement and welcome to the Namoli franchise family.</p></li>
</ol>
<p class="nf-note">A minimum of 14 days must pass between your disclosure meeting and investing in a Namoli franchise.</p>
<div class="nf-ctas">''' + btn_primary + '''</div>
</div>
</section>
'''
VS = VS.replace("' + VS_CLIENTS + '", VS_CLIENTS).replace("' + VS_UPFRONT + '", VS_UPFRONT).replace("' + VS_ONGOING + '", VS_ONGOING)
anchor_logos = '<div class="kb-row-layout-wrap kb-row-layout-id1508739_e73af7-d4'
rep(anchor_logos, VS + anchor_logos)

# ---------------- FAQ accordion ----------------
acc_start = h.find('<div class="wp-block-kadence-accordion alignnone">')
acc_inner_start = h.find('<div class="kt-accordion-inner-wrap', acc_start)
acc_inner_open_end = h.find('>', acc_inner_start) + 1
last_pane = h.rfind('<div class="wp-block-kadence-pane', acc_inner_open_end, h.find('Start Your Journey', acc_inner_open_end))
_d = 0
for _m in re.finditer(r'<(/?)div\b[^>]*>', h[last_pane:]):
    _d += -1 if _m.group(1) else 1
    if _d == 0:
        panes_end = last_pane + _m.end(); break
old_panes = h[acc_inner_open_end:panes_end]
pane_classes = re.findall(r'kt-pane1508739_[0-9a-f]+-[0-9a-f]+', old_panes)
assert len(pane_classes) == 5, pane_classes
panes = []
for i,(q,a) in enumerate(faqs):
    pid = 408128 + i*7
    active = i == 0
    pc = pane_classes[min(i, 4)]
    hdr_act = " kt-accordion-panel-active" if active else ""
    exp = "true" if active else "false"
    pan_cls = "kt-accordion-panel-active" if active else "kt-accordion-panel-hidden"
    sty = ' style=""' if active else ""
    panes.append(
      f'<div class="wp-block-kadence-pane kt-accordion-pane kt-accordion-pane-{i+1} {pc}"><div class="kt-accordion-header-wrap"><button class="kt-blocks-accordion-header kt-acccordion-button-label-show{hdr_act}" type="button" id="kt-accordion-header-{pid}" aria-controls="kt-accordion-panel-{pid}" data-kt-accordion-header-id="{i}" aria-expanded="{exp}"><span class="kt-blocks-accordion-title-wrap"><span class="kt-blocks-accordion-title">{H.escape(q)}</span></span><span class="kt-blocks-accordion-icon-trigger"></span></button></div><div class="kt-accordion-panel {pan_cls}" id="kt-accordion-panel-{pid}" aria-labelledby="kt-accordion-header-{pid}" role="region" data-panel-height="0px"{sty}><div class="kt-accordion-panel-inner">\n<p class="wp-block-paragraph">{H.escape(a)}</p>\n</div></div></div>\n\n\n\n')
h = h[:acc_inner_open_end] + '\n' + ''.join(panes) + h[panes_end:]
rep('kt-accordion-has-5-panes', 'kt-accordion-has-8-panes')
rep('>Common Questions</h2>', '>Office Cleaning Franchise FAQs</h2>')
rep('Our franchise team is available to answer specific questions about territories in Brisbane.',
    'Our franchise team can walk you through tiers, fees and available contracts across Queensland.')

# ---------------- logo carousel markup ----------------
_cg = re.search(r'(<div class="wp-block-group client-grid[^"]*")([^>]*>)(.*?)(</div>\s*</div></div>)', h, re.S)
assert _cg, 'client-grid not found'
_figs = re.findall(r'<figure\b.*?</figure>', _cg.group(3), re.S)
assert len(_figs) == 7, len(_figs)
_dupes = [f.replace('<figure ', '<figure aria-hidden="true" ', 1).replace(' alt="', ' alt="" data-alt="') for f in _figs]
_track = '<div class="nf-marquee-track">' + ''.join(_figs) + ''.join(_dupes) + '</div>\n'
h = h[:_cg.start()] + _cg.group(1)[:-1] + ' nf-marquee"' + _cg.group(2) + _track + _cg.group(4) + h[_cg.end():]

# ---------------- header login link: simulate member state ----------------
if NP:
    h = h.replace('<a href="https://www.namoli.com.au/member-login/">Login</a>', '<a href="member.html#franchise-cost">Login</a>')
else:
    h = h.replace('<a href="https://www.namoli.com.au/member-login/">Login</a>', '<a href="index.html">Log out</a>')

# ---------------- review toggle (mockup only) ----------------
_cur_out, _cur_in = (' aria-current="page"', '') if NP else ('', ' aria-current="page"')
TOGGLE = ('\n<!-- REVIEW TOGGLE: mockup only, remove before go-live -->\n'
          '<div id="nf-review-toggle" role="region" aria-label="Mockup version toggle">'
          '<span class="nf-rt-label">Gated pricing preview</span>'
          '<span class="nf-rt-switch"><a href="index.html"' + _cur_out + '>Logged out (public)</a><a href="member.html"' + _cur_in + '>Logged in (member)</a></span>'
          '<span class="nf-rt-note">Simulates the member login for review. This toggle is not included when the page goes live.</span></div>\n'
          '<script>(function(){function s(){var t=document.getElementById("nf-review-toggle");if(t)document.documentElement.style.setProperty("--nf-rt-h",t.offsetHeight+"px")}s();window.addEventListener("load",s);window.addEventListener("resize",s)})();</script>\n')
h = re.sub(r'(<body\b[^>]*>)', lambda m: m.group(1) + TOGGLE, h, count=1)

# ---------------- embedded forms: freeze as static snapshots ----------------
# The saved LeadConnector forms are Nuxt server-rendered snapshots. Their scripts try to
# hydrate from a URL that doesn't exist on GitHub Pages, fail, and reload the iframe in a
# loop (flicker between the form and a 500 error). Strip all scripts so the form renders
# once as a static preview, and drop the parent-page embed script that re-initialises it.
import os
h = re.sub(r'<script\b[^>]*src="assets/form_embed\.js"[^>]*>\s*</script>\s*', '', h)
_site_dir = os.path.dirname(os.path.abspath(OUT))
for _src in sorted(set(re.findall(r'<iframe\b[^>]*\bsrc="(assets/[^"]+\.html)"', h))):
    _fp = os.path.join(_site_dir, _src)
    if not os.path.exists(_fp):
        continue
    _f = open(_fp, encoding='utf-8', errors='ignore').read()
    _f2 = re.sub(r'<script\b[^>]*>.*?</script>', '', _f, flags=re.S)
    _f2 = re.sub(r'<script\b[^>]*/>', '', _f2)
    _f2 = re.sub(r'<link\b[^>]*rel="modulepreload"[^>]*>', '', _f2)
    if '<meta name="robots"' not in _f2:
        _f2 = _f2.replace('<head>', '<head><meta name="robots" content="noindex, nofollow">', 1)
    if _f2 != _f:
        open(_fp, 'w', encoding='utf-8').write(_f2)

open(OUT, 'w', encoding='utf-8').write(h)
print('written', OUT, len(h))
