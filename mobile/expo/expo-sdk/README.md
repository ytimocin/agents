# Expo SDK agent prompts

Reference knowledge for the **Expo SDK** — the ~80 cross-platform `expo-*` packages, the **Expo Modules API** for authoring your own native Swift/Kotlin modules, **push notifications** (Expo Push Service vs raw FCM/APNs), and the **Expo UI** component layer (SwiftUI / Jetpack Compose / Universal). One of four sibling agents under `expo/`: companion to `expo-core` (project setup, `app.config`, CNG, Metro), `expo-router` (file-based routing), and `eas` (cloud Build/Submit/Update/Workflows/Hosting).

Covers the **module catalog** organized by domain — **media** (`expo-camera`, `expo-audio` and `expo-video` replacing `expo-av`, `expo-image`, `expo-image-picker`, `expo-image-manipulator`, `expo-media-library`, `expo-sharing`, `expo-print`, `expo-blur-view`, `expo-linear-gradient`, `expo-mesh-gradient`, `expo-glass-effect`, `expo-live-photo`, `expo-symbols`), **filesystem & storage** (`expo-file-system` modern class API replacing the string-URI legacy, `expo-secure-store` Keychain/Keystore with the ~2KB Android value limit and biometric-rekey invalidation footgun, `expo-sqlite`, `expo-asset`, `expo-clipboard`, `expo-document-picker`, `expo-blob`), **auth, crypto, identity** (`expo-auth-session` for OAuth/OIDC + PKCE, `expo-apple-authentication`, `expo-crypto`, `expo-local-authentication`, `expo-app-integrity`), **notifications & background** (`expo-notifications` with the 3-second `handleNotification` budget and Android notification-channel mandate since API 26, `expo-background-task` replacing `expo-background-fetch` for SDK 54+, `expo-task-manager`, `expo-screen-capture`, `expo-keep-awake`, `expo-screen-orientation`, `expo-status-bar`, `expo-navigation-bar`, `expo-system-ui`, `expo-splash-screen`), **location, sensors, device** (`expo-location` with foreground vs background permission split, `expo-sensors`, `expo-device`, `expo-application`, `expo-cellular`, `expo-network`, `expo-battery`, `expo-brightness`, `expo-haptics`, `expo-localization`, `expo-constants` as the runtime read-path for `app.config.extra`, `expo-intent-launcher`), **communications** (`expo-sms`, `expo-mail-composer`, `expo-contacts`, `expo-calendar`, `expo-speech`, `expo-storereview`), and **the Expo UI component layer** (SDK 54+ Jetpack Compose components, SwiftUI components, Universal components, plus drop-in replacements for community libraries like `BottomSheet`, `DateTimePicker`, `Menu`, `PagerView`, `Picker`, `SegmentedControl`, `Slider`).

Covers the **cross-cutting patterns** that show up in every module — the `usePermissions()` hook (returns `PermissionResponse` with `status` / `granted` / `expires` / `canAskAgain`; route to `Linking.openSettings()` when `canAskAgain: false`), the `…Async` method naming convention, `EventSubscription.remove()` cleanup discipline, JSI shared objects (`AudioPlayer`, `VideoPlayer`, `ImageRef`, `Recording` live in native memory — never `JSON.stringify`, never in serializable React state), foreground vs background work (background needs platform capabilities + config-plugin flags + `expo-task-manager`), web fallbacks (the platform compatibility matrix at the top of each module page).

Covers **push notifications** as a deep-dive section — the two token kinds (`ExponentPushToken[…]` via `getExpoPushTokenAsync({ projectId })` for the Expo Push Service at `https://exp.host/--/api/v2/push/send` vs raw FCM/APNs token via `getDevicePushTokenAsync()`), the credentials matrix (APNs auth key `.p8` + Key ID + Team ID for iOS; FCM v1 service-account JSON for Android — **legacy FCM server key is being deprecated, migrate**), `setNotificationHandler` with its 3-second timeout, Android notification channels mandatory since API 26, what works in Expo Go (local notifications only — remote push requires a dev build on iOS since SDK ~49, on Android since SDK 53).

