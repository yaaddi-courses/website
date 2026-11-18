"""Tests for the website review tools.

Run from the Website folder:   python -m unittest discover -s tools -p "test_*.py"
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_links_live as links  # noqa: E402
import scan_claims as claims  # noqa: E402


class LinkTests(unittest.TestCase):
    def test_trailing_slash_and_www_are_not_a_move(self):
        self.assertEqual(links.classify("https://example.com/a", "https://www.example.com/a/", 200), "ok")

    def test_different_path_is_a_move(self):
        self.assertEqual(links.classify("https://example.com/a", "https://example.com/login", 200), "moved")

    def test_different_host_is_a_move(self):
        self.assertEqual(links.classify("http://a.com/x", "https://b.com/x", 200), "moved")

    def test_error_status_is_broken(self):
        self.assertEqual(links.classify("https://example.com/a", "https://example.com/a", 404), "broken")
        self.assertEqual(links.classify("https://example.com/a", "https://example.com/a", 0), "broken")

    def test_bot_blocking_is_unverified_not_broken(self):
        self.assertEqual(links.classify("https://linkedin.com/in/x", "https://linkedin.com/in/x", 999), "unverified")

    def test_title_extraction(self):
        self.assertEqual(links.title_of(b"<html><title> Hello \n World </title>"), "Hello World")


class ClaimTests(unittest.TestCase):
    def kinds(self, markup):
        return {k for ks, _ in claims.scan_text(markup) for k in ks}

    def test_flags_absolutes_and_numbers(self):
        got = self.kinds("<p>Yaaddi always works and has twenty question types.</p>")
        self.assertIn("absolute", got)
        self.assertIn("number", got)

    def test_ignores_scripts_and_styles(self):
        self.assertEqual(self.kinds("<script>var always = 1;</script><style>.best{}</style>"), set())

    def test_plain_sentence_is_not_flagged(self):
        self.assertEqual(self.kinds("<p>Open the Settings tab and tap Appearance.</p>"), set())


if __name__ == "__main__":
    unittest.main()
