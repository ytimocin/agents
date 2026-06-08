# SEO Structured Data agent prompts

Reference knowledge for **structured data and rich results in Google Search** — the JSON-LD format, the Schema.org vocabulary (a Google + Microsoft + Yahoo + Yandex community project, ~800 types, ~1500 properties, ~45M domains using it), the 26+ rich-result types Google currently surfaces, plus the adjacent metadata layers (Open Graph, Twitter / X Cards, Pinterest Rich Pins). One of four sibling agents under `seo/`: companion to `seo-core` (content quality + E-E-A-T + on-page craft), `seo-technical` (crawling + indexing + robots + sitemaps + canonical + hreflang + Search Console), and `seo-performance` (Core Web Vitals + page experience + Lighthouse).

Covers the **`@context` / `@type` / `@id` / `@graph` JSON-LD patterns** with cross-page `@id` references, multi-typing (`"@type": ["LocalBusiness", "Restaurant", "Place"]`), where to put `<script type="application/ld+json">` blocks, the **JSON-LD vs Microdata vs RDFa** tradeoffs and why JSON-LD wins for new projects. Covers **all 26+ rich-result types** with required + recommended properties per type — **Article / NewsArticle / BlogPosting**, **Breadcrumb**, **Carousel**, **Course List**, **Dataset**, **Discussion Forum**, **Education Q&A**, **Employer Aggregate Rating**, **Event**, **FAQ** (deprecated for general sites since May 2026 — government + health authority sites only), **Image Metadata (IPTC)**, **Job Posting**, **Local Business** (with the 70+ Schema.org subtypes — Restaurant / Store / MedicalBusiness / Hotel / LegalService / etc. and the relationship with Google Business Profile), **Math Solver**, **Movie**, **Organization** (with the underrated `sameAs` property for Knowledge-Graph grounding), **Product Snippets** (review pages) vs **Merchant Listings** (e-commerce pages with `offers` + `price` + `priceCurrency` ISO 4217 + `availability` schema.org URIs + `shippingDetails` + `hasMerchantReturnPolicy`), **Profile Page**, **Q&A**, **Recipe**, **Review Snippet**, **Software App**, **Speakable**, **Subscription / Paywalled Content** (the disclosure mechanism that distinguishes paywalls from spam-policy-1 cloaking), **Vacation Rental**, **Vehicle Listing**, **Video** (with `Clip`-based Key Moments and `BroadcastEvent` for LIVE-badge streams) — plus the **deprecated-and-must-remove** types (HowTo removed September 2023, sitelinks-searchbox markup removed October 2024 since Google now generates sitelinks automatically). Covers the **testing workflow** — Rich Results Test (search.google.com/test/rich-results) as the authoritative Google-eligibility tester vs Schema Markup Validator (validator.schema.org) for vocab compliance, URL Inspection in Search Console for post-deploy render-truth, the Search Console Enhancements report for ongoing monitoring. Covers **per-type implementation specifics** — Article author conventions (each author as separate `Person`, never comma-concatenated, `url` linking to a real indexable bio page that itself has `Person` markup with `sameAs` to social profiles — the chain Google uses to ground E-E-A-T author identity), Product `aggregateRating` + `reviewCount` requirements, BreadcrumbList with 1-indexed `position`, LocalBusiness's required `address`/`name` + recommended `telephone`/`geo`/`openingHoursSpecification`, VideoObject with `contentUrl` preferred over `embedUrl`, FAQ structure for the gov/health exception, paywall disclosure with `isAccessibleForFree: false` + `cssSelector`-targeted `WebPageElement`. Covers the **adjacent metadata layers**: **Open Graph** (`og:type` / `og:title` / `og:description` / `og:url` / `og:image` 1200×630 standard) for Facebook / LinkedIn / Slack / Discord / iMessage link previews, **Twitter / X Cards** (`twitter:card=summary_large_image` / `summary` / `player` / `app`, `twitter:site` / `twitter:creator`), **Pinterest Rich Pins** (auto-read from page structured data — no separate markup needed). Grounded in live docs at https://developers.google.com/search/docs/appearance/structured-data/ with inline `Full docs:` links per section — Google retires markup categories on a schedule (HowTo 2023, FAQ 2026), so re-audit at least annually.

## Files

| File | Target tool | Format |
|------|-------------|--------|
| `claude.md` | Claude Code | Markdown with YAML frontmatter |
| `codex.md` | OpenAI Codex | Plain markdown |
| `copilot.md` | GitHub Copilot | Plain markdown |

## Install

### Claude Code

```bash
mkdir -p ~/.claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/seo/seo-structured-data/claude.md \
  -o ~/.claude/agents/seo-structured-data-specialist.md
```

### OpenAI Codex

```bash
mkdir -p ~/.codex
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/seo/seo-structured-data/codex.md \
  -o ~/.codex/AGENTS.md
```

### GitHub Copilot CLI

```bash
mkdir -p .github
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/seo/seo-structured-data/copilot.md \
  -o .github/copilot-instructions.md
```

## Provenance and scope

- Built from https://developers.google.com/search/docs/appearance/structured-data/ — the Search Gallery (the canonical list of supported rich-result types), the intro page, the general-guidelines / sd-policies page, and per-type pages for Article, Product, Breadcrumb, FAQ, LocalBusiness, Video, Organization, Paywalled Content.
- Plus the Schema.org vocabulary site (https://schema.org), the JSON-LD 1.1 W3C spec (https://www.w3.org/TR/json-ld11/), the Open Graph protocol (https://ogp.me), Twitter Cards (https://developer.x.com/en/docs/twitter-for-websites/cards/overview/abouts-cards), and Pinterest Rich Pins (https://help.pinterest.com/en/business/article/rich-pins).
- Snapshot date: **2026-06-07**. Important recent changes: **HowTo rich results removed September 2023** (no longer eligible regardless of markup); **FAQ rich results removed for general sites May 2026** (gov + health authority sites only) with full Rich Results Test support removal slated for August 2026; **sitelinks-searchbox markup removed October 2024** (Google generates sitelinks automatically). Re-audit per-type docs for required-property updates.
- **Structured data + rich results + adjacent social-link-preview metadata only.** Content quality / E-E-A-T / titles out of scope (see `seo-core`). Crawl / index / canonical / hreflang / Search Console out of scope (see `seo-technical`). Core Web Vitals out of scope (see `seo-performance`).
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. WebFetch the per-type page before quoting required-property lists — Google updates them.