Covers **authoring native modules with the Expo Modules API** — the `Module()` definition DSL (`Name`, `Function`, `AsyncFunction`, `Property`, `Constants`, `Events`, `View(SwiftClass.self) { Prop { } ; Events }`, `OnCreate`, `OnDestroy`), the Swift + Kotlin parallel structure, JSI-backed performance (hundreds of thousands of native calls per second, negligible binary-size impact), when to use it (Expo Modules API for ergonomic cross-platform native; Turbo Modules for heavy C++), the autolinking + `AppDelegate subscribers` + `Android lifecycle listeners` infrastructure that lets modules hook iOS/Android lifecycle without editing files wiped by `prebuild --clean`.

Covers the **per-module config plugin parameters** (`expo-camera` cameraPermission/microphonePermission/recordAudioAndroid/barcodeScannerEnabled, `expo-image-picker` cameraPermission/photosPermission/microphonePermission, `expo-location` locationAlwaysAndWhenInUsePermission/locationWhenInUsePermission/isIosBackgroundLocationEnabled/isAndroidBackgroundLocationEnabled, `expo-notifications` icon/color, `expo-build-properties` for `compileSdkVersion`/`iosDeploymentTarget`/`kotlinVersion`/`enableBundleCompression`) and the **cross-module permission table** mapping each native permission to the `expo-*` modules that need it, the iOS Info.plist key, and the Android manifest entry.

Grounded in live docs at https://docs.expo.dev/versions/latest/ with inline `Full docs:` links per section so the agent can fetch the specific module page (URL pattern: `https://docs.expo.dev/versions/latest/sdk/<module>`) when exact method signatures and option enums are needed. Catalog-style by design — *which module to use and how to set it up* — not a per-module API mirror.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/mobile/expo/expo-sdk/claude.md \
  -o ~/.claude/agents/expo-sdk-specialist.md
```

Invoke by asking Claude Code to "use the expo-sdk-specialist agent", or programmatically via the `Agent` tool with `subagent_type: "expo-sdk-specialist"`.

### OpenAI Codex

```bash
mkdir -p ~/.codex
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/mobile/expo/expo-sdk/codex.md \
  -o ~/.codex/AGENTS.md
```

### GitHub Copilot CLI

```bash
mkdir -p .github
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/mobile/expo/expo-sdk/copilot.md \
  -o .github/copilot-instructions.md
```

---

## Provenance and scope

- Built from https://docs.expo.dev/versions/latest/ (the SDK reference index of ~80 modules), the LLM-friendly index at https://docs.expo.dev/llms.txt, the push notifications guide at https://docs.expo.dev/push-notifications/overview, the Expo Modules API at https://docs.expo.dev/modules/overview, and per-module pages including `https://docs.expo.dev/versions/latest/sdk/{expo,camera,notifications,filesystem,securestore,audio,…}`.
- Snapshot date: **2026-06-06**. Audited against **SDK 55+** (New Architecture always-on; legacy frozen).
- **Catalog-style by design.** The agent knows *which module to use, how to install it, what permissions/config plugin/credentials it needs, and the cross-cutting patterns shared across modules*. For exact method signatures and option enums, the agent WebFetches the specific module page (URL pattern: `https://docs.expo.dev/versions/latest/sdk/<name>`).
- **SDK modules, Modules API authoring, push notifications, Expo UI components only.** Project shape, `app.config`, CNG, Metro, env vars out of scope (see `expo-core`). Routing out of scope (see `expo-router`). EAS cloud services out of scope (see `eas`).
- Legacy modules (`expo-av`, `expo-file-system/legacy`, `expo-calendar-legacy`, `expo-contacts-legacy`, `expo-media-library-legacy`, `expo-background-fetch`) are surfaced with their deprecation status; new-project recommendations point at the modern replacements (`expo-audio`+`expo-video`, modern `expo-file-system`, modern variants, `expo-background-task`).
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. Per-module pages are the source of truth for prop tables, method signatures, and recent additions.
