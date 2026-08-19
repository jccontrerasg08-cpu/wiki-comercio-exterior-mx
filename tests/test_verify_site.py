from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.verify_site import LEGACY_ROUTES, verify_site


CANONICAL = "https://jccontrerasg08-cpu.github.io/wiki-comercio-exterior-mx/"


class SiteVerifierTests(unittest.TestCase):
    def _write(self, root: Path, relative: str, text: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _write_required_legacy_routes(self, root: Path) -> None:
        for relative, target in LEGACY_ROUTES.items():
            self._write(root, relative, f'<html><body><a href="{target}">redirect</a></body></html>')

    def test_broken_local_links_without_fragments_are_reported(self):
        with TemporaryDirectory() as tmp:
            site = Path(tmp)
            self._write_required_legacy_routes(site)
            self._write(
                site,
                "index.html",
                f'<html lang="es"><head><title>Inicio</title><link rel="canonical" href="{CANONICAL}"></head><body><a href="missing/">rota</a></body></html>',
            )
            self._write(
                site,
                "404.html",
                '<html lang="es"><head><title>No encontrado</title></head><body></body></html>',
            )

            findings = verify_site(site)

        self.assertIn("missing local target: index.html -> missing/", findings)

    def test_project_base_absolute_links_resolve(self):
        with TemporaryDirectory() as tmp:
            site = Path(tmp)
            self._write_required_legacy_routes(site)
            self._write(
                site,
                "index.html",
                f'<html lang="es"><head><title>Inicio</title><link rel="canonical" href="{CANONICAL}"></head><body><a href="/wiki-comercio-exterior-mx/wiki/destino/">destino</a></body></html>',
            )
            self._write(
                site,
                "wiki/destino/index.html",
                f'<html lang="es"><head><title>Destino</title><link rel="canonical" href="{CANONICAL}wiki/destino/"></head><body></body></html>',
            )
            self._write(
                site,
                "404.html",
                '<html lang="es"><head><title>No encontrado</title></head><body></body></html>',
            )

            self.assertEqual([], verify_site(site))

    def test_redirect_pages_are_not_treated_as_indexable_content(self):
        with TemporaryDirectory() as tmp:
            site = Path(tmp)
            self._write_required_legacy_routes(site)
            self._write(
                site,
                "index.html",
                f'<html lang="es"><head><title>Inicio</title><link rel="canonical" href="{CANONICAL}"></head><body></body></html>',
            )
            self._write(
                site,
                "404.html",
                '<html lang="es"><head><title>No encontrado</title></head><body></body></html>',
            )
            self._write(
                site,
                "old/topic/index.html",
                '<html><head><meta http-equiv="refresh" content="0; url=../../../wiki/topic/"></head><body></body></html>',
            )

            self.assertEqual([], verify_site(site))


if __name__ == "__main__":
    unittest.main()
