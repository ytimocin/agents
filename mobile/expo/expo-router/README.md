# Expo Router agent prompts

Reference knowledge for **Expo Router** — Expo's file-based routing library built on React Navigation + React Native Screens. One of four sibling agents under `expo/`: companion to `expo-core` (project setup, `app.config`, CNG, Metro), `expo-sdk` (the ~80 `expo-*` module catalog + Expo Modules API + push notifications), and `eas` (cloud Build/Submit/Update/Workflows/Hosting).

Covers the **`app/` directory convention** as the entire route tree (`index.tsx` → `/`, `name.tsx` → `/name`, `[param].tsx` → dynamic, `[...catchAll].tsx` → rest, `(group)/` → route group not in URL, `_layout.tsx` → navigator, `+not-found.tsx` → 404 fallback, `+html.tsx` → web HTML shell, `+middleware.ts` → web request middleware, `+native-intent.ts` → deep-link interception, `name+api.ts` → server API route), **layouts** (`<Stack>` / `<Tabs>` / `<Drawer>` / `<Slot>` / `expo-router/native-tabs`'s `<NativeTabs>` rendering UITabBarController + BottomNavigationView, `expo-router/ui`'s `<SplitView>`), **navigation** (declarative `<Link href>` with `asChild` + `replace` + `prefetch`; imperative `useRouter().push / replace / navigate / back / dismiss / dismissTo / dismissAll / canDismiss / setParams`; reading state via `useLocalSearchParams` vs `useGlobalSearchParams` — **the re-render footgun where the global hook causes background screens to re-render on every URL change**), **URL parameters** (route params from `[name]` filename — remount on change; search params from `?key=value` — no remount; the reserved-name list `screen` / `params` / `initial` / `state`), **typed routes** (`experiments.typedRoutes: true` → `Href<T>` validated at build time; auto-generated `expo-env.d.ts`; only absolute paths typed; query-param values not typed), **`<Stack>`** configuration (`screenOptions`, per-screen `options` static or dynamic-inside-the-screen, `presentation` modes — `card` / `modal` / `formSheet` / `transparentModal` / `containedModal` / `fullScreenModal`; `getId` to allow multiple instances of the same dynamic route; `Stack.Protected` guards SDK 54+), **`<Tabs>`** with `tabBarIcon` / `tabBarLabel` / `href: null` to hide a route from the bar, **modals** with `sheetAllowedDetents` / `sheetGrabberVisible` / `sheetCornerRadius` / `sheetLargestUndimmedDetentIndex`, **auth patterns** (`Stack.Protected` guards, `<Redirect>` in layout, modal sign-in over current route, `expo-secure-store` for native + `localStorage` or HTTP-only cookies for web, splash-screen handoff to prevent flicker), **web features** (`+api.ts` server routes with standard `Request` / `Response`, `output: "server"`, the `expo-server` utility surface — `StatusError`, `runTask`, `deferTask`; `+middleware.ts`, `+html.tsx`, static + server rendering, `+server-headers.ts`, async routes; CJS-only constraint; no platform suffixes on `+api.ts`), **automatic deep linking** (every screen deep-linkable via `expo.scheme` + iOS `associatedDomains` + Android `intentFilters` with `assetlinks.json` — testing fails in Expo Go because Universal Links bind to the bundle ID), **`unstable_settings.anchor`** for deep-linked modals, **migration from React Navigation** (the navigator → directory mapping, `navigation.navigate('Home')` → `router.push('/home')`, `route.params.id` → `useLocalSearchParams<{id:string}>().id`, theme via `expo-router/react-navigation`'s `ThemeProvider`, `usePathname()` + `useEffect` instead of `onStateChange`). Grounded in live docs at https://docs.expo.dev/router/ with inline `Full docs:` links under every section so the agent can fetch upstream for navigator-specific options and recent API additions.

## Files

| File | Target tool | Format |
|------|-------------|--------|
| `claude.md` | Claude Code | Markdown with YAML frontmatter (`name`, `description`, `model`, `tools`) |
| `codex.md` | OpenAI Codex | Plain markdown (no frontmatter) |
| `copilot.md` | GitHub Copilot | Plain markdown (no frontmatter) |

---

## Install

### Claude Code

```bash
mkdir -p ~/.claude/agents
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/mobile/expo/expo-router/claude.md \
  -o ~/.claude/agents/expo-router-specialist.md
```

Invoke by asking Claude Code to "use the expo-router-specialist agent", or programmatically via the `Agent` tool with `subagent_type: "expo-router-specialist"`.

### OpenAI Codex

```bash
mkdir -p ~/.codex
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/mobile/expo/expo-router/codex.md \
  -o ~/.codex/AGENTS.md
```

### GitHub Copilot CLI

```bash
mkdir -p .github
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/mobile/expo/expo-router/copilot.md \
  -o .github/copilot-instructions.md
```

---

## Provenance and scope

- Built from https://docs.expo.dev/router/ — Introduction, Router 101 (`core-concepts`, `notation`, `navigation`, `navigation-layouts`, `common-navigation-patterns`), Advanced (`stack`, `tabs`, `native-tabs`, `drawer`, `authentication`, `authentication-rewrites`, `nesting-navigators`, `modals`, `web-modals`, `shared-routes`, `protected`, `platform-specific-modules`, `native-intent`, `router-settings`, `apple-handoff`, `custom-tabs`, `stack-toolbar`, `zoom-transition`), Web (`api-routes`, `data-loaders`, `middleware`, `server-headers`, `static-rendering`, `server-rendering`, `async-routes`), Reference (`url-parameters`, `color`, `sitemap`, `redirects`, `link-preview`, `typed-routes`, `screen-tracking`, `src-directory`, `testing`, `troubleshooting`, `reserved-paths`, `error-handling`), Migration (`from-react-navigation`, `from-expo-webpack`, `sdk-55-to-56`), and the SDK reference at https://docs.expo.dev/versions/latest/sdk/router.
- Snapshot date: **2026-06-06**. Audited against **SDK 55+**.
- **Routing only.** Project setup, `app.config`, CNG, Metro, env vars, debugging out of scope (see `expo-core`). SDK modules out of scope (see `expo-sdk`). EAS cloud services out of scope (see `eas`).
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. WebFetch the navigator-specific page when exact options matter — Stack/Tabs/Drawer add fields per SDK release.
