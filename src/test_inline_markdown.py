import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link
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
                TextNode(" word", TextType.TEXT)
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
            new_nodes
        )
    
    def test_delim_italic(self):
        node = TextNode(
            "This is text with an __italic__ word", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_multi_delim(self):
        node = TextNode(
            "This is text with both __italic__ and **bold** words", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "__", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with both ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" words", TextType.TEXT)
            ],
            new_nodes
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
        
    def test_extract_img(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )
        
    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"),
             ("to youtube", "https://www.youtube.com/@bootdotdev")],
            matches
        )
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_no_link(self):
        node = TextNode(
            "This is text with no link",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no link", TextType.TEXT)
            ],
            new_nodes,
        )
        
    def test_no_image(self):
        node = TextNode(
            "This is text with no image",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no image", TextType.TEXT)
            ],
            new_nodes,
        )
        
    def test_mixed_image(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes
        )
        
    def test_mixed_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_link_matching(self):
        node = TextNode(
            "This is text with a ![link](same link) and a [link](same link)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ![link](same link) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "same link")
            ],
            new_nodes
        )
        
    def test_image_matching(self):
        node = TextNode(
            "This is text with a [link](same link) and a ![link](same link)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a [link](same link) and a ", TextType.TEXT),
                TextNode("link", TextType.IMAGE, "same link")
            ],
            new_nodes
        )
        
    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )
        
    def test_split_link_single(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes
        )
        
    # This test will try to split one, then the other
    def test_split_links_then_images(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes
        )

    def test_split_delimiter_and_image(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and an ![image](https://i.imgur.com/zjjcJKZ.png), and some **bold** text too",
            TextType.TEXT
        )
        
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_image(new_nodes)
        new_nodes = split_nodes_link(new_nodes)
        
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(", and some ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text too", TextType.TEXT)
            ],
            new_nodes
        )