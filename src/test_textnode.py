import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_bold_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_itl_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_with_none_url(self):
        node = TextNode("This is a text node", TextType.LINK, None)
        node2 = TextNode("This is a text node", TextType.LINK, None)
        self.assertEqual(node, node2)

    def test_new_eq_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_neq_with_different_urls(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://example.org")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("hello", TextType.BOLD, "https://test.com")
        node2 = "TextNode(hello, bold, https://test.com)"
        self.assertEqual(repr(node), node2)

    def test_repr_with_none_url(self):
        node = TextNode("hello", TextType.BOLD, None)
        node2 = "TextNode(hello, bold, None)"
        self.assertEqual(repr(node), node2)


if __name__ == "__main__":
    unittest.main()
