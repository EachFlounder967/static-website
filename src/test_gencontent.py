import unittest

from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_h1(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_whitespace_stripped(self):
        markdown = "   #   Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_missing_h1_raises(self):
        markdown = "## Not an h1\nJust text"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_eq(self):
        actual = extract_title("# This is a title")
        self.assertEqual(actual, "This is a title")

    def test_eq_double(self):
        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")

    def test_eq_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list
"""
        )
        self.assertEqual(actual, "title")

    def test_none(self):
        with self.assertRaises(Exception):
            extract_title(
                """
no title
"""
            )


if __name__ == "__main__":
    unittest.main()

