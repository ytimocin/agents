# Azure Resource Manager (ARM) agent prompts

Reference knowledge for [Azure Resource Manager](https://learn.microsoft.com/en-us/azure/azure-resource-manager/) — the deployment and management control plane for Azure and the JSON template (IaC) language that targets it. Covers the management model (the management group → subscription → resource group → resource scope hierarchy, control plane vs data plane, resource providers + types + registration, locks, tags, move operations), authoring ARM JSON templates (the template skeleton, per-scope `$schema` URLs, parameters/variables/outputs, the full built-in function catalog, `dependsOn` vs implicit dependencies, `copy` loops, conditions, languageVersion 2.0), running deployments (the four scopes, Incremental vs Complete mode, linked/nested templates, what-if, deployment stacks, deployment scripts), and the surrounding surfaces (Bicep relationship, the REST API shape, 429 token-bucket throttling, async-operation polling, service limits, best practices, and common errors).

Grounded in the official docs at https://learn.microsoft.com/en-us/azure/azure-resource-manager/, with inline `Full docs: <url>` links under every section so the agent can fetch upstream when it needs more detail.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/azure/azure-resource-manager/claude.md \
  -o ~/.claude/agents/azure-resource-manager-specialist.md

# Project-level
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/azure/azure-resource-manager/claude.md \
  -o .claude/agents/azure-resource-manager-specialist.md
```

The frontmatter registers it as a subagent named `azure-resource-manager-specialist`. Invoke it by asking Claude Code to "use the azure-resource-manager-specialist agent", or delegate programmatically via the `Agent` tool with `subagent_type: "azure-resource-manager-specialist"`.

The preamble directs the agent to WebFetch the linked upstream page on questions the summary doesn't fully cover, so it stays accurate as Azure evolves.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/azure/azure-resource-manager/codex.md \
  -o ~/.codex/AGENTS.md

# Per-project — scoped to the current directory
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/azure/azure-resource-manager/codex.md \
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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/azure/azure-resource-manager/copilot.md \
  -o .github/copilot-instructions.md
```

For an always-on personal setup (active in every directory), check `copilot --help` for the user-level custom-instructions path — last checked it lives under `~/.copilot/`.

---

## Updating

These files track the live Azure Resource Manager docs. To refresh, re-run the relevant `curl` above — nothing else is needed.

## Provenance and scope

- Built from the public docs at https://learn.microsoft.com/en-us/azure/azure-resource-manager/.
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. When in doubt, link the user to the canonical page.
- Claims not directly stated in the docs are explicitly hedged in-text (e.g., the resource-groups-can't-be-nested rule is flagged as unverified, and the variables limit cites the service-limits page over the best-practices page).
- ARM is the engine underneath both ARM JSON and Bicep — for new IaC authoring prefer Bicep. For the Azure networking *resources* themselves use the `azure-load-balancer`, `azure-virtual-network`, or `azure-nat-gateway` agents.
