#!/usr/bin/env python3
"""Doc-freshness helpers for the agent prompt library.

Two independent jobs build on this:

  * ``doc-drift.yml``  — hashes the live content of every monitored doc URL and
    diffs it against a committed baseline so an edit to upstream content opens
    an issue.
  * ``doc-msdate.yml`` — reads the ``ms.date`` (last significant update) that
    learn.microsoft.com pages publish and flags any page updated after the
    owning ``knowledge.md``'s ``Last audited:`` date.

Subcommands (all I/O is plain TSV so the workflows can grep/awk around it):

  hash       stdin:  one URL per line
             stdout: ``<url>\\t<sha256-of-normalized-content>`` (or ``ERROR``)

  msdate     stdin:  ``<url>\\t<last_audited:YYYY-MM-DD>\\t<knowledge_path>``
             stdout: drift rows ``<path>\\t<url>\\t<ms_date>\\t<last_audited>``

  compare    argv:   ``<baseline.tsv> <current.tsv>``
             stdout: a markdown report of added/changed/removed URLs
             exit:   0 = no change, 10 = drift found (so the workflow can branch)

Network failures never count as drift — that is link-rot, which ``links.yml``
already owns. A URL that fails to fetch is emitted as ``ERROR`` and skipped by
``compare``.
"""

from __future__ import annotations

import hashlib
import html
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date

UA = "Mozilla/5.0 (compatible; agents-doc-freshness/1.0; +https://github.com/ytimocin/agents)"
TIMEOUT = 30
RETRIES = 3

_SCRIPT_STYLE = re.compile(r"<(script|style|svg|noscript)\b.*?</\1>", re.I | re.S)
_COMMENT = re.compile(r"<!--.*?-->", re.S)
_MAIN = re.compile(r"<main\b[^>]*>(.*?)</main>", re.I | re.S)
_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")
# learn.microsoft.com publishes ms.date as a <meta> tag or in the page's JSON.
_MSDATE = re.compile(
    r"""(?:name=["']ms\.date["']\s+content=["']([^"']+)["'])"""
    r"""|(?:["']ms\.date["']\s*:\s*["']([^"']+)["'])""",
    re.I,
)


def fetch(url: str) -> str:
    last = None
    for attempt in range(RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                charset = resp.headers.get_content_charset() or "utf-8"
                return resp.read().decode(charset, errors="replace")
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError) as exc:
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"fetch failed: {last}")


def normalize(page: str) -> str:
    """Reduce a page to the stable text of its main article.

    Strips scripts/styles/comments, prefers the <main> element (article body on
    learn.microsoft.com and most doc sites), drops remaining tags, unescapes
    entities, and collapses whitespace. This filters most cosmetic chrome so the
    hash only moves when the prose moves.
    """
    page = _SCRIPT_STYLE.sub(" ", page)
    page = _COMMENT.sub(" ", page)
    m = _MAIN.search(page)
    body = m.group(1) if m else page
    text = _TAG.sub(" ", body)
    text = html.unescape(text)
    return _WS.sub(" ", text).strip()


def cmd_hash() -> int:
    for line in sys.stdin:
        url = line.strip()
        if not url:
            continue
        try:
            digest = hashlib.sha256(normalize(fetch(url)).encode("utf-8")).hexdigest()
        except Exception as exc:  # noqa: BLE001 — any failure is "couldn't hash"
            print(f"{url}\tERROR", flush=True)
            print(f"  ! {url}: {exc}", file=sys.stderr)
            continue
        print(f"{url}\t{digest}", flush=True)
        time.sleep(0.3)  # be polite to upstream
    return 0


def _parse_msdate(raw: str) -> date | None:
    raw = raw.strip()
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y"):
        try:
            return _strptime(raw, fmt)
        except ValueError:
            continue
    return None


def _strptime(raw: str, fmt: str) -> date:
    import datetime

    return datetime.datetime.strptime(raw, fmt).date()


def cmd_msdate() -> int:
    drift = 0
    for line in sys.stdin:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        url, audited_raw, path = parts[0], parts[1], parts[2]
        audited = _parse_msdate(audited_raw)
        try:
            page = fetch(url)
        except Exception as exc:  # noqa: BLE001
            print(f"  ! {url}: {exc}", file=sys.stderr)
            continue
        m = _MSDATE.search(page)
        if not m:
            print(f"  ? {url}: no ms.date found", file=sys.stderr)
            continue
        ms = _parse_msdate(m.group(1) or m.group(2) or "")
        if ms is None or audited is None:
            continue
        if ms > audited:
            print(f"{path}\t{url}\t{ms.isoformat()}\t{audited.isoformat()}", flush=True)
            drift += 1
        time.sleep(0.3)
    print(f"ms.date drift rows: {drift}", file=sys.stderr)
    return 0


def _load(path: str) -> dict[str, str]:
    out: dict[str, str] = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            url, _, digest = line.rstrip("\n").partition("\t")
            if url:
                out[url] = digest
    return out


def cmd_compare(baseline_path: str, current_path: str) -> int:
    baseline = _load(baseline_path)
    current = _load(current_path)

    added, changed, removed = [], [], []
    for url, digest in current.items():
        if digest == "ERROR":
            continue  # fetch failure → link-rot's job, not drift
        if url not in baseline:
            added.append(url)
        elif baseline[url] != digest:
            changed.append(url)
    for url in baseline:
        if url not in current:
            removed.append(url)

    if not (added or changed or removed):
        print("No upstream content changes since the last baseline.")
        return 0

    def block(title: str, urls: list[str]) -> str:
        if not urls:
            return ""
        lines = "\n".join(f"- {u}" for u in sorted(urls))
        return f"\n### {title} ({len(urls)})\n{lines}\n"

    print("The normalized content of these monitored doc pages changed since the "
          "committed baseline. Re-audit the affected `knowledge.md` sections, then "
          "refresh the baseline (run the **doc-drift** workflow with "
          "`refresh_baseline=true`).\n")
    print(block("Changed", changed), end="")
    print(block("New (now referenced)", added), end="")
    print(block("Removed (no longer referenced)", removed), end="")
    return 10


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cmd = sys.argv[1]
    if cmd == "hash":
        return cmd_hash()
    if cmd == "msdate":
        return cmd_msdate()
    if cmd == "compare":
        if len(sys.argv) != 4:
            print("usage: doc_check.py compare <baseline.tsv> <current.tsv>", file=sys.stderr)
            return 2
        return cmd_compare(sys.argv[2], sys.argv[3])
    print(f"unknown subcommand: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
