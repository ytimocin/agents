# Hubble agent prompts

Reference knowledge for [Hubble](https://docs.cilium.io/en/stable/observability/hubble/) — the eBPF-based networking, service, and security observability layer built on Cilium. Covers the architecture (Hubble server, Relay, UI, CLI, Peer service, ports), enabling via the Cilium CLI and Helm, the `hubble observe` filter surface, the network flow schema and `flow.proto` enums (verdicts, drop reasons, trace points), L7 visibility (HTTP/DNS/Kafka via L7 policy or the `io.cilium.proxy-visibility` annotation) and redaction, metrics (port 9965, metric families, context options, OpenMetrics, Grafana), flow export (static + dynamic exporter), the Hubble UI, TLS/mTLS, and the Observer gRPC API.

Grounded in the official docs at https://docs.cilium.io/en/stable/observability/ and the canonical `cilium/cilium` API protos, with inline `Full docs: <url>` links under every section so the agent can fetch upstream when it needs more detail.

This is the deep companion to the [`cilium`](../cilium/) agent, which carries only a summary-level Hubble section. For the Cilium datapath, CiliumNetworkPolicy enforcement, kube-proxy replacement, Cluster Mesh, or BGP, use the `cilium` agent.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/cloud-native/hubble/claude.md \
  -o ~/.claude/agents/hubble-specialist.md

# Project-level
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/cloud-native/hubble/claude.md \
  -o .claude/agents/hubble-specialist.md
```

The frontmatter registers it as a subagent named `hubble-specialist`. Invoke it by asking Claude Code to "use the hubble-specialist agent", or delegate programmatically via the `Agent` tool with `subagent_type: "hubble-specialist"`.

The preamble directs the agent to WebFetch the linked upstream page on questions the summary doesn't fully cover, so it stays accurate as Hubble evolves.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/cloud-native/hubble/codex.md \
  -o ~/.codex/AGENTS.md

# Per-project — scoped to the current directory
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/cloud-native/hubble/codex.md \
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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/cloud-native/hubble/copilot.md \
  -o .github/copilot-instructions.md
```

For an always-on personal setup (active in every directory), check `copilot --help` for the user-level custom-instructions path — last checked it lives under `~/.copilot/`.

---

## Updating

These files track the live Cilium/Hubble docs. To refresh, re-run the relevant `curl` above — nothing else is needed.

## Provenance and scope

- Built from the public docs at https://docs.cilium.io/en/stable/observability/ and the `cilium/cilium` API protos (`api/v1/flow`, `api/v1/observer`).
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. When in doubt, link the user to the canonical page.
- Claims not directly stated in the docs are explicitly hedged in-text (e.g., the flow-export rotation key scope).
- For the Cilium datapath and policy enforcement, use the `cilium` agent.
