# REST API best-practices agent prompts

Reference knowledge for **designing and reviewing REST/HTTP JSON APIs**, distilled from the three most widely cited public corpora — the [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/) (~180 numbered MUST/SHOULD/MAY rules), the [Google AIPs](https://google.aip.dev/) (~150 API Improvement Proposals), and the [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines) (Azure + Graph, ~250 rules combined) — grounded in the underlying IETF RFCs and IANA registries.

Covers HTTP method semantics (RFC 9110: safety / idempotency / cacheability), status code selection (IANA registry + the most-specific-code discipline), URL design (kebab-case vs camelCase paths, custom-action notation — verb-free resources vs `:colon` suffix), JSON conventions (top-level object, casing fork, RFC 3339 dates, ISO 4217 money, extensible string enums, polymorphism via discriminator), three error-envelope choices (RFC 9457 Problem Details vs Google `google.rpc.Status` vs Microsoft `{error: {code, message, target, details, innererror}}` + `x-ms-error-code` header), pagination (cursor vs offset, opaque tokens, `nextLink` vs `Link` header — Zalando #166's forbid-mixing rule), versioning (URI vs `api-version` query vs media-type — three strategies with explicit tradeoffs), idempotency (`Idempotency-Key` IETF draft vs OASIS Repeatable Requests with `Repeatability-Request-ID` / `-First-Sent`), caching & conditional requests (RFC 9111 + ETag / `If-Match` / `If-None-Match` / 412 / 428), rate limiting (`RateLimit-*` IETF draft headers, 429 vs 503), auth (OAuth 2.0 Bearer per RFC 6750, scope naming, 401 vs 403, RFC 6648's `X-` prefix deprecation), long-running operations (Azure's `Operation-Location` + status monitor with ≥24h retention vs Google's `google.longrunning.Operation` with ~30 day retention), deprecation discipline (`Deprecation` IETF draft header + `Sunset` per RFC 8594 + `Link rel="successor-version"`), HATEOAS and the Richardson Maturity Model (Level 2 as the practical floor), bulk/batch patterns (207 Multi-Status vs Google AIPs 231/233/234/235 vs OData `$batch`), and OpenAPI 3.1 spec hygiene (Zalando `x-api-id`, `x-audience`, `deprecated: true`, reusable `components.schemas`). Grounded in live upstream docs with inline `Full docs: <url>` links under every section so the agent can fetch the canonical wording when it needs more detail.

The three corpora **disagree on opinionated questions** (JSON casing, versioning strategy, error envelope shape, action-vs-resource modeling, collection-name conventions). Where they disagree, this prompt surfaces all three positions and the tradeoff rather than picking a winner — so the agent helps the user choose deliberately rather than imposing a house style.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/rest-api/claude.md \
  -o ~/.claude/agents/rest-api-specialist.md

# Project-level
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/rest-api/claude.md \
  -o .claude/agents/rest-api-specialist.md
```

The frontmatter registers it as a subagent named `rest-api-specialist`. Invoke it by asking Claude Code to "use the rest-api-specialist agent", or delegate programmatically via the `Agent` tool with `subagent_type: "rest-api-specialist"`.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/rest-api/codex.md \
  -o ~/.codex/AGENTS.md

# Per-project — scoped to the current directory
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/rest-api/codex.md \
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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/rest-api/copilot.md \
  -o .github/copilot-instructions.md
```

For an always-on personal setup (active in every directory), check `copilot --help` for the user-level custom-instructions path — last checked it lives under `~/.copilot/`.

**3. Launch** with `copilot` in the workspace.

---

## Updating

These files track the live Zalando / Google AIPs / Microsoft guidelines pages and the underlying RFCs. To refresh, re-run the relevant `curl` above. The corpora update in place (rules can be added, deprecated, or renumbered), so set a periodic refresh cadence (~quarterly) and audit the `Last audited` timestamp in `knowledge.md` against the current rule numbering.

## Provenance and scope

- Built from the three corpora directly:
  - **Zalando** rules #100-#255 distilled from https://opensource.zalando.com/restful-api-guidelines/ (single-page; event-only rules #194-#214 deliberately excluded — this prompt is REST-only).
  - **Google AIPs** distilled from https://google.aip.dev/ — the foundational set (AIP-121 resource-oriented design, AIP-122 resource names, AIP-130/131/132/133/134/135/136 standard + custom methods, AIP-140 field names, AIP-151 LRO, AIP-154 etag, AIP-158 pagination, AIP-160 filtering, AIP-180 backwards compat, AIP-185 versioning, AIP-193 errors).
  - **Microsoft Azure** distilled from https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md (vNext branch — the actively maintained successor to the deprecated top-level `Guidelines.md`).
  - **Microsoft Graph** distilled from https://github.com/microsoft/api-guidelines/blob/vNext/graph/GuidelinesGraph.md.
- Grounded in the IETF RFCs that underlie the corpora: **RFC 9110** (HTTP Semantics, June 2022 — supersedes 7230-7235), **RFC 9111** (HTTP Caching — supersedes 7234), **RFC 9457** (Problem Details, July 2023 — supersedes 7807), **RFC 5789** (PATCH), **RFC 7396** (JSON Merge Patch), **RFC 6902** (JSON Patch), **RFC 8594** (Sunset header), **RFC 8288** (Web Linking), **RFC 3339** (Date/Time), **RFC 6750** (OAuth 2.0 Bearer), **RFC 6648** (deprecation of `X-` prefix). IETF drafts: `draft-ietf-httpapi-idempotency-key-header`, `draft-ietf-httpapi-deprecation-header`, `draft-ietf-httpapi-ratelimit-headers`. OASIS: Repeatable Requests v1.0. IANA registries: status codes, methods, fields, link relations.
- Snapshot date: **2026-06-06**. The Zalando and Google guidelines update in place; Microsoft's Azure guidelines move on the `vNext` branch — re-audit when a rule's exact wording is being quoted to a customer.
- **REST/HTTP/JSON only.** gRPC, GraphQL, AsyncAPI / event-driven design are out of scope. Zalando's event-type rules (#194-#214) are not included because they describe Nakadi / Kafka event schemas, not REST.
- Where the three corpora disagree — **JSON casing**, **versioning strategy**, **error-envelope shape**, **action-vs-resource modeling**, **collection-name conventions**, **PATCH format (JSON Merge Patch vs JSON Patch vs field-mask)** — the prompt surfaces all three positions and the tradeoff. It does **not** pick a winner. The agent's job is to help the user choose deliberately, not impose a house style.
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream pages. When in doubt, link the user to the canonical rule page (Zalando rule URL, AIP-NNN URL, or the GitHub blob of the Microsoft Guidelines.md).
- Claims not directly stated in the docs are explicitly hedged in-text (notably: the practical "most public APIs in the wild use camelCase / kebab-case" observations, the relative popularity of `Idempotency-Key` vs OASIS Repeatable Requests, and the cross-corpus consensus framing — these are editorial judgments grounded in the sources but not verbatim quotes).
