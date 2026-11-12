"""Build the thank-you page and the 2026 pricing page for the form-gated pricing flow.

Usage:
  python scripts/build_gated_pages.py <public index.html> <priced build.html> <site dir>

Both outputs reuse the public page's header, footer, styles and review bar, with new <main> content.
The priced sections (tier table, fees, worked example, 5 steps) are lifted from the priced build.
"""
import re, sys, os

PUBLIC, PRICED, SITE = sys.argv[1], sys.argv[2], sys.argv[3]
base = open(PUBLIC, encoding='utf-8').read()
priced = open(PRICED, encoding='utf-8').read()

def grab(html, sid):
    m = re.search(r'<section class="nf-section[^"]*" id="' + sid + r'".*?</section>', html, re.S)
    assert m, sid
    return m.group(0)

cost = grab(priced, 'franchise-cost')
cost = cost.replace('href="#contact-form"', 'href="index.html#contact-form"')
cost = cost.replace('<p class="nf-eyebrow">Your investment</p>', '<p class="nf-eyebrow">2026 pricing</p>')
cost = cost.replace('How Much Does an Office Cleaning Franchise Cost?', 'Your Investment, Tier by Tier')
cost = cost.replace('Most cleaning franchisors publish a &ldquo;from&rdquo; price with an asterisk. We publish the full schedule. ', '')
steps = grab(priced, 'become-a-franchisee')
steps = steps.replace('href="#contact-form"', 'href="index.html#contact-form"')
steps = steps.replace('or complete the form below.', 'or complete the <a href="index.html#contact-form">enquiry form</a>.')

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'

THANKS_MAIN = f'''
<section class="nf-page-hero" aria-labelledby="nf-ty-h">
<div class="nf-wrap">
<span class="nf-hero-icon" aria-hidden="true">{CHECK}</span>
<p class="nf-eyebrow">Thank you</p>
<h1 id="nf-ty-h">Your Franchise Information Guide is <span>on its way</span></h1>
<p>Check your inbox in the next few minutes. As promised, here&rsquo;s the full 2026 investment schedule for a Namoli office cleaning franchise, with every tier, the ongoing fees and a worked example.</p>
<div class="nf-hero-btns"><a class="nf-btn nf-btn-primary" href="pricing-2026.html">View the 2026 franchise pricing</a><a class="nf-btn nf-btn-light" href="index.html#contact-form">Request a discovery call</a></div>
</div>
</section>
<section class="nf-section nf-tint" aria-labelledby="nf-next-h">
<div class="nf-wrap">
<p class="nf-eyebrow">What happens next</p>
<h2 class="nf-h2" id="nf-next-h">Three Steps From Here</h2>
<ol class="nf-next">
<li><h3>Review the 2026 pricing</h3><p>Compare all 10 tiers and see which starting contract value suits the business you want to build. <a href="pricing-2026.html">View pricing</a></p></li>
<li><h3>Read your guide</h3><p>It covers our 4 R&rsquo;s framework, training, specialist paths and the support behind every contract.</p></li>
<li><h3>Talk to our Franchise Manager</h3><p>Call <a href="tel:1300626654">1300 626 654</a> or <a href="index.html#contact-form">request a discovery call</a> to discuss available contracts across Queensland.</p></li>
</ol>
<p class="nf-note">All figures are confirmed in the Franchise Disclosure Document, with a minimum of 14 days to get independent advice before you invest.</p>
</div>
</section>
'''

PRICING_MAIN = f'''
<section class="nf-page-hero" aria-labelledby="nf-pr-h">
<div class="nf-wrap">
<p class="nf-eyebrow">Namoli franchise</p>
<h1 id="nf-pr-h">2026 Franchise <span>Investment Schedule</span></h1>
<p>Thanks for requesting the Franchise Information Guide. Here&rsquo;s the full investment schedule for a Namoli office cleaning franchise. All figures exclude GST.</p>
<div class="nf-hero-btns"><a class="nf-btn nf-btn-primary" href="index.html#contact-form">Request a discovery call</a><a class="nf-btn nf-btn-light" href="tel:1300626654">Call 1300 626 654</a></div>
</div>
</section>
{cost}
{steps}
'''

def page(main_html, title, desc, current):
    h = base
    i = h.index('<main'); i = h.index('>', i) + 1
    j = h.index('</main>')
    h = h[:i] + main_html + h[j:]
    h = re.sub(r'<title>.*?</title>', '<title>' + title + '</title>', h, count=1, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + desc + '">', h, count=1)
    h = re.sub(r'og:title" content="[^"]*"', 'og:title" content="' + title + '"', h, count=1)
    h = re.sub(r'og:description" content="[^"]*"', lambda m: 'og:description" content="' + desc + '"', h, count=1)
    h = re.sub(r'<link rel="canonical"[^>]*>\s*', '', h)
    h = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>\s*', '', h, flags=re.S)
    h = h.replace(' aria-current="page"', '')
    h = h.replace('href="' + current + '">', 'href="' + current + '" aria-current="page">', 1)
    return h

os.makedirs(SITE, exist_ok=True)
open(os.path.join(SITE, 'thank-you.html'), 'w', encoding='utf-8').write(
    page(THANKS_MAIN, 'Thank You | Namoli Franchise', 'Your Namoli Franchise Information Guide is on its way. View the 2026 franchise investment schedule.', 'thank-you.html'))
open(os.path.join(SITE, 'pricing-2026.html'), 'w', encoding='utf-8').write(
    page(PRICING_MAIN, '2026 Franchise Pricing | Namoli', 'The 2026 Namoli office cleaning franchise investment schedule: all 10 tiers, ongoing fees and a worked example.', 'pricing-2026.html'))
print('written thank-you.html and pricing-2026.html')
