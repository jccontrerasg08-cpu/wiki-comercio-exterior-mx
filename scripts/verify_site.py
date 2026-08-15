"""Verify representative compatibility routes in a built MkDocs site."""

from __future__ import annotations

import argparse
from pathlib import Path


LEGACY_ROUTES = {
    "aduana/documentos/index.html": "../../wiki/aduana/documentos/",
    "clasificacion/tigie-nico/index.html": "../../wiki/clasificacion/tigie-nico/",
    "programas/immex/index.html": "../../wiki/programas/immex/",
}


def verify_site(site_dir: Path) -> list[str]:
    """Return missing or misdirected representative legacy routes."""

    findings: list[str] = []
    for relative_path, target in LEGACY_ROUTES.items():
        path = site_dir / relative_path
        if not path.is_file():
            findings.append(f"missing legacy route: {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        if f'href="{target}"' not in text:
            findings.append(f"wrong redirect target: {relative_path} -> {target}")
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
    print("Legacy site routes verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
