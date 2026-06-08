# Expo Core agent prompts

Reference knowledge for the **foundation of an Expo project** — the mental model (Expo SDK + Expo Modules + Continuous Native Generation + EAS), how to configure it, run it, debug it, and organize it. Companion to three sibling agents: `expo-router` for file-based routing, `expo-sdk` for the ~80 `expo-*` module catalog + Expo Modules API authoring + push notifications, and `eas` for the cloud Build/Submit/Update/Workflows/Hosting services.

Covers the **three ways to run an Expo app** (Expo Go vs development build vs production — the failure-mode classifier), `app.config.js` / `app.config.ts` / `app.json` (resolution order, dynamic config middleware, `Constants.expoConfig.extra` runtime access, fields filtered from the public config), **Continuous Native Generation** (`npx expo prebuild --clean`, the contract between `app.config` + plugins + autolinking + template, when to opt out and commit `ios/` / `android/`), **config plugins** (`with<Name>(config, props)`, `withAndroidManifest` / `withInfoPlist` / `withAppDelegate` mods, mod-run-only-during-prebuild semantics), **Metro customization** (`expo/metro-config` not `@expo/metro-config` — the version-drift footgun; `resolver.assetExts`, `resolver.resolveRequest`, web bundling, `package.json` exports, DOM components, tree-shaking), **Babel** (`babel-preset-expo` + Reanimated plugin last), the **`EXPO_PUBLIC_*` env-var convention** (inlined at bundle time via dot-notation only; never bracket notation; never secrets — they ship plaintext), **monorepo** support (SDK 52+ auto-detects; pnpm `nodeLinker: hoisted`; `experiments.autolinkingModuleResolution: true` to align Metro with native autolinking; duplicate-React/RN footguns), **the New Architecture** (Fabric / TurboModules / JSI / Codegen — always-on from SDK 55+; legacy frozen June 2025; `newArchEnabled` field is dead in 55+), **Hermes** (the default JS engine, AOT bytecode, `j` to launch Chrome DevTools Protocol debugger, per-platform `jsEngine` override), **deep linking** (`expo.scheme` for custom schemes, `associatedDomains` for iOS Universal Links + `intentFilters` for Android App Links, `Linking.openURL` / `Linking.createURL` / `Linking.addEventListener`), **debugging** (Hermes debugger, `adb logcat`, `Console.app`, `--no-dev --minify` production-mode local repro, source maps, Sentry/Bugsnag integration paths), **bare workflow** vs CNG vs **brownfield** (isolated vs integrated React Native embedding), and the **Expo CLI** command surface (`expo start --tunnel`, `expo prebuild --clean`, `expo run:ios`, `expo run:android`, `expo install --fix`, `expo lint`, `expo-doctor`, `expo customize`, `expo export`). Grounded in the live docs at https://docs.expo.dev/ with inline `Full docs:` links under every section so the agent can fetch upstream for edge cases. Explicitly stays in its lane — defers to `expo-router`, `expo-sdk`, and `eas` rather than half-answering across them.

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

```bash
# User-level (recommended — reusable across all projects)
mkdir -p ~/.claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/mobile/expo/expo-core/claude.md \
  -o ~/.claude/agents/expo-core-specialist.md

# Project-level
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/mobile/expo/expo-core/claude.md \
  -o .claude/agents/expo-core-specialist.md
```

Invoke by asking Claude Code to "use the expo-core-specialist agent", or programmatically via the `Agent` tool with `subagent_type: "expo-core-specialist"`.

### OpenAI Codex

```bash
mkdir -p ~/.codex
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/mobile/expo/expo-core/codex.md \
  -o ~/.codex/AGENTS.md
# or per-project at ./AGENTS.md
```

### GitHub Copilot CLI

```bash
mkdir -p .github
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/mobile/expo/expo-core/copilot.md \
  -o .github/copilot-instructions.md
```

---

## Provenance and scope

- Built from the live docs at https://docs.expo.dev/, the LLM-friendly index at https://docs.expo.dev/llms.txt, and the configuration reference at https://docs.expo.dev/versions/latest/config/app.
- Snapshot date: **2026-06-06**. Audited against **SDK 55+** (the cutover to always-on New Architecture; `newArchEnabled: false` is ignored).
- **Project setup, config, prebuild, Metro/Babel, env vars, debugging, monorepos, bare/brownfield only.** Routing is out of scope (see `expo-router`), the SDK module catalog is out of scope (see `expo-sdk`), and the EAS cloud services are out of scope (see `eas`).
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. When in doubt, link the user to the canonical page (the `Full docs:` footer of each section).
