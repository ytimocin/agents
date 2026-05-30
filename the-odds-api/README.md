# The Odds API agent prompts

Reference knowledge for [The Odds API V4](https://the-odds-api.com/) — a JSON HTTP API for sports betting odds, scores, events, and historical snapshots covering **190+ sport/league keys** and **100+ bookmakers** across US, UK, EU, FR, SE, and AU markets. Every request returns the standard envelope of headers (`x-requests-remaining` / `x-requests-used` / `x-requests-last`) plus a per-endpoint JSON body; quota cost is computed off the `markets × regions × (1 if data else 0)` formula, with the *10-bookmaker = 1 region* billing rule and the *empty-response-doesn't-charge* rule baked in.

Covers authentication and base URLs (including the IPv6 alternate `https://ipv6-api.the-odds-api.com/v4`), pricing tiers (Free 500 / 20K $30 / 100K $59 / 5M $119 / 15M $249 monthly credits, calendar-month reset on the 1st UTC), rate limits (~30 req/sec hard cap with HTTP 429 + retry after ~2 s), the full error-code catalog (`MISSING_KEY`, `INVALID_KEY`, `DEACTIVATED_KEY`, `EXCEEDED_FREQ_LIMIT`, `OUT_OF_USAGE_CREDITS`, `INVALID_MARKET_COMBO`, `HISTORICAL_UNAVAILABLE_ON_FREE_USAGE_PLAN`, `HISTORICAL_MARKETS_UNAVAILABLE_AT_DATE`, …), every endpoint (`/sports`, `/sports/{sport}/odds`, `/sports/{sport}/scores` with the `daysFrom` window, `/sports/{sport}/events`, `/sports/{sport}/events/{eventId}/odds`, `/sports/{sport}/participants`, and the `/historical/...` family), the published market catalog (h2h, spreads, totals, outrights, alternate lines, period markets, and the per-sport player-prop families for NFL/NBA/MLB/NHL/soccer/golf/tennis/MMA), the live bookmaker lists per region (`us`/`us2`/`uk`/`eu`/`au`/`fr`/`se` snapshots with state-specific entries like `hardrockbet_az`/`_fl`/`_oh`), the published update intervals (featured 60 s pre-match / 40 s in-play; additional 60/60; outrights 5 min/60 s; exchanges 30/20; the 6-hour-out ramp), the historical-odds family (5-minute granularity since Sep 2022, additional markets historical from `2023-05-03T05:30:00Z`, the snapshot-envelope `{timestamp, previous_timestamp, next_timestamp, data}` shape, and the "closest snapshot equal to or earlier" semantics), the rotation numbers release on `2025-11-04`, and the anti-patterns that silently torch quota (querying every sport every minute, ignoring `x-requests-remaining`, not caching `/sports`). Grounded in the live docs at https://the-odds-api.com/liveapi/guides/v4/, with inline `Full docs: <url>` links under every section so the agent can fetch upstream when it needs more detail.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/the-odds-api/claude.md \
  -o ~/.claude/agents/the-odds-api-specialist.md

# Project-level
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/the-odds-api/claude.md \
  -o .claude/agents/the-odds-api-specialist.md
```

The frontmatter registers it as a subagent named `the-odds-api-specialist`. Invoke it by asking Claude Code to "use the the-odds-api-specialist agent", or delegate programmatically via the `Agent` tool with `subagent_type: "the-odds-api-specialist"`.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/the-odds-api/codex.md \
  -o ~/.codex/AGENTS.md

# Per-project — scoped to the current directory
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/the-odds-api/codex.md \
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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/the-odds-api/copilot.md \
  -o .github/copilot-instructions.md
```

For an always-on personal setup (active in every directory), check `copilot --help` for the user-level custom-instructions path — last checked it lives under `~/.copilot/`.

**3. Launch** with `copilot` in the workspace.

---

## Updating

These files track the live Odds API docs. To refresh, re-run the relevant `curl` above — nothing else is needed. The bookmaker lists per region (`us`/`us2`/`uk`/`eu`/`au`/`fr`/`se`) churn most often; if you need an authoritative snapshot, hit https://the-odds-api.com/sports-odds-data/bookmaker-apis.html directly.

## Provenance and scope

- Built from the public docs at https://the-odds-api.com/liveapi/guides/v4/ and the supporting pages (https://the-odds-api.com/sports-odds-data/sports-apis.html, `/bookmaker-apis.html`, `/betting-markets.html`, `/update-intervals.html`, `/historical-odds-data/`, `/liveapi/guides/v4/api-error-codes.html`, `/manage/faqs.html`, `/account/`, `/releases/rotation-numbers.html`).
- Snapshot date: **2026-05-30**. Pricing tiers, bookmaker rosters per region, and the rotation-numbers release date are all timestamped — verify the current pricing page before quoting to a customer; bookmaker keys can be added/paused between audits.
- The Odds API exposes one versioned surface (V4) at `https://api.the-odds-api.com/v4`. The historical-odds family is a paid-only add-on that ships under the same V4 path tree — covered here in its own section.
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. When in doubt, link the user to the canonical page.
- Claims not directly stated in the docs are explicitly hedged in-text.
