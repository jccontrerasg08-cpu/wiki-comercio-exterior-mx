"""Verify that a Material offline build has no remote runtime assets."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re


_REMOTE = re.compile(r"^(?:https?:)?//", re.IGNORECASE)
_CSS_REMOTE = re.compile(r"url\(\s*['\"]?(?:https?:)?//", re.IGNORECASE)
_RUNTIME_LINK_RELS = {"stylesheet", "preload", "modulepreload", "icon", "manifest"}


class OfflineAssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.remote_assets: list[str] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        candidate = ""
        if tag in {"script", "img", "source"}:
            candidate = attrs.get("src") or ""
        elif tag == "link":
            rel = set((attrs.get("rel") or "").casefold().split())
            if rel.intersection(_RUNTIME_LINK_RELS):
                candidate = attrs.get("href") or ""
        if candidate and _REMOTE.match(candidate):
            self.remote_assets.append(candidate)


def verify_offline_site(site_dir: Path) -> list[str]:
    """Return deterministic findings for remote assets or missing offline search."""

    findings: list[str] = []
    if not site_dir.is_dir():
        return [f"offline site directory missing: {site_dir}"]

    search_index = site_dir / "search" / "search_index.js"
    if not search_index.is_file():
        findings.append("offline search index missing: search/search_index.js")

    for path in sorted(site_dir.rglob("*.html")):
        parser = OfflineAssetParser()
        try:
            parser.feed(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            findings.append(f"cannot read {path.relative_to(site_dir)}: {exc}")
            continue
        rel = path.relative_to(site_dir).as_posix()
        for url in sorted(set(parser.remote_assets)):
            findings.append(f"remote runtime asset: {rel} -> {url}")

    for path in sorted(site_dir.rglob("*.css")):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            findings.append(f"cannot read {path.relative_to(site_dir)}: {exc}")
            continue
        if _CSS_REMOTE.search(text):
            findings.append(f"remote runtime asset in CSS: {path.relative_to(site_dir).as_posix()}")

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site_dir", nargs="?", type=Path, default=Path("site-offline"))
    args = parser.parse_args(argv)
    findings = verify_offline_site(args.site_dir)
    for finding in findings:
        print(finding)
    if findings:
        return 1
    print("Offline site search and runtime assets verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
