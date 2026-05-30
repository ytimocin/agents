# Prompt engineering agent prompts

Reference knowledge for **prompting Claude** — the discipline (clarity, examples, XML, thinking, agentic patterns), the Console tooling (prompt generator, templates, improver), and the evaluation workflow (success criteria, eval design, the Console eval tool, LLM-as-judge).

Built from Anthropic's live docs at https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview and https://platform.claude.com/docs/en/test-and-evaluate/develop-tests. Every `##` section ends with a `Full docs: <url>` so the agent can WebFetch upstream when an edge case isn't covered in the summary.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/prompt-engineering/claude.md \
  -o ~/.claude/agents/prompt-engineering-specialist.md

# Project-level
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/prompt-engineering/claude.md \
  -o .claude/agents/prompt-engineering-specialist.md
```

The frontmatter registers it as a subagent named `prompt-engineering-specialist`. Invoke it by asking Claude Code to "use the prompt-engineering-specialist agent", or delegate programmatically via the `Agent` tool with `subagent_type: "prompt-engineering-specialist"`.

When loaded correctly, the subagent reaches for upstream docs on questions the summary doesn't fully cover — the preamble directs it to WebFetch the linked best-practices/eval/prompting-tools pages before answering.

---

### OpenAI Codex

**1. Install Codex CLI** and authenticate (`codex login` or set `OPENAI_API_KEY`):

```bash
brew install codex            # or: npm install -g @openai/codex
codex --version
```

**2. Drop the prompt into Codex's instruction path.** Two options:

```bash
# Global — active in every Codex session
mkdir -p ~/.codex
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/prompt-engineering/codex.md \
  -o ~/.codex/AGENTS.md

# Per-project — scoped to the current directory
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/prompt-engineering/codex.md \
  -o AGENTS.md
```

Codex merges `AGENTS.md` files up the directory tree — either works. The startup banner lists the loaded path next to `Agents.md:`.

---

### GitHub Copilot CLI

Drop into `.github/copilot-instructions.md` per repository (works for the standalone CLI and for VS Code with **GitHub › Copilot › Chat › Code Generation: Use Instruction Files** enabled):

```bash
mkdir -p .github
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/prompt-engineering/copilot.md \
  -o .github/copilot-instructions.md
```

For an always-on personal setup, check `copilot --help` for the user-level instructions path (typically under `~/.copilot/`).

---

## Pairs with the prompt-reviewer workflow agents

This topic provides the **reference checklist**. Two complementary workflow agents live in this repo at `.claude/agents/` and apply that checklist to real prompts:

- **`prompt-reviewer-code`** — locates LLM call sites in code, reconstructs the resolved prompt across templates, embeds, builders, and conditionals, cites file:line for every fragment, then applies the checklist.
- **`prompt-reviewer-logs`** — reads sent-prompt / response pairs from any database (Postgres, MongoDB, MySQL, BigQuery, SQLite, ClickHouse, DuckDB) via standard CLIs, aggregates output-side signals (refusal rate, format adherence, drift, cohort failures, injection evidence), then applies the same checklist.

Install them user-wide so they're available in every Claude Code session:

```bash
mkdir -p ~/.claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/.claude/agents/prompt-reviewer-code.md \
  -o ~/.claude/agents/prompt-reviewer-code.md
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/.claude/agents/prompt-reviewer-logs.md \
  -o ~/.claude/agents/prompt-reviewer-logs.md
```

Or project-scoped:

```bash
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/.claude/agents/prompt-reviewer-code.md \
  -o .claude/agents/prompt-reviewer-code.md
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/.claude/agents/prompt-reviewer-logs.md \
  -o .claude/agents/prompt-reviewer-logs.md
```

Both agents resolve the checklist file from this order: `prompt-engineering/knowledge.md` in the current repo → `~/.claude/agents/prompt-engineering-specialist.md` → live upstream via WebFetch. Install `prompt-engineering-specialist` (above) so the user-level fallback exists.

---

## Updating

Re-run the relevant `curl` above. These files track the live Anthropic docs; refreshing pulls the latest audit.

## Scope and provenance notes

- Covers Claude 4.5 / 4.6 / 4.7 / 4.8 (NextOpus) prompting; cross-references feature docs (adaptive thinking, effort, structured outputs, context awareness, memory tool, agent skills) inline via `Full docs:` links.
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs — link the user to the canonical page when in doubt.
- Claims not directly stated in the docs are explicitly hedged in-text.
