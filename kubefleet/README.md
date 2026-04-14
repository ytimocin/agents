# KubeFleet agent prompts

Reference knowledge for [KubeFleet](https://kubefleet.dev/) — multi-cluster Kubernetes management via hub-and-spoke placement, scheduling, staged rollouts, overrides, drift detection, and eviction.

Covers concepts, how-tos, API groups/versions, troubleshooting conditions, and CLI quick-reference. Grounded in the official docs at https://kubefleet.dev/docs.

## Files

| File | Target tool | Format |
|------|-------------|--------|
| `claude.md` | Claude Code | Markdown with YAML frontmatter (`name`, `description`, `model`, `tools`) |
| `codex.md` | OpenAI Codex | Plain markdown (no frontmatter) |
| `copilot.md` | GitHub Copilot | Plain markdown (no frontmatter) |

## Install

### Claude Code

Drop `claude.md` into your agents directory — user-level (available in every session) or project-level (this repo only):

```bash
# User-level (recommended — reusable across all projects)
mkdir -p ~/.claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/kubefleet/claude.md \
  -o ~/.claude/agents/kubefleet-specialist.md

# Project-level
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/kubefleet/claude.md \
  -o .claude/agents/kubefleet-specialist.md
```

The frontmatter registers it as a subagent named `kubefleet-specialist`. Invoke it by asking Claude Code to "use the kubefleet-specialist agent" or by delegating via the `Agent` tool with `subagent_type: "kubefleet-specialist"`.

### OpenAI Codex

Codex reads `AGENTS.md` from the repo root (and merges nested ones as you descend into subdirectories). Two options:

```bash
# Option A: drop in as the project's AGENTS.md
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/kubefleet/codex.md \
  -o AGENTS.md

# Option B: append to an existing AGENTS.md
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/kubefleet/codex.md \
  >> AGENTS.md
```

User-level instructions live in `~/.codex/AGENTS.md` if you want it active across all Codex projects.

### GitHub Copilot

Copilot reads `.github/copilot-instructions.md` per repository:

```bash
mkdir -p .github
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/kubefleet/copilot.md \
  -o .github/copilot-instructions.md
```

Enable **Code referencing > Use instruction files** in your Copilot settings if it isn't already on. Copilot will pick up the file on the next interaction in that repo.

## Updating

These files track the live KubeFleet docs. To refresh, re-run the relevant `curl` above — nothing else is needed.

## Provenance and scope

- Built from the public docs at https://kubefleet.dev/docs and the repo at https://github.com/kubefleet-dev/kubefleet.
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. When in doubt, link the user to the canonical page.
- Known soft claims (not directly stated in docs) are explicitly hedged in-text.
