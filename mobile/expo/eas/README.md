# EAS agent prompts

Reference knowledge for **EAS (Expo Application Services)** — Expo's hosted cloud services that ship React Native and Expo apps end-to-end: cloud-compiled native binaries (iOS on macOS runners + Android on Linux GCP runners), App Store / Play Store submission, over-the-air JS-bundle updates via the `expo-updates` client, YAML-defined CI/CD workflows, and Cloudflare-Workers-backed web + API-route hosting. One of four sibling agents under `expo/`: companion to `expo-core` (project setup, `app.config`, CNG, Metro), `expo-router` (file-based routing), and `expo-sdk` (the ~80 `expo-*` module catalog + Expo Modules API + push notifications).

Covers the **`eas.json` schema** in full — the `cli` block (`version` SemVer range, `appVersionSource: "remote" | "local"` and why `remote` + `autoIncrement: true` is the safe default, `requireCommit`, `promptToConfigurePushNotifications`); named `build` profiles with the conventional three (`development` / `preview` / `production`) and the full field surface (`extends` up to 5 levels deep no cycles, `env` for build-time + runtime inlining, `distribution: "internal" | "store"`, `channel` to bind the build to an EAS Update channel, `developmentClient: true` to bundle `expo-dev-client`, `image` for pinned worker images, `node` for pinned Node version, `resourceClass: "default" | "medium" | "large"` with `large` paid-plan-only for monorepos/heavy native deps, `autoIncrement` for server-side `versionCode`/`buildNumber` bumps, `simulator: true` for iOS Simulator `.app` instead of device `.ipa`, `buildType: "apk" | "app-bundle"` for Android, `android.gradleCommand`, `ios.scheme`, `cache` knobs, `prebuildCommand`); `submit` profiles per platform (iOS `appleId`/`ascAppId`/`appleTeamId` or the recommended `ascApiKeyPath`+`ascApiKeyIssuerId`+`ascApiKeyId` App Store Connect API key, `changesNotSentForReview`; Android `serviceAccountKeyPath`/`track`/`releaseStatus`); `update` profiles binding `channel` → branch.

Covers **EAS Build** in depth (the build sequence — repo sync → install deps → `expo prebuild` if `ios/`/`android/` absent → credentials resolution → native build → sign + package → upload), credentials handling (iOS distribution cert account-level one-per-team + per-app provisioning profile expiring 12mo but shipped apps keep working + APNs `.p8` key max 2 per account never-expires; Android keystore with **Play App Signing** recoverable upload-certificate vs legacy app-signing-key irrecoverable; FCM v1 service-account JSON for push), `eas build:resign` to swap provisioning profile without rebuilding, **internal distribution** ad-hoc install links, GitHub-triggered builds, build cache controls, custom-builds YAML overrides.

Covers **EAS Submit** (the platform-specific gotchas — iOS lands in TestFlight in 10-15 minutes but **production release requires manual App Review submission in App Store Connect**; Android **first-ever Play Store submission for an app must be a manual upload** via Play Console UI because the API can only update existing entries, track promotion uses Play Console rollout policies, `--auto-submit` chains build → submit), the App Store Connect API key flow vs Apple ID password, the Google Service Account JSON with "Release Manager" grant.

Covers **EAS Update** with the **mental model the user is most likely to get wrong**: every running build identifies itself by `(platform, runtimeVersion, channel)`; updates live on **branches**; **channels point at branches** (default same-name auto-linking; rollback works by re-pointing the channel at an older branch); the four `runtimeVersion` policies (literal string / `"sdkVersion"` / `"appVersion"` / `"fingerprint"` SDK 53+) with their tradeoffs and the **don't-change-mid-lifecycle** rule; the publish + delivery flow (`eas update --auto`, `eas update --branch <name> --message`, two-phase manifest+assets download with next-launch activation if download exceeds timeout); rollback via `eas update:republish`; gradual rollout via `eas update:roll-out-new-update`; **app-store-rules safety** — JS, styles, images, fonts, non-native assets only; **never native code changes, native dep changes, permission changes, or Expo SDK version changes** (those require a new binary); `eas-update-code-signing` for MITM protection.

Covers **EAS Workflows** YAML in `.eas/workflows/` (the `name` / `on` (push / pull_request / schedule / manual / `appstore-connect`) / `jobs` shape, pre-packaged job types `build` / `submit` / `update` / `maestro` for E2E / `deploy` / custom shell, the explicit non-features — **no matrix builds, no shared workflow templates** — and when to prefer GitHub Actions calling out to `eas build` instead).

