# SEO Technical agent prompts

Reference knowledge for **the technical layer of Google SEO** — Googlebot identification + verification, the crawl/index/render pipeline, robots.txt + `noindex` directives, sitemaps, canonical URLs, redirects, JavaScript SEO, mobile-first indexing, international targeting via `hreflang`, URL structure, and Google Search Console as the diagnostic surface. One of four sibling agents under `seo/`: companion to `seo-core` (content quality + E-E-A-T + spam policies + titles + on-page craft), `seo-structured-data` (Schema.org + JSON-LD + the 26+ rich-result types), and `seo-performance` (Core Web Vitals + page experience + Lighthouse).

Covers **Googlebot taxonomy** (the three categories — common crawlers / special-case crawlers like AdsBot that ignore `User-agent: *` by default / user-triggered fetchers, every variant including **Google-Extended** as the opt-out token for Gemini + Vertex AI training, Google-CloudVertexBot, Google-InspectionTool), reverse-then-forward DNS verification, public IP-range JSONs, the 15 MB body-size cap and HTTP/2 + Brotli support; **robots.txt** (RFC 9309 spec, `User-agent` / `Disallow` / `Allow` / `Sitemap` syntax, Google's `*` and `$` wildcard extensions, the 24h cache, **blocks crawling but not indexing** — disallowed URLs can still appear with no snippet if externally linked, the "don't double-block with `noindex`" footgun, per-host exact-match on protocol + host + port); **robots meta tag + `X-Robots-Tag` HTTP header** (`noindex` / `nofollow` / `noarchive` / `nosnippet` / `max-snippet:N` / `max-image-preview` / `max-video-preview:N` / `noimageindex` / `unavailable_after:ISO-8601`, bot-specific overrides, the must-be-crawlable-to-be-noindexed rule); **sitemaps** (sitemaps.org XML protocol, 50,000-URL / 50 MB-uncompressed limits, sitemap-index files, `<lastmod>` honored but `<changefreq>` / `<priority>` ignored by Google, image / video / news / hreflang sitemap variants, the deprecated ping endpoint replaced by `Sitemap:` in robots.txt and Search Console submission); **canonicalization** (the duplicate-cause taxonomy — protocol/host/trailing-slash/params/case/mobile-separate-URLs/AMP/pagination/filters/print/staging, the canonical-signal stack with `<link rel="canonical">` + HTTP `Link` header + sitemap `<loc>` + 301s + internal linking + HTTPS preference, **canonical is a hint not a directive** — Google can override per the "Duplicate, Google chose different canonical than user" Search Console report); **redirects** (301 Moved Permanently vs 308 Permanent-keep-method, 302 Found vs 307 Temporary-keep-method vs 303 See Other, meta-refresh instant=permanent / delayed=temporary, the avoid-chains-greater-than-1-hop rule with hard cap at 5, HTTPS migration checklist with HSTS, soft-404 avoidance, the no-1000-URLs-to-the-homepage rule); **JavaScript SEO** — the 3-phase crawl → render → index pipeline with deferred WRS rendering on recent Chromium, strategies ranked by SEO-friendliness (SSG/SSR/ISR A+, hybrid dynamic-rendering A-, CSR-with-hydration B, pure CSR C, fragment-only routing F), why `<span onClick>` / `routerLink` / `javascript:` URLs are invisible, lazy-loading caveats, soft-404 SPA gotchas, URL Inspection + Rich Results Test as the render-truth viewers; **mobile-first indexing** (fully rolled out October 2023, responsive vs dynamic-serving vs separate-URLs with responsive recommended, the content-gap / structured-data / lazy-loading / title-meta divergence failure modes); **hreflang** (the three equivalent declaration methods — HTML link / HTTP Link header / sitemap `<xhtml:link>`, the `<language>[-<region>]` format with ISO 639-1 + ISO 3166-1 alpha-2 — `en-GB` not `en-UK`, `x-default` fallback, the bidirectional return-link requirement that silently drops one-way annotations, the ccTLD vs subdomain vs subdirectory strategy with Google's lean toward subdirectory + hreflang); URL structure (descriptive lowercase hyphenated stable URLs, the deprecated URL-parameter-handling tool, faceted-nav parameter-sprawl mitigation); **Search Console** as the diagnostic surface (Domain property + DNS TXT verification vs URL-prefix, the URL Inspection / Pages / Sitemaps / Performance / Removals / Manual actions / Security issues / Links reports, the BigQuery bulk-export bypassing the 1000-row truncation, the Search Console API); **Bing Webmaster Tools** + **IndexNow** for non-Google + AI-search ingestion. Grounded in live docs at https://developers.google.com/search/docs/crawling-indexing/ with inline `Full docs:` links per section. The robots.txt spec is RFC 9309 (IETF, September 2022); sitemaps.org is the multi-vendor XML protocol.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/seo/seo-technical/claude.md \
  -o ~/.claude/agents/seo-technical-specialist.md
```

### OpenAI Codex

```bash
mkdir -p ~/.codex
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/seo/seo-technical/codex.md \
  -o ~/.codex/AGENTS.md
```

### GitHub Copilot CLI

```bash
mkdir -p .github
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/seo/seo-technical/copilot.md \
  -o .github/copilot-instructions.md
```

## Provenance and scope

- Built from Google Search Central's crawling/indexing docs: https://developers.google.com/search/docs/crawling-indexing — overview-google-crawlers, verifying-googlebot, robots/intro, robots-meta-tag, sitemaps/overview, canonicalization, consolidate-duplicate-urls, 301-redirects, javascript/javascript-seo-basics, mobile/mobile-sites-mobile-first-indexing, url-structure.
- Plus the international docs at https://developers.google.com/search/docs/specialty/international, robots.txt RFC 9309 (https://www.rfc-editor.org/rfc/rfc9309), sitemaps.org protocol (https://www.sitemaps.org/protocol.html), Search Console help (https://support.google.com/webmasters), IndexNow spec (https://www.indexnow.org), Bing Webmaster Guidelines (https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a).
- Snapshot date: **2026-06-07**. Google adds crawlers (`Google-Extended` for AI-training opt-out was added in 2023; `Google-CloudVertexBot` more recently) and rewrites the canonicalization-signal list periodically. Re-audit annually.
- **Crawling, indexing, robots, sitemaps, canonical, hreflang, redirects, JS SEO, mobile-first, Search Console only.** Content quality / E-E-A-T / spam policies out of scope (see `seo-core`). Structured data out of scope (see `seo-structured-data`). Core Web Vitals out of scope (see `seo-performance`).
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs.
