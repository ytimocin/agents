# agents

Agent prompts for [Claude Code](https://docs.claude.com/en/docs/claude-code), [OpenAI Codex](https://github.com/openai/codex), and [GitHub Copilot](https://docs.github.com/en/copilot).

Each topic folder contains three variants of the same knowledge base — one per tool — because each harness expects a different file format and install location.

## Layout

```
agents/
  kubefleet/
    claude.md     # Claude Code subagent (with YAML frontmatter)
    codex.md      # Codex AGENTS.md body
    copilot.md    # GitHub Copilot instructions body
    README.md     # per-topic install instructions
```

## How to use

Pick the topic folder you care about and follow its `README.md` for install instructions. The three files within a folder share the same body; only the header differs so each tool can parse it.

## Topics

- [kubefleet](kubefleet/) — multi-cluster Kubernetes management (CNCF sandbox)

More topics may be added over time.
