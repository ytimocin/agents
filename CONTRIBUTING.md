# Contributing

Thanks for taking the time. Most contributions fall into one of three buckets:

1. **Reporting a wrong or missing fact** in an existing topic — file an issue.
2. **Editing an existing topic** — PR against `<topic>/knowledge.md`; run the sync script before committing.
3. **Adding a new topic** — scaffold the files following the kubefleet layout.

## The layout: domain folders + one-source-three-peers per topic

Topics live either at the top level (singletons) or grouped under a **domain folder** when ≥2 related topics exist — `cloud-native/`, `databases/`, `mobile/`, `observability/`, `seo/`, `sports-data/`. The grouping is organizational; the `scripts/sync.sh` script walks the tree recursively and finds every `knowledge.md` regardless of nesting depth.

```
agents/
  <domain>/             # ← only present when ≥2 topics cluster
    <topic>/
      knowledge.md
      claude.frontmatter.yaml
      claude.md         # generated
      codex.md          # generated
      copilot.md        # generated
      README.md
  <topic>/              # ← singletons stay flat
    knowledge.md
    ...
```

Every topic folder (at any nesting depth) contains:

- `<topic>/knowledge.md` — the shared body. **The only file edited by hand.**
- `<topic>/claude.frontmatter.yaml` — YAML frontmatter used for the Claude Code subagent wrapper.
- `<topic>/claude.md` — generated: frontmatter + knowledge.md
- `<topic>/codex.md` — generated: knowledge.md verbatim (for Codex `AGENTS.md`)
- `<topic>/copilot.md` — generated: knowledge.md verbatim (for GitHub Copilot)
- `<topic>/README.md` — install instructions (the `curl` URLs reflect the full path including any domain folder)

The three tool-facing files are **peers**, not copies of each other. They all derive from `knowledge.md`. CI regenerates them on every push and fails the build if any has drifted, so there's no way for a teammate using one tool to get different knowledge than a teammate using another.

## Editing an existing topic

1. Edit `<topic>/knowledge.md`.
2. Run `bash scripts/sync.sh`.
3. `git diff` — confirm only the files you meant to change moved.
4. Commit and open a PR.

Don't edit `claude.md`, `codex.md`, or `copilot.md` directly — the next sync will clobber your changes.

### Style rules for the knowledge itself

These files are LLM-consumed, not human prose. Structure for retrieval:

- Dense tables, YAML skeletons, and short bullet lists over narrative.
- **Every `##` section ends with a `Full docs: <live-url>` link**, and the preamble tells the LLM to WebFetch the linked upstream page for edge cases. Don't drop these footers.
- Hedge claims that aren't in the upstream docs ("implementation detail not specified in the docs") rather than asserting them. When in doubt, open the upstream page and copy the exact wording.

## Auditing a claim against upstream docs

Before adding or changing a fact:

1. Open the relevant upstream page (e.g. https://kubefleet.dev/docs/concepts/crp/).
2. Confirm the claim is stated there — not inferred, not from a GitHub issue or blog.
3. Link that page in the `Full docs:` footer of the section.
4. If a claim is plausibly true but not in the docs, mark it with wording like *"not specified in the docs"* so future readers know it's an implementation detail, not an API guarantee.

## Adding a new topic

Pick a short, lowercase folder name (`kubefleet`, `argocd`, `kubectl`, `expo-router`, etc. — hyphens are fine).

**Decide where it goes:**

- **Does an existing domain folder fit?** Drop it in (`cloud-native/<topic>/`, `databases/<topic>/`, `mobile/<topic>/`, etc.).
- **Does an existing top-level singleton become a sibling?** Create the domain folder now and move the singleton in alongside the newcomer.
- **Neither?** Drop it at the top level as a singleton. Don't preemptively create a one-child domain folder — wrap when a sibling shows up.

```bash
topic=<name>
# Top-level singleton:
mkdir -p "$topic/images"
# Or inside a domain:
mkdir -p "<domain>/$topic/images"
```

Create `<topic>/knowledge.md`. Use `cloud-native/kubefleet/knowledge.md` as a structural template — preamble with upstream links and a "fetch the linked page for edge cases" directive, an `## API Groups & Versions` table if applicable, `## Core Concepts`, `## Troubleshooting`, etc. Keep it high-signal; link out rather than reproducing the docs verbatim.

Create `<topic>/claude.frontmatter.yaml` with the subagent metadata:

```yaml
---
name: <topic>-specialist
description: One sentence describing the agent's scope so Claude Code knows when to invoke it.
model: sonnet
tools: Read, Grep, Glob, Bash, Edit, Write, WebFetch
memory: user
---

```

Note the trailing blank line — it becomes the spacer between frontmatter and body in the generated `claude.md`.

Generate the three tool-facing files:

```bash
bash scripts/sync.sh
```

Create `<topic>/README.md` modeled on `cloud-native/kubefleet/README.md` — three install sections (Claude Code, Codex, Copilot) with `curl` commands, plus a Provenance note pointing at upstream docs. The `curl` URLs must reflect the **full path** including any domain folder (`/agents/main/<domain>/<topic>/claude.md`, not `/agents/main/<topic>/claude.md`).

Add the new topic to the Topics list in the root `README.md`.

## Reporting wrong or missing knowledge

Open an issue using the **Incorrect knowledge** template. Include the tool you were using, the topic and section, the upstream URL that contradicts the claim, and the exact prompt that produced the bad output. The more specific the reproduction, the faster it gets fixed.
