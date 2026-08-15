from __future__ import annotations

import unittest

from scripts.snice_discovery import DiscoveryPolicy


class SniceLiveContractTests(unittest.TestCase):
    def test_default_bound_covers_verified_current_index_size(self) -> None:
        # Web verification on 2026-08-15 showed the live Apache index exceeds
        # 4,194,305 bytes. Keep a bounded ceiling with enough operating room.
        self.assertGreaterEqual(DiscoveryPolicy().max_bytes, 8 * 1024 * 1024)


if __name__ == "__main__":
    unittest.main()
