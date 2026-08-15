"""Verify legacy routes plus deterministic SEO/accessibility invariants in a built MkDocs site."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


LEGACY_ROUTES = {
    "aduana/documentos/index.html": "../../wiki/aduana/documentos/",
    "clasificacion/tigie-nico/index.html": "../../wiki/clasificacion/tigie-nico/",
    "programas/immex/index.html": "../../wiki/programas/immex/",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_lang = ""
        self.title_depth = 0
        self.title = ""
        self.canonical = ""
        self.ids: set[str] = set()
        self.local_hrefs: list[str] = []
        self.images_missing_alt = 0
        self.is_redirect_stub = False

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        if tag == "html":
            self.html_lang = attrs.get("lang") or ""
        if tag == "title":
            self.title_depth += 1
        element_id = attrs.get("id")
        if element_id:
            self.ids.add(element_id)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href") or ""
        if tag == "meta" and (attrs.get("http-equiv") or "").lower() == "refresh":
            self.is_redirect_stub = True
        if tag == "a":
            href = attrs.get("href")
            if href:
                self.local_hrefs.append(href)
        if tag == "img" and "alt" not in attrs:
            self.images_missing_alt += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_depth:
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title += data


def _parser(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def verify_site(site_dir: Path) -> list[str]:
    findings: list[str] = []

    for relative_path, target in LEGACY_ROUTES.items():
        path = site_dir / relative_path
        if not path.is_file():
            findings.append(f"missing legacy route: {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        if f'href="{target}"' not in text:
            findings.append(f"wrong redirect target: {relative_path} -> {target}")

    pages: dict[Path, PageParser] = {}
    for path in sorted(site_dir.rglob("*.html")):
        rel = path.relative_to(site_dir)
        if rel.as_posix() in LEGACY_ROUTES:
            continue
        parser = _parser(path)
        if parser.is_redirect_stub:
            continue
        pages[path] = parser
        if not parser.html_lang.lower().startswith("es"):
            findings.append(f"missing Spanish lang: {rel}")
        if not parser.title.strip():
            findings.append(f"missing title: {rel}")
        if rel.as_posix() != "404.html" and not parser.canonical.startswith(
            "https://jccontrerasg08-cpu.github.io/wiki-comercio-exterior-mx/"
        ):
            findings.append(f"missing or wrong canonical: {rel}")
        if parser.images_missing_alt:
            findings.append(f"images without alt ({parser.images_missing_alt}): {rel}")

    for path, parser in pages.items():
        rel = path.relative_to(site_dir)
        for href in parser.local_hrefs:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc or href.startswith(("mailto:", "tel:", "javascript:")):
                continue
            if href.startswith("#"):
                fragment = unquote(parsed.fragment)
                if fragment and fragment not in parser.ids:
                    findings.append(f"missing local fragment: {rel} -> #{fragment}")
                continue
            if not parsed.fragment:
                continue
            target_path = (path.parent / unquote(parsed.path)).resolve()
            if target_path.is_dir():
                target_path = target_path / "index.html"
            elif target_path.suffix != ".html":
                candidate = target_path / "index.html"
                if candidate.exists():
                    target_path = candidate
            try:
                target_parser = pages.get(target_path)
            except TypeError:
                target_parser = None
            if target_parser and unquote(parsed.fragment) not in target_parser.ids:
                findings.append(f"missing target fragment: {rel} -> {href}")

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site_dir", nargs="?", type=Path, default=Path("site"))
    args = parser.parse_args(argv)
    findings = verify_site(args.site_dir)
    for finding in findings:
        print(finding)
    if findings:
        return 1
    print("Site compatibility, SEO and static accessibility checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
