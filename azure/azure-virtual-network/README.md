# Azure Virtual Network agent prompts

Reference knowledge for [Azure Virtual Network](https://learn.microsoft.com/en-us/azure/virtual-network/) and the connectivity/security primitives around it — VNets and subnets, IP addressing (the 5 reserved IPs, CIDR sizing), Network Security Groups and Application Security Groups, service tags, public IP addresses, user-defined routes and system routing, VNet peering (regional + global, hub-and-spoke), service endpoints, Private Link / Private Endpoints, Private Link Service, and Private DNS.

Grounded in the official docs at https://learn.microsoft.com/en-us/azure/virtual-network/ (and the Private Link / DNS doc sets), with inline `Full docs: <url>` links under every section so the agent can fetch upstream when it needs more detail.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/azure/azure-virtual-network/claude.md \
  -o ~/.claude/agents/azure-virtual-network-specialist.md

# Project-level
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/azure/azure-virtual-network/claude.md \
  -o .claude/agents/azure-virtual-network-specialist.md
```

The frontmatter registers it as a subagent named `azure-virtual-network-specialist`. Invoke it by asking Claude Code to "use the azure-virtual-network-specialist agent", or delegate programmatically via the `Agent` tool with `subagent_type: "azure-virtual-network-specialist"`.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/azure/azure-virtual-network/codex.md \
  -o ~/.codex/AGENTS.md

# Per-project — scoped to the current directory
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/azure/azure-virtual-network/codex.md \
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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/azure/azure-virtual-network/copilot.md \
  -o .github/copilot-instructions.md
```

For an always-on personal setup (active in every directory), check `copilot --help` for the user-level custom-instructions path — last checked it lives under `~/.copilot/`.

---

## Updating

These files track the live Azure Virtual Network docs. To refresh, re-run the relevant `curl` above — nothing else is needed.

## Provenance and scope

- Built from the public docs at https://learn.microsoft.com/en-us/azure/virtual-network/ plus the Private Link and Azure DNS doc sets.
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. When in doubt, link the user to the canonical page.
- Claims not directly stated in the docs are explicitly hedged in-text; soft service limits are flagged as "confirm on the limits page."
- For the Load Balancer data path use the `azure-load-balancer` agent; for outbound NAT gateway internals use the `azure-nat-gateway` agent.
