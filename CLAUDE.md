# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Prompt library — no application code, no tests. Each top-level folder is an agent topic (currently `kubefleet/`). Every topic follows a one-source/three-peers layout so the same knowledge is served to whichever AI tool a teammate uses.

## Topic folder layout

```
<topic>/
  knowledge.md               # shared body — the ONLY file edited by hand
  claude.frontmatter.yaml    # YAML header used to wrap claude.md as a Claude Code subagent
  claude.md                  # generated: claude.frontmatter.yaml + knowledge.md
  codex.md                   # generated: knowledge.md verbatim (for Codex AGENTS.md)
  copilot.md                 # generated: knowledge.md verbatim (for .github/copilot-instructions.md)
  README.md                  # install instructions
  images/                    # screenshots referenced by README
```

**The three tool-facing files are generated peers, not sources.** Never edit them directly — the next sync will clobber your changes. Edit `knowledge.md`, then run:

```bash
bash scripts/sync.sh
```

CI (`.github/workflows/verify.yml`) runs the same script on every push and fails if any generated file drifted. That's the safeguard that keeps Claude Code / Codex / Copilot users from ending up with different knowledge.

## Knowledge-file style

The files are LLM-consumed, so structure for retrieval over narrative:

- Short paragraphs, dense tables, and YAML skeletons over prose.
- **Every `##` section ends with a `Full docs: <live-url>` link**, and the preamble instructs the LLM to WebFetch the linked upstream page for edge cases. That pair is what lets the agent answer authoritatively without bloating the prompt. Don't drop either half when editing.
- Hedge unverified claims ("implementation detail not specified in the docs") rather than asserting them. Existing content has been audited against upstream docs; preserve that discipline.

## Workflow agents (exemption to the topic pattern)

`.claude/agents/` holds **workflow** agents — they do things (review prompts in code, review prompt/response logs in a DB), they don't describe a technology. They intentionally sit outside the 3-peer sync pattern: there's no `codex.md`/`copilot.md` peer because Codex and Copilot consume agent definitions differently, and the substantive prompt-engineering knowledge they reference lives in the `prompt-engineering/` topic (which *is* synced). Don't try to "fix" the asymmetry by giving workflow agents peer files — there's nothing to keep in sync.

Current workflow agents:
- `.claude/agents/prompt-reviewer-code.md` — reconstructs prompts buried in code, applies the prompt-engineering checklist
- `.claude/agents/prompt-reviewer-logs.md` — reads prompt/response logs from any DB, applies the checklist + output-side signals

## Verification

No application tests exist. The one thing worth checking before a commit: `bash scripts/sync.sh && git diff` — if `claude.md`, `codex.md`, or `copilot.md` shows changes, you're editing the wrong file (should be `knowledge.md`), or you forgot to run sync.
