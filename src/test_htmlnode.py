import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # ---- HTMLNode tests ----
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode("div", "I wish I could read")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    # ---- LeafNode tests ----
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_one_child(self):
        child = LeafNode("p", "hello")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><p>hello</p></div>")

    def test_to_html_multiple_children(self):
        child1 = LeafNode("p", "hello")
        child2 = LeafNode("span", "world")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><p>hello</p><span>world</span></div>",
        )

    def test_to_html_nested_parent(self):
        inner_child = LeafNode("b", "bold")
        inner_parent = ParentNode("span", [inner_child])
        outer_parent = ParentNode("div", [inner_parent])
        self.assertEqual(
            outer_parent.to_html(),
            "<div><span><b>bold</b></span></div>",
        )

    def test_to_html_tag_none(self):
        child = LeafNode("p", "hello")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_children_none(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_children_empty_list(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")


if __name__ == "__main__":
    unittest.main()
