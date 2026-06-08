# SEO Performance agent prompts

Reference knowledge for **the page-experience layer of Google SEO** — Core Web Vitals (LCP / INP / CLS), the broader page-experience signals (HTTPS / mobile-friendliness / intrusive interstitials / ad density / content clarity), and the measurement stack (CrUX field data vs Lighthouse lab data vs PageSpeed Insights vs Search Console's Core Web Vitals report vs your own RUM via `web-vitals.js`). One of four sibling agents under `seo/`: companion to `seo-core` (content + E-E-A-T + spam policies + on-page craft), `seo-technical` (crawl + index + robots + sitemaps + canonical + hreflang + JS SEO + Search Console), and `seo-structured-data` (Schema.org + JSON-LD + the 26+ rich-result types + Open Graph + Twitter Cards).

Covers the **three Core Web Vitals** with the @ p75 thresholds across mobile-and-desktop-separately — **LCP** (Largest Contentful Paint — ≤ 2.5s good, 2.5-4s needs improvement, > 4s poor; measures the largest `<img>` / `<image>` in SVG / `<video>` poster / CSS-background-image / block-level text element's render time relative to navigation; decomposes into TTFB + resource-load-delay + resource-load-duration + element-render-delay; the optimization playbook — `<link rel="preload" as="image">` + `fetchpriority="high"` + responsive `srcset`/`sizes` + modern formats AVIF/WebP + CDN with image optimization + eliminating render-blocking CSS/JS + inlining critical CSS + `font-display: optional` + SSR/SSG over CSR for the hero), **INP** (Interaction to Next Paint — replaced FID in March 2024, ≤ 200ms good / 200-500ms needs improvement / > 500ms poor; measures the slowest click/tap/keyboard interaction's full latency from input to next paint across the entire page session; decomposes into input-delay + processing-time + presentation-delay; the optimization playbook — break up long tasks with `scheduler.yield()` / `setTimeout(0)` / `scheduler.postTask` / `requestIdleCallback`, move heavy work to Web Workers, virtualize long lists with `react-window` / `@tanstack/virtual` / native `content-visibility: auto`, debounce/throttle high-frequency inputs, **defer / async / Partytown third-party scripts** as the new INP battleground, React 18 transitions with `useTransition` / `startTransition`, the Long Animation Frames (LoAF) API for diagnosing slow frames in field data, the Event Timing API for RUM attribution), **CLS** (Cumulative Layout Shift — ≤ 0.1 good / 0.1-0.25 needs improvement / > 0.25 poor; measures the largest burst of unexpected layout shifts in a session window with the within-500ms-of-user-input expected-shift exemption; the five biggest fixes — always set `width`/`height` attributes on images and iframes for aspect-ratio reservation, reserve space for ads/embeds with `min-height` or `aspect-ratio`, `font-display: optional` + `size-adjust`/`ascent-override` to size-match fallback fonts, animate only `transform`/`opacity`/`filter` instead of layout properties). Covers the **lab-vs-field distinction** (lab = Lighthouse synthetic Moto-G4-on-slow-4G run for debugging + CI; field = CrUX or your own RUM for what Google actually ranks on — the verdict). Covers **CrUX** (the Chrome User Experience Report — 28-day rolling window, real Chrome users with usage-statistics opted in + synced history + no Sync passphrase, four access surfaces — PageSpeed Insights + CrUX API + public BigQuery dataset + CrUX History API, URL-level + origin-level data with the no-URL-level-data-for-low-traffic-pages footgun → page-experience signal defaults to neutral). Covers **Lighthouse** (5 audit categories — Performance / Accessibility / Best Practices / SEO; PWA deprecated December 2024 and removed in Lighthouse 12+; Agentic Browsing added 2026+; the perf score weights — LCP 25% / TBT 30% / CLS 25% / SI 10% / FCP 10% — with **INP not in the lab score** because it requires real interactions, TBT as the lab proxy). Covers **PageSpeed Insights** (unified mobile + desktop dashboard combining CrUX field data + Lighthouse lab + ranked opportunities; the "Core Web Vitals Assessment Passed/Failed" badge is the SEO-relevant verdict from field data). Covers **Search Console's Core Web Vitals report** (URL groups grouped by Google; the "Validate fix" flow with multi-day re-evaluation; 28-day data lag). Covers measuring yourself with the **`web-vitals` JS library** (~2KB, `onLCP` / `onINP` / `onCLS` / `onFCP` / `onTTFB`; the attribution build for element selectors / interaction targets / shift sources — faster feedback than CrUX's 28-day lag, all browsers not just Chrome, per-segment slicing). Covers the **non-CWV page-experience signals** (HTTPS required; mobile usability — viewport meta + ≥48px tap targets + ≥16px body text + never `user-scalable=no`; intrusive-interstitials demotion for modals blocking main content right after navigation; ad-density signal for excessive ads interfering with main content). Covers the **end-to-end optimization workflow** (identify metric → identify URLs → reproduce in lab → diagnose with attribution → apply per-metric fix → verify lab → deploy → monitor RUM 1-2 days → wait 14-28 days for CrUX → Validate fix in Search Console). Page experience is a **ranking factor, not just a tiebreaker** per Google — but **relevance dominates**, so this is a multiplier on content quality, not a substitute. Grounded in live docs at https://developers.google.com/search/docs/appearance/page-experience and https://web.dev/articles/vitals with inline `Full docs:` links per section.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/seo/seo-performance/claude.md \
  -o ~/.claude/agents/seo-performance-specialist.md
```

### OpenAI Codex

```bash
mkdir -p ~/.codex
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/seo/seo-performance/codex.md \
  -o ~/.codex/AGENTS.md
```

### GitHub Copilot CLI

```bash
mkdir -p .github
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/seo/seo-performance/copilot.md \
  -o .github/copilot-instructions.md
```

## Provenance and scope

- Built from Google Search Central's page-experience guidance at https://developers.google.com/search/docs/appearance/page-experience, web.dev's CWV documentation at https://web.dev/articles/vitals (LCP / INP / CLS per-metric pages), Chrome's Lighthouse docs at https://developer.chrome.com/docs/lighthouse/overview, PageSpeed Insights at https://pagespeed.web.dev, the CrUX documentation at https://developer.chrome.com/docs/crux, and the `web-vitals` JS library at https://github.com/GoogleChrome/web-vitals.
- Snapshot date: **2026-06-07**. Important recent changes: **INP replaced FID as a Core Web Vital in March 2024** (all FID-targeted advice is now stale); **the standalone "Mobile-Friendly Test" tool was retired late 2023** (diagnostic moved into Search Console's URL Inspection); **Lighthouse's PWA category was deprecated December 2024 and removed in Lighthouse 12+**; the legacy "Page Experience" Search Console report was retired November 2023 in favor of the dedicated Core Web Vitals report.
- **Core Web Vitals + page experience + measurement stack only.** Content / titles / E-E-A-T / spam policies out of scope (see `seo-core`). Crawl / index / canonical / hreflang / JS SEO / Search Console diagnostics out of scope (see `seo-technical`). Structured data / rich results out of scope (see `seo-structured-data`).
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. WebFetch the per-metric web.dev page when exact threshold or recent optimization-pattern updates matter — web.dev's optimization guides get rewritten with each Chrome major.
