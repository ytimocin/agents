# SEO Core agent prompts

Reference knowledge for **the foundation of Google SEO** — Google Search Essentials (the rules), the spam-policy enforcement surface, the helpful-content / E-E-A-T framework, and on-page craft (titles, meta descriptions, headings, internal linking, anchor text, URL hygiene). One of four sibling agents under `seo/`: companion to `seo-technical` (crawling, indexing, robots.txt, sitemaps, canonical, hreflang, redirects, JS SEO, Search Console), `seo-structured-data` (Schema.org + JSON-LD + the 26+ rich-result types + Open Graph + Twitter Cards), and `seo-performance` (Core Web Vitals — LCP, INP, CLS — + page-experience signals + Lighthouse + CrUX).

Covers the **three layers of Google Search Essentials** (technical requirements / 18 spam policies / best practices), the spam-policy catalog verbatim (cloaking, doorways, expired-domain abuse, hacked content, hidden text + link abuse, keyword stuffing, link spam, machine-generated traffic, malicious practices, misleading functionality, **scaled content abuse** — explicitly the policy that covers low-effort AI content, scraping, **site reputation abuse** / "parasite SEO" heavily enforced since May 2024, sneaky redirects, thin affiliation, user-generated spam, policy circumvention, scam and fraud), enforcement modes (algorithmic vs manual actions visible in Search Console vs index removal), the **E-E-A-T rubric** (Experience-Expertise-Authoritativeness-Trustworthiness with Trust as "most important"; the framework Search Quality Raters use, not a direct algorithmic factor — the rubric calibrates the signals), the four self-assessment buckets (content & quality / expertise / presentation & production / who-how-why), YMYL ("Your Money or Your Life") higher-bar topic handling for health/finance/legal/news, **title-link generation** (the priority order of sources Google uses — `<title>` element / main visual title / `<h1>` / `og:title` / large prominent styled text / body content / anchor text from inbound links / `WebSite` structured data; ~50-60 character truncation; brand placement with delimiters; why Google rewrites ~20-30% of `<title>` elements), **meta descriptions** (the `<meta name="description">` as a suggestion not a guarantee; per-query snippet generation; when Google overrides; the `nosnippet` / `max-snippet:N` / `max-image-preview` / `max-video-preview:N` / `data-nosnippet` controls), heading conventions (H1 as title-link input not a magic ranking factor; semantic structure for accessibility more than SEO), **link best practices** (crawlable `<a href>` only — `<span onClick>` / `routerLink="…"` / `javascript:` URLs invisible to Google; anchor-text discipline — "click here" considered harmful; the `rel="nofollow" | "sponsored" | "ugc"` triplet as *hints* not directives since 2019; hub-and-spoke internal linking; never `nofollow` internal links to "sculpt PageRank"; the every-important-page-needs-an-inbound-internal-link rule), URL hygiene (descriptive lowercase hyphenated paths, the one-canonical-per-resource rule, parameter sprawl mitigation), and the misconceptions Google explicitly refutes (meta keywords ignored since 2009, no magic word count, date-only updates detected, AI content not banned — quality is the criterion, "domain authority" not a Google metric). Grounded in live docs at https://developers.google.com/search/ with inline `Full docs:` links per section so the agent can fetch upstream when exact wording matters — Google rewrites the spam policies and helpful-content guidance multiple times per year.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/seo/seo-core/claude.md \
  -o ~/.claude/agents/seo-core-specialist.md
```

### OpenAI Codex

```bash
mkdir -p ~/.codex
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/seo/seo-core/codex.md \
  -o ~/.codex/AGENTS.md
```

### GitHub Copilot CLI

```bash
mkdir -p .github
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/seo/seo-core/copilot.md \
  -o .github/copilot-instructions.md
```

## Provenance and scope

- Built from https://developers.google.com/search — Search Essentials, spam policies, SEO Starter Guide, helpful-content guidance, title-link and snippet docs, link best practices.
- Cross-referenced with the Search Quality Rater Guidelines PDF (https://services.google.com/fh/files/misc/hsw-sqrg.pdf) for the rubric Google's raters use.
- Snapshot date: **2026-06-07**. Google rewrites the helpful-content framing and tightens spam policies regularly — re-audit the spam-policies and helpful-content pages quarterly.
- **Content quality, on-page craft, spam policies, E-E-A-T only.** Crawl/index/canonical/hreflang/JS SEO out of scope (see `seo-technical`). Structured data out of scope (see `seo-structured-data`). Core Web Vitals out of scope (see `seo-performance`).
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. WebFetch the canonical Search Central page when policy wording or rich-result-eligibility specifics matter.
