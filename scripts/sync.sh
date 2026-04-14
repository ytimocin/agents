#!/usr/bin/env bash
# Regenerate every topic's claude.md / codex.md / copilot.md from its
# shared knowledge.md body. claude.md additionally gets the YAML
# frontmatter from claude.frontmatter.yaml prepended so Claude Code
# can register it as a subagent.
#
# knowledge.md is the single source of truth — edit that. The three
# tool-facing files are generated peers; CI runs this script and
# fails the build if any of them drifts.

set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

shopt -s nullglob

any_topic=0
for topic_dir in */; do
    knowledge="${topic_dir}knowledge.md"
    [[ -f "$knowledge" ]] || continue
    any_topic=1

    cp "$knowledge" "${topic_dir}codex.md"
    cp "$knowledge" "${topic_dir}copilot.md"

    frontmatter="${topic_dir}claude.frontmatter.yaml"
    if [[ -f "$frontmatter" ]]; then
        cat "$frontmatter" "$knowledge" > "${topic_dir}claude.md"
    else
        cp "$knowledge" "${topic_dir}claude.md"
    fi

    echo "synced ${topic_dir}{claude,codex,copilot}.md from ${knowledge}"
done

if (( any_topic == 0 )); then
    echo "no topic folders with knowledge.md found; nothing to do" >&2
fi
