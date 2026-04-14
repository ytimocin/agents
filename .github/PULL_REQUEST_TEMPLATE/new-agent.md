## New agent topic

**Topic name (folder):** <!-- e.g. argocd, kubectl, cert-manager -->

### Why this agent is worth adding

<!-- What problem does it solve? Which teammates benefit? -->

### Upstream sources used

At least one valid URL is required. The more sources linked, the easier the prompt is to audit.

- Project repository: <!-- e.g. https://github.com/argoproj/argo-cd -->
- Official docs: <!-- e.g. https://argo-cd.readthedocs.io/en/stable/ -->
- API reference (if separate): 
- Other canonical references (specs, RFCs, CRDs): 

### Scope covered

<!-- Which topics does the new agent know about? e.g. "Application CRs,
     ApplicationSets, Projects, Sync waves, Health checks." -->

### Checklist

- [ ] `<topic>/knowledge.md` exists and follows the [style rules in CONTRIBUTING.md](../CONTRIBUTING.md#style-rules-for-the-knowledge-itself) (short paragraphs, tables, YAML skeletons, `Full docs: <url>` under every `##` section).
- [ ] `<topic>/claude.frontmatter.yaml` exists with `name: <topic>-specialist`, a one-line `description`, `model`, `tools`, `memory`.
- [ ] `<topic>/README.md` exists with install commands for Claude Code, Codex, and Copilot (model on `kubefleet/README.md`).
- [ ] I ran `bash scripts/sync.sh` — `claude.md`, `codex.md`, and `copilot.md` are regenerated.
- [ ] `Last audited: YYYY-MM-DD` is set in `knowledge.md`.
- [ ] The new topic is listed in the root `README.md` under **Topics**.
- [ ] CI (`verify`, `links`) is green.
