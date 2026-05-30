# API-Football agent prompts

Reference knowledge for [API-Football](https://www.api-football.com/) v3 — the REST API for football (soccer) data covering **1200+ leagues and cups across 170+ countries** with livescores, fixtures, lineups, events, statistics, standings, players, coaches, transfers, predictions, and odds (pre-match and in-play). API-Football is sport-specific; api-sports.io operates sibling APIs for AFL, baseball, basketball, F1, handball, hockey, MMA, NBA, NFL/NCAA, rugby, and volleyball on their own hosts.

Covers the **two distribution channels** (direct `https://v3.football.api-sports.io/` with `x-apisports-key` vs the RapidAPI mirror at `https://api-football-v1.p.rapidapi.com/v3/` with `x-rapidapi-key` + `x-rapidapi-host`), the standard response envelope (`get` / `parameters` / `errors` / `paging` / `results` / `response`), the four published plan tiers and their per-day quotas and per-minute rate-limit ceilings (Free $0 / 100 req-per-day / 10 req-per-min; Pro $19 / 7,500 / 300; Ultra $29 / 75,000 / 450; Mega $39 / 150,000 / 900 — Custom up to 1.5M/day), the **24-hour rolling-window quota reset anchored to subscription anniversary** (not midnight UTC), the rate-limit headers in both distributions (`x-ratelimit-requests-limit` / `-remaining` on direct, `X-RateLimit-Limit` / `-Remaining` on RapidAPI), every endpoint grouped by domain — status/timezone, countries/leagues/seasons, teams/venues/statistics, standings, the fixtures family (`/fixtures`, `/fixtures/rounds`, `/fixtures/headtohead`, `/fixtures/statistics`, `/fixtures/events`, `/fixtures/lineups`, `/fixtures/players`), injuries, predictions, coaches, trophies, sidelined, players/transfers, and the odds family (`/odds`, `/odds/live`, `/odds/mapping`, `/odds/bookmakers`, `/odds/bets`) — the canonical fixture status machine (`NS`, `1H`, `HT`, `2H`, `FT`, `AET`, `PEN`, `BT`, `SUSP`, `INT`, `PST`, `CANC`, `ABD`, `AWD`, `WO`, `LIVE`), per-endpoint pagination defaults (the inconsistent `/players: 20`, `/players/profiles: 250`, `/odds: 10`, `/odds/mapping: 100`, and the silent failure mode when `paging.total > 1`), the `coverage` matrix that gates which leagues actually carry lineups/events/odds/predictions, and the published anti-patterns (the strict CORS firewall that rejects requests with default axios/fetch headers; the silent-200-with-`errors`-still-counts-against-quota footgun; pre-match vs in-play bet-ID non-interchangeability). Grounded in the live OpenAPI spec at https://api-sports.io/public/documentations/football-v3.yaml and the docs at https://www.api-football.com/documentation-v3, with inline `Full docs: <url>` links under every section so the agent can fetch upstream when it needs more detail.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/api-football/claude.md \
  -o ~/.claude/agents/api-football-specialist.md

# Project-level
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/api-football/claude.md \
  -o .claude/agents/api-football-specialist.md
```

The frontmatter registers it as a subagent named `api-football-specialist`. Invoke it by asking Claude Code to "use the api-football-specialist agent", or delegate programmatically via the `Agent` tool with `subagent_type: "api-football-specialist"`.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/api-football/codex.md \
  -o ~/.codex/AGENTS.md

# Per-project — scoped to the current directory
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/api-football/codex.md \
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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/api-football/copilot.md \
  -o .github/copilot-instructions.md
```

For an always-on personal setup (active in every directory), check `copilot --help` for the user-level custom-instructions path — last checked it lives under `~/.copilot/`.

**3. Launch** with `copilot` in the workspace.

---

## Updating

These files track the live API-Football OpenAPI spec and docs. To refresh, re-run the relevant `curl` above — nothing else is needed. League coverage, response fields, and the `coverage` flags change in place between audits; quote https://api-sports.io/public/documentations/football-v3.yaml for the authoritative shape and https://www.api-football.com/pricing for current quotas.

## Provenance and scope

- Built from the published OpenAPI spec (https://api-sports.io/public/documentations/football-v3.yaml — v3.9.3 / 808 KB at audit), the docs site at https://www.api-football.com/documentation-v3, the rate-limit blog post at https://www.api-football.com/news/post/how-ratelimit-works, and the pricing page at https://www.api-football.com/pricing.
- Snapshot date: **2026-05-30**. The OpenAPI spec is the source of truth for endpoint shapes; pricing and per-plan rate-limit ceilings drift in place — verify the pricing page before quoting to a customer.
- **Football (soccer) only.** The sibling APIs (basketball, NBA, NFL, F1, …) live at their own hosts under `*.api-sports.io` and are out of scope for this agent.
- Both distribution channels (direct api-sports.io and RapidAPI mirror) carry the same endpoint paths but **different auth headers and slightly different rate-limit header names** — the prompt documents both so a single SDK can target either.
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. When in doubt, link the user to the canonical page.
- Claims not directly stated in the docs are explicitly hedged in-text (notably: the 24-hour rolling-window quota anchored to subscription anniversary, the strict CORS firewall, and the silent quota burn on 200-with-`errors` responses are sourced from the API-Football blog and community reports, not the OpenAPI spec).
