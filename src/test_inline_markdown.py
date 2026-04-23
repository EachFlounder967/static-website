import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "Here is ![img1](url1.png) and ![img2](url2.png)"
        )
        self.assertListEqual(
            [("img1", "url1.png"), ("img2", "url2.png")],
            matches,
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This text has no images at all")
        self.assertListEqual([], matches)

    def test_extract_markdown_mixed_content(self):
        text = "Here is an ![image](img.png) and a [link](https://boot.dev)"

        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)

        self.assertListEqual([("image", "img.png")], image_matches)
        self.assertListEqual([("link", "https://boot.dev")], link_matches)

    def test_extract_markdown_links_basic(self):
        matches = extract_markdown_links(
            "Visit [Boot.dev](https://boot.dev) and [Google](https://google.com)"
        )
        self.assertListEqual(
            [("Boot.dev", "https://boot.dev"), ("Google", "https://google.com")],
            matches,
        )

    def test_split_link(self):
        node = TextNode(
            "Visit [Boot.dev](https://boot.dev) and [Google](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "Here is an ![image](img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "img.png"),
            ],
            new_nodes,
        )

    def test_split_image_and_link(self):
        node = TextNode(
            "Here is ![img](img.png) and a [link](https://boot.dev)",
            TextType.TEXT,
        )

        image_nodes = split_nodes_image([node])
        link_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "img.png"),
                TextNode(" and a [link](https://boot.dev)", TextType.TEXT),
            ],
            image_nodes,
        )

        self.assertListEqual(
            [
                TextNode("Here is ![img](img.png) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            link_nodes,
        )

    def test_split_no_images_or_links(self):
        node = TextNode(
            "Just plain text here",
            TextType.TEXT,
        )

        image_nodes = split_nodes_image([node])
        link_nodes = split_nodes_link([node])

        self.assertListEqual([node], image_nodes)
        self.assertListEqual([node], link_nodes)

    def test_split_multiple_images_with_text_around(self):
        node = TextNode(
            "Start ![one](1.png) middle ![two](2.png) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "1.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "2.png"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    # tests for split_nodes_link and split_nodes_image with multiple images and links in the same text node
    #
    def test_text_to_textnodes_happy_path(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_plain_text(self):
        text = "Just plain text"
        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            nodes,
        )

    def test_text_to_textnodes_only_bold(self):
        text = "**bold**"
        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            nodes,
        )

    def test_text_to_textnodes_only_link(self):
        text = "[Boot.dev](https://boot.dev)"
        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [TextNode("Boot.dev", TextType.LINK, "https://boot.dev")],
            nodes,
        )

    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