Covers **EAS Hosting** (Cloudflare Workers V8 runtime — Web-standard `Request`/`Response`, no `fs` / no `child_process` / no `Buffer`; `eas deploy` with immutable deployments + aliases for instant rollback; custom domains paid-plan-only with automatic TLS; `+api.ts` server routes running as Workers; `+server-headers.ts` for per-route caching; 3600s default static asset cache; observability dashboard with per-request logs and crashes).

Covers **app signing** with the full credentials matrix per platform (iOS three credentials: distribution cert + provisioning profile + push key, with their account-vs-per-app scope and expiry semantics; Android keystore management with the Play App Signing recommendation and the **"don't lose the keystore on legacy app-signing-key apps"** warning; FCM v1 vs legacy FCM server key migration), the `eas credentials` interactive management command, and EAS-managed vs local credential storage tradeoffs.

Covers **EAS environment variables** (`eas env:create` / `:list` / `:pull --file` / `:exec` across **three scopes** account-level + project-level + per-profile; the same `EXPO_PUBLIC_*` inlining rule as local — visible plaintext in the bundle, never for secrets; `eas env --visibility secret` for sensitive build-time values; the older `eas secret` API still works), **webhooks** for build/update events with HMAC-SHA256 verification, and the **EAS Insights / EAS Observe / EAS Metadata** preview-tier services with their preview-status flag.

Covers the **EAS CLI** command surface (`eas init`, `eas build:configure`, `eas login`, `eas build` with `--platform` / `--profile` / `--auto-submit` / `--no-wait` / `--id`, `eas build:resign`, `eas build:list / :view / :cancel`, `eas submit`, `eas update` with `--branch` / `--auto` / `--message`, `eas update:republish`, `eas update:roll-out-new-update`, `eas channel:list / :create / :edit`, `eas credentials`, `eas workflow:run / :list`, `eas deploy / deploy:list / deploy:promote`, `eas env:*`, `eas project:init`).

Grounded in live docs at https://docs.expo.dev/eas with inline `Full docs:` links per section so the agent can fetch upstream for exact `eas.json` field tables, CLI flag changes, and current pricing tiers.

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
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/mobile/expo/eas/claude.md \
  -o ~/.claude/agents/eas-specialist.md
```

Invoke by asking Claude Code to "use the eas-specialist agent", or programmatically via the `Agent` tool with `subagent_type: "eas-specialist"`.

### OpenAI Codex

```bash
mkdir -p ~/.codex
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/mobile/expo/eas/codex.md \
  -o ~/.codex/AGENTS.md
```

### GitHub Copilot CLI

```bash
mkdir -p .github
curl -fsSL https://raw.githubusercontent.com/ytimocin/agents/main/mobile/expo/eas/copilot.md \
  -o .github/copilot-instructions.md
```

---

## Provenance and scope

- Built from https://docs.expo.dev/eas (the EAS landing index), https://docs.expo.dev/build/introduction + `/build/eas-json` + `/build-reference/*`, https://docs.expo.dev/submit/introduction + `/submit/{ios,android,eas-json}`, https://docs.expo.dev/eas-update/introduction + `/eas-update/how-it-works` + `/eas-update/runtime-versions` + `/eas-update/{rollouts,rollbacks,code-signing,migrate-from-classic-updates}`, https://docs.expo.dev/eas/workflows/introduction + `/eas/workflows/{syntax,pre-packaged-jobs,examples/introduction}`, https://docs.expo.dev/eas/hosting/introduction + `/eas/hosting/{deployments-and-aliases,custom-domain,api-routes,workflows,reference/*}`, https://docs.expo.dev/app-signing/{app-credentials,managed-credentials,local-credentials,syncing-credentials,security}, https://docs.expo.dev/eas/environment-variables + `/eas/environment-variables/{manage,usage,without-eas,faq}`, https://docs.expo.dev/eas/{cli,webhooks,metadata}, https://docs.expo.dev/eas-insights/introduction, https://docs.expo.dev/eas/observe/*.
- Snapshot date: **2026-06-06**. Audited against the **vNext** EAS docs. Pricing tiers, preview-feature status (EAS Insights, EAS Metadata, EAS Observe), and EAS CLI flag surface drift in place — re-check the canonical pages before quoting numbers or making customer commitments.
- **EAS cloud services only.** Project setup, `app.config`, CNG, Metro, env-var inlining mechanics out of scope (see `expo-core`). Routing out of scope (see `expo-router`). The SDK module catalog and `expo-updates` client API out of scope (see `expo-sdk`).
- Intended as a fast-retrieval reference for an LLM, not a substitute for the upstream docs. Per-page WebFetch when exact `eas.json` field tables, CLI flag combinations, or pricing matter.
