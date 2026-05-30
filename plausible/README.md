# Plausible agent prompts

Reference knowledge for [Plausible Analytics](https://plausible.io/) — the lightweight, cookie-less, GDPR-friendly web analytics product, available as a SaaS (Cloud) and as an open-source self-host distribution (Community Edition). Aggregate-only data model: no individual user profiles, no session replay, no cross-site tracking, no cookie banner required — *"unique visitors"* is a daily-rotating salted hash of `(IP + UA + domain)`, not a persistent identifier.

Covers the tracking script (the bare `script.js` plus stackable file-based variants for hash routing, outbound links, file downloads, exclusions, manual mode, tagged events, pageview-props, revenue, IE-compat, and localhost; and the modern `@plausible-analytics/tracker` npm package with `plausible.init({ hashBasedRouting, outboundLinks, fileDownloads, customProperties, formSubmissions, captureOnLocalhost, autoCapturePageviews, endpoint, transformRequest })`), custom event goals (the `plausible('EventName', { props, revenue, callback })` call and the CSS-class `plausible-event-name=...` declarative syntax), custom properties (scalars only, ≤30 per event, no PII, Business plan), funnels (Business, 2–8 steps), ecommerce revenue tracking (Business, ISO 4217 currency), SPA tracking (`pushState` automatic, hash routing needs the hash variant, Next.js double-counting workaround), the v2 Stats API (single `POST /api/v2/query` endpoint, bearer auth, 600 req/hr, full metric and dimension list including `visit:utm_source`/`event:props:<name>`/`time:day`, period values `7d`/`28d`/`6mo`/`12mo`/`all`/etc.), the Events API for server-side ingestion (`POST /api/event` with mandatory raw `User-Agent` and `X-Forwarded-For` headers — without them the bot filter drops events silently), the Enterprise-only Sites API (programmatic site, goal, and shared-link CRUD), reverse proxying via Nginx/Vercel/Netlify/Cloudflare/Caddy/Apache (with the *avoid path names like `analytics`/`stats`/`plausible`* rule), excluding traffic (page wildcards in Shields → Pages, IP block list, the `localStorage.plausible_ignore` per-domain flag, default-dropped localhost, automatic IAB bot filter), shared links and embedded dashboards, GA4 import (GA4-only, daily aggregates, 5-property cap, blocked by GA4's 2-month retention default), teams and role-based access (Owner/Admin/Editor/Billing/Viewer/Guest variants), and operating Community Edition (Docker Compose, ClickHouse SSE 4.2 / NEON CPU requirement, paid-Cloud-features missing). Grounded in the live docs at https://plausible.io/docs, with inline `Full docs: <url>` links under every section so the agent can fetch upstream when it needs more detail.

## Files

| File | Target tool | Format |
|------|-------------|--------|
| `claude.md` | Claude Code | Markdown with YAML frontmatter (`name`, `description`, `model`, `tools`) |
| `codex.md` | OpenAI Codex | Plain markdown (no frontmatter) |
| `copilot.md` | GitHub Copilot | Plain markdown (no frontmatter) |

The three files share the same body — only the frontmatter differs so each tool can parse it.

---

## Install

### Claude Code

Drop the file into your agents directory — user-level (available in every session) or project-level (this repo only):

```bash
# User-level (recommended — reusable across all projects)
mkdir -p ~/.claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/plausible/claude.md \
  -o ~/.claude/agents/plausible-specialist.md

# Project-level
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/plausible/claude.md \
  -o .claude/agents/plausible-specialist.md
```

The frontmatter registers it as a subagent named `plausible-specialist`. Invoke it by asking Claude Code to "use the plausible-specialist agent", or delegate programmatically via the `Agent` tool with `subagent_type: "plausible-specialist"`.

---

### OpenAI Codex

**1. Install Codex CLI** and authenticate (`codex login` or set `OPENAI_API_KEY`):

```bash
brew install codex            # or: npm install -g @openai/codex
codex --version
```

**2. Drop the prompt into Codex's instruction path.** Two options — pick based on scope:

```bash
# Global — active in every Codex session
mkdir -p ~/.codex
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/plausible/codex.md \
  -o ~/.codex/AGENTS.md

# Per-project — scoped to the current directory
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/plausible/codex.md \
  -o AGENTS.md
```

Codex merges `AGENTS.md` files up the directory tree — either works. Run `codex` in your target directory; the startup banner lists the loaded path next to `Agents.md:` so you can confirm it's picked up.

---

### GitHub Copilot CLI

The standalone terminal tool. For VS Code or other IDEs, drop the same file at `.github/copilot-instructions.md` per repository and enable **GitHub › Copilot › Chat › Code Generation: Use Instruction Files** in settings.

**1. Install and authenticate:**

```bash
npm install -g @github/copilot
copilot       # first launch walks through GitHub sign-in
```

Requires a Copilot subscription. Run `copilot --help` if command names differ — this CLI moves fast.

**2. Install the prompt into a workspace.** Copilot CLI reads `.github/copilot-instructions.md` from the directory it's launched in:

```bash
mkdir -p .github
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/plausible/copilot.md \
  -o .github/copilot-instructions.md
```

For an always-on personal setup (active in every directory), check `copilot --help` for the user-level custom-instructions path — last checked it lives under `~/.copilot/`.

**3. Launch** with `copilot` in the workspace.

---

## Updating

These files track the live Plausible docs. To refresh, re-run the relevant `curl` above — nothing else is needed.

## Provenance and scope

- Built from the public docs at https://plausible.io/docs and the open-source repos at https://github.com/plausible/analytics (cloud source) and https://github.com/plausible/community-edition (self-host).
- Default flavor: Cloud-hosted Plausible with the standard JS tracker. Community Edition (self-host) is documented as a distinct surface with its own constraints (Docker Compose deployment, ClickHouse CPU instruction-set requirement, paid-Cloud features unavailable).
- Plausible's API moved from v1 (per-resource paths) to v2 (single `POST /api/v2/query`) for the Stats API, and the tracker is migrating from file-based script variants (`script.outbound-links.exclusions.js`) toward `@plausible-analytics/tracker` with `plausible.init({...})`. The preamble instructs the agent to WebFetch the relevant upstream page for version-sensitive specifics rather than asserting from memory.
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. When in doubt, link the user to the canonical page.
- Claims not directly stated in the docs are explicitly hedged in-text.
