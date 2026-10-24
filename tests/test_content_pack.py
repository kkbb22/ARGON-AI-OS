import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from content_pack import build_content


class ContentPackTests(unittest.TestCase):
    def test_contains_three_platform_drafts(self):
        package = build_content()
        self.assertEqual(
            set(package["platforms"]),
            {"instagram", "facebook", "x"}
        )

    def test_requires_human_review(self):
        package = build_content()
        self.assertEqual(package["status"], "DRAFT_REQUIRES_HUMAN_REVIEW")
        self.assertFalse(package["publishing"]["published"])
        self.assertFalse(package["publishing"]["automatic_publishing_enabled"])

    def test_has_review_checklist(self):
        package = build_content()
        self.assertGreaterEqual(len(package["review_checklist"]), 4)

    def test_drafts_are_not_empty(self):
        package = build_content()
        for draft in package["platforms"].values():
            self.assertTrue(draft.strip())


if __name__ == "__main__":
    unittest.main(verbosity=2)
