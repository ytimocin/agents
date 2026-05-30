# TheSportsDB agent prompts

Reference knowledge for [TheSportsDB](https://www.thesportsdb.com/) — a crowdsourced, multi-sport database that ships a free JSON sports API. Covers all major sports (soccer, NBA, NFL, NHL, MLB, F1, motorsports, esports, …), excels at **rich media** (team badges, jerseys, stadium photos, league posters, player cutouts/fanart) delivered through the artwork CDN, runs a **livescore feed** for the five tracked leagues, and exposes shared external IDs (`idAPIfootball`, `idSoccerXML`, `idWikidata`) for cross-referencing with other data providers.

Covers the **two parallel APIs** — V1 legacy PHP (URL pattern `https://www.thesportsdb.com/api/v1/json/{API_KEY}/<endpoint>.php`, free with the documented test key `3` or the in-example `123`) and V2 modern REST (header-based Patreon-tier auth, richer schemas, livescore endpoints) — every V1 endpoint grouped by purpose (search: `searchteams.php`, `searchplayers.php`, `searchevents.php`, `searchvenues.php`; lookup-by-ID: `lookupteam.php`, `lookupplayer.php`, `lookupleague.php`, `lookupevent.php`, `lookupvenue.php`, `lookuptable.php`, `lookuphonours.php` (British spelling — matches the API), `lookupcontracts.php`, `lookupformerteams.php`; lists: `all_leagues.php`, `all_sports.php`, `all_countries.php`, `search_all_leagues.php`, `search_all_teams.php`; schedules: `eventsnext.php`, `eventslast.php`, `eventsday.php`, `eventsseason.php`, `eventsnextleague.php`, `eventspastleague.php`; livescore: **V2 only** (V1 `livescore.php` is deprecated per current docs); TV: `eventstv.php`), the V2 REST paths and how the response shape differs from V1, the Patreon tier model (no unlimited plan exists at any price — paid tiers just raise rate-limit ceilings and unlock V2 paths), media URL conventions and the `/preview` thumbnail suffix for badges/jerseys/stadium photos, the **null-vs-empty-array gotcha** (every list endpoint wraps in `{ "events": null }` not `{ "events": [] }` when empty, which silently breaks naive `Array.isArray()` checks), the **`{ "events": null }` transient-sync state** on V2 livescore and `eventsnextleague` (community workaround: retry once after ~2 s — admin-acknowledged), the **unreliable `strStatus` field** (project staff confirmed it's not authoritative — compute finished-state from `dateEvent`/`strTimestamp` + 120 min instead), the **rotating 9-digit `idLiveScore`** that the docs themselves describe as "not useful" (key off `idEvent` instead), the cross-referencing IDs that connect TheSportsDB entities to API-Football / SoccerXML / Wikidata, and the operating-mode recommendations (cache `/lookup*` aggressively, use the test key for dev only, expect community-edited data quality, never hardcode media URLs because they migrate). Grounded in the live docs at https://www.thesportsdb.com/documentation and the two OpenAPI specs at `/api/spec/v1/openapi.yaml` and `/api/spec/v2/openapi.yaml`, with inline `Full docs: <url>` links under every section so the agent can fetch upstream when it needs more detail.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/thesportsdb/claude.md \
  -o ~/.claude/agents/thesportsdb-specialist.md

# Project-level
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/thesportsdb/claude.md \
  -o .claude/agents/thesportsdb-specialist.md
```

The frontmatter registers it as a subagent named `thesportsdb-specialist`. Invoke it by asking Claude Code to "use the thesportsdb-specialist agent", or delegate programmatically via the `Agent` tool with `subagent_type: "thesportsdb-specialist"`.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/thesportsdb/codex.md \
  -o ~/.codex/AGENTS.md

# Per-project — scoped to the current directory
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/thesportsdb/codex.md \
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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/thesportsdb/copilot.md \
  -o .github/copilot-instructions.md
```

For an always-on personal setup (active in every directory), check `copilot --help` for the user-level custom-instructions path — last checked it lives under `~/.copilot/`.

**3. Launch** with `copilot` in the workspace.

---

## Updating

These files track the live TheSportsDB docs and the V1/V2 OpenAPI specs. To refresh, re-run the relevant `curl` above — nothing else is needed. The V2 surface is the one that drifts most often; quote the OpenAPI specs (https://www.thesportsdb.com/api/spec/v1/openapi.yaml, https://www.thesportsdb.com/api/spec/v2/openapi.yaml) for authoritative paths and shapes.

## Provenance and scope

- Built from the public docs at https://www.thesportsdb.com/documentation, the marketing/landing pages at https://www.thesportsdb.com/free_sports_api and `/api.php`, the data-dictionary and artwork pages (`/docs_api_data`, `/docs_artwork.php`, `/docs_api_examples`, `/docs_api_testing`, `/docs_libraries`), the Patreon tier list at https://www.patreon.com/thedatadb, and the V1/V2 OpenAPI specs at `/api/spec/v1/openapi.yaml` and `/api/spec/v2/openapi.yaml`. Several behaviors (the `{ "events": null }` transient-sync state, the unreliable `strStatus`, the rotating `idLiveScore`, the no-unlimited-plan rule) are forum-confirmed by project staff and cited inline.
- Snapshot date: **2026-05-30**. Patreon tier pricing and the V2 endpoint surface drift; verify https://www.thesportsdb.com/pricing and https://www.patreon.com/thedatadb before quoting plan limits to a customer.
- **All sports.** Soccer, NBA, NFL, NHL, MLB, F1, motorsports, esports — TheSportsDB is multi-sport by design. Livescore coverage is narrower (the five tracked leagues at audit).
- TheSportsDB is **community-edited**. Accuracy varies by league/sport; obscure leagues may have stale rosters, missing translations, or out-of-date logos. Treat it as a media-rich complement to a primary data provider, not the single source of truth.
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. When in doubt, link the user to the canonical page.
- Claims not directly stated in the docs are explicitly hedged in-text.
