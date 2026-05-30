# PostHog agent prompts

Reference knowledge for [PostHog](https://posthog.com/) — the open-source product analytics platform that also bundles session replay, feature flags, experiments, surveys, error tracking, web analytics, LLM observability, a data warehouse, and a customer data platform. One event stream, many products: a `$pageview` from `posthog-js` powers product analytics, web analytics, heatmaps, and replay simultaneously.

Covers the JavaScript Web SDK (full `posthog.init()` config table, every method on the `posthog` object, autocapture and rage/dead-click signals, replay privacy hooks like `maskAllInputs` / `maskTextSelector` / `ph-no-capture`), identification (`identify`/`alias`/`reset`, `person_profiles: 'identified_only'` vs `'always'`, groups for B2B), the Python and Node.js server SDKs (including `evaluateFlags`/`evaluate_flags`, local evaluation with `personalApiKey`, and `shutdown()` for serverless), feature flags and experiments (and the rule that *only `getFeatureFlag` records an exposure*), HogQL (the ClickHouse-flavored SQL layer with `events`/`persons`/`sessions`/warehouse tables and the `/api/projects/:id/query` endpoint), the REST API surface (the `.i.posthog.com` public ingest host vs the bare `posthog.com` private API host, US vs EU regions, rate limits per tier), data pipelines and the warehouse, error tracking (`$exception`), LLM observability (40+ providers, traces vs generations, automatic cost), reverse proxying (`api_host` + `ui_host`), self-host scope ("Cloud recommended; paid features Cloud-only; Kubernetes self-host no longer supported"), and a troubleshooting guide for the common failure modes (ad-blocker drops, missed exposures, MAU spikes, replay PII leaks). Grounded in the live docs at https://posthog.com/docs, with inline `Full docs: <url>` links under every section so the agent can fetch upstream when it needs more detail.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/posthog/claude.md \
  -o ~/.claude/agents/posthog-specialist.md

# Project-level
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/posthog/claude.md \
  -o .claude/agents/posthog-specialist.md
```

The frontmatter registers it as a subagent named `posthog-specialist`. Invoke it by asking Claude Code to "use the posthog-specialist agent", or delegate programmatically via the `Agent` tool with `subagent_type: "posthog-specialist"`.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/posthog/codex.md \
  -o ~/.codex/AGENTS.md

# Per-project — scoped to the current directory
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/posthog/codex.md \
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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/posthog/copilot.md \
  -o .github/copilot-instructions.md
```

For an always-on personal setup (active in every directory), check `copilot --help` for the user-level custom-instructions path — last checked it lives under `~/.copilot/`.

**3. Launch** with `copilot` in the workspace.

---

## Updating

These files track the live PostHog docs. To refresh, re-run the relevant `curl` above — nothing else is needed.

## Provenance and scope

- Built from the public docs at https://posthog.com/docs and the repo at https://github.com/PostHog/posthog.
- Default flavor: JavaScript Web SDK (`posthog-js`) for instrumentation and HogQL for querying, with the `posthog-node` and `posthog-python` server SDKs for backend feature-flag evaluation and ingestion. Mobile SDKs (iOS, Android, React Native, Flutter) and the less-common server libraries (Ruby, PHP, Go, Java, .NET, Elixir, Rust) are linked in the preamble so the agent can pivot when needed.
- PostHog ships changes weekly — config keys do get renamed (e.g. `advanced_disable_decide` → `advanced_disable_flags`, `feature_enabled` → `evaluate_flags`). The preamble instructs the agent to WebFetch the relevant upstream page for version-sensitive specifics rather than asserting from memory.
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. When in doubt, link the user to the canonical page.
- Claims not directly stated in the docs are explicitly hedged in-text.
