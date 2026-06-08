# agents

[![verify](https://github.com/ytimocin/agents/actions/workflows/verify.yml/badge.svg)](https://github.com/ytimocin/agents/actions/workflows/verify.yml)
[![links](https://github.com/ytimocin/agents/actions/workflows/links.yml/badge.svg)](https://github.com/ytimocin/agents/actions/workflows/links.yml)
[![license](https://img.shields.io/github/license/ytimocin/agents)](./LICENSE)

Agent prompts for [Claude Code](https://docs.claude.com/en/docs/claude-code), [OpenAI Codex](https://github.com/openai/codex), and [GitHub Copilot](https://docs.github.com/en/copilot).

Each topic folder holds one source of knowledge (`knowledge.md`) and three generated tool-facing files, so the same knowledge is served to whichever AI tool a teammate uses. Topics either sit at the top level (singletons) or live under a **domain folder** when ≥2 related topics cluster.

## Layout

```
agents/
  <domain>/                  # only when ≥2 related topics exist
    <topic>/
      knowledge.md           # shared body — the only file edited by hand
      claude.frontmatter.yaml
      claude.md              # generated
      codex.md               # generated
      copilot.md             # generated
      README.md              # per-topic install guide (curl URLs include the full path)
  <topic>/                   # singletons stay flat
    knowledge.md
    …
```

CI regenerates `claude.md`, `codex.md`, and `copilot.md` from `knowledge.md` on every push and fails the build if any has drifted. `scripts/sync.sh` walks the tree recursively — domain nesting depth doesn't matter for sync.

## How to use

Pick the topic folder you care about and follow its `README.md` for install instructions per tool.

## Topics

### `cloud-native/` — Kubernetes ecosystem

- [cloud-native/argocd](cloud-native/argocd/) — declarative GitOps continuous delivery for Kubernetes (CNCF graduated)
- [cloud-native/cilium](cloud-native/cilium/) — eBPF-based CNI for Kubernetes networking, security (L3/L4/L7 NetworkPolicy), observability (Hubble), service mesh, cluster mesh
- [cloud-native/flux](cloud-native/flux/) — CNCF-graduated pull-based GitOps toolkit (source-controller, kustomize-controller, helm-controller, notification-controller, image automation, SOPS)
- [cloud-native/helm](cloud-native/helm/) — the package manager for Kubernetes (charts, templating, hooks, OCI registries, CLI)
- [cloud-native/kubefleet](cloud-native/kubefleet/) — multi-cluster Kubernetes management (CNCF sandbox; hub-and-spoke placement, scheduling, staged rollouts, overrides, drift detection)
- [cloud-native/kubernetes](cloud-native/kubernetes/) — the container orchestration platform itself (workloads, networking, storage, RBAC, troubleshooting)

### `databases/` — databases

- [databases/postgres](databases/postgres/) — PostgreSQL, split into 5 specialists:
  - [postgres-sql](databases/postgres/postgres-sql/) — SQL language, indexes, MVCC, EXPLAIN/planner tuning
  - [postgres-plpgsql](databases/postgres/postgres-plpgsql/) — PL/pgSQL functions, triggers, event triggers, exception handling, dynamic SQL
  - [postgres-admin](databases/postgres/postgres-admin/) — server administration, postgresql.conf/pg_hba.conf, replication, PITR, VACUUM/autovacuum
  - [postgres-extensions](databases/postgres/postgres-extensions/) — bundled contrib extensions (pg_stat_statements, pg_trgm, pgcrypto, postgres_fdw, hstore, ltree, …)
  - [postgres-tools](databases/postgres/postgres-tools/) — psql, pg_dump/pg_restore, pg_basebackup, pg_upgrade, pgbench, vacuumdb, …

### `mobile/` — mobile development

- [mobile/expo](mobile/expo/) — Expo / React Native, split into 4 specialists:
  - [expo-core](mobile/expo/expo-core/) — project foundation: `app.config`, CNG + `prebuild`, config plugins, Metro, Babel, env vars, monorepos, New Architecture, Hermes, deep-linking, debugging, bare workflow, Expo CLI
  - [expo-router](mobile/expo/expo-router/) — file-based routing: the `app/` tree, `_layout.tsx` navigators, route notation, `<Link>` + `useRouter()`, typed routes, `Stack.Protected` auth guards, modals, web API routes, React Navigation migration
  - [expo-sdk](mobile/expo/expo-sdk/) — the ~80 `expo-*` SDK packages by domain, Expo Modules API for authoring, push notifications deep-dive, Expo UI components
  - [eas](mobile/expo/eas/) — Expo Application Services cloud: Build / Submit / Update (the channel→branch match contract) / Workflows / Hosting (Cloudflare Workers) / `eas.json` schema / app signing

### `observability/` — analytics & monitoring

- [observability/plausible](observability/plausible/) — privacy-friendly cookieless web analytics (`script.js` + `plausible.init()`, custom events, v2 Stats API, Events API, Sites API, reverse proxy, Community Edition self-host)
- [observability/posthog](observability/posthog/) — all-in-one product analytics + session replay + feature flags + experiments + surveys + LLM observability + warehouse + CDP (`posthog-js` + server SDKs, HogQL, `getFeatureFlag` exposure semantics, reverse proxy with `api_host` + `ui_host`)

### `seo/` — search engine optimization (Google + web.dev + Schema.org)

- [seo/seo-core](seo/seo-core/) — Search Essentials (technical requirements + 18-item spam policies + best practices), the helpful-content framework + E-E-A-T rubric, title-link generation, meta-description controls, link best practices (`rel="nofollow"`/`"sponsored"`/`"ugc"` as hints not directives)
- [seo/seo-technical](seo/seo-technical/) — Googlebot taxonomy (incl. `Google-Extended` AI-training opt-out), robots.txt (RFC 9309), sitemaps, canonicalization, redirects, JavaScript SEO (the 3-phase crawl→render→index pipeline), mobile-first indexing, `hreflang`, Search Console, IndexNow
- [seo/seo-structured-data](seo/seo-structured-data/) — Schema.org + JSON-LD + the 26+ Google rich-result types, deprecated-and-must-remove types (HowTo 2023, FAQ for general sites 2026, sitelinks-searchbox 2024), Open Graph + Twitter/X Cards + Pinterest Rich Pins
- [seo/seo-performance](seo/seo-performance/) — Core Web Vitals: LCP (≤2.5s @ p75) + INP (replaced FID March 2024, ≤200ms @ p75) + CLS (≤0.1 @ p75), lab-vs-field distinction, CrUX 28-day window, Lighthouse, PageSpeed Insights, `web-vitals.js` for RUM

### `sports-data/` — sports & data APIs

- [sports-data/api-football](sports-data/api-football/) — API-Football v3 for football/soccer (1200+ leagues, fixtures, lineups, statistics, standings, odds; direct vs RapidAPI distribution, fixture status enum, `coverage` matrix, silent 200-with-`errors` quota footgun)
- [sports-data/the-odds-api](sports-data/the-odds-api/) — The Odds API V4 sports-betting odds JSON API (every endpoint, market key, bookmaker key, quota rule; `regions × markets` cost formula, 10-bookmaker = 1 region rule, historical snapshot envelope, error-code catalog)
- [sports-data/thesportsdb](sports-data/thesportsdb/) — TheSportsDB crowdsourced multi-sport database (V1 legacy PHP free with public test key, V2 modern REST behind Patreon paid tier, rich media/artwork CDN, livescore feed for the five tracked leagues, `idAPIfootball` cross-referencing, `{events: null}` transient-sync gotcha)

### Singletons (no domain folder yet)

- [dockerfile](dockerfile/) — the Dockerfile (instructions, parser directives, BuildKit `--mount`, multi-stage, secrets, cache backends, attestations, `.dockerignore`)
- [golang](golang/) — the Go programming language (spec, generics, concurrency, modules, testing, profiling, stdlib)
- [playwright](playwright/) — cross-browser end-to-end testing with `@playwright/test` (locators, web-first assertions, fixtures, projects, sharding, trace viewer, CI Docker image)
- [prompt-engineering](prompt-engineering/) — prompting Claude (the techniques + the Console tooling + the evaluation workflow that backs it)
- [rest-api](rest-api/) — REST/HTTP JSON API best practices distilled from Zalando + Google AIPs + Microsoft (Azure & Graph), grounded in RFC 9110 / 9111 / 9457 / 5789 / 7396 / 8594 / 8288 and IANA registries — surfaces tradeoffs where the three corpora disagree

More topics may be added over time — see [CONTRIBUTING.md](./CONTRIBUTING.md) for the scaffold.

## Contributing

Corrections, new topics, and feedback are welcome. Start with [CONTRIBUTING.md](./CONTRIBUTING.md) — it covers the editing flow, how to audit a claim against upstream docs, and how to add a new topic (including when to create a new domain folder vs drop in alongside existing singletons).

Found a fact that's wrong? Open an issue with the **Incorrect knowledge** template. Want a new agent for a tool we don't cover yet? Use the **New agent request** template — valid repository and/or docs URLs are required so the topic can actually be built.
