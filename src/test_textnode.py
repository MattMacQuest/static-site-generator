import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
    def test_ne2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node?", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_default_constructor(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)
        
    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )
    
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")
        
# class TestSplitNodesDelimiter(unittest.TestCase):
#     def test_code(self):
#         node = TextNode("This is text with a `code block` word", TextType.TEXT)
#         new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
#         self.assertEqual(new_nodes[0].text, "This is text with a ")
#         self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
#         self.assertEqual(new_nodes[1].text, "code block")
#         self.assertEqual(new_nodes[1].text_type, TextType.CODE)
#         self.assertEqual(new_nodes[2].text, " word")
#         self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        
#     def test_bold(self):
#         node = TextNode("This is text with a **bold** word", TextType.TEXT)
#         new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
#         self.assertEqual(new_nodes[0].text, "This is text with a ")
#         self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
#         self.assertEqual(new_nodes[1].text, "bold")
#         self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
#         self.assertEqual(new_nodes[2].text, " word")
#         self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        
#     def test_italic(self):
#         node = TextNode("This is text with an __italic__ word", TextType.TEXT)
#         new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)
#         self.assertEqual(new_nodes[0].text, "This is text with an ")
#         self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
#         self.assertEqual(new_nodes[1].text, "italic")
#         self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
#         self.assertEqual(new_nodes[2].text, " word")
#         self.assertEqual(new_nodes[2].text_type, TextType.TEXT)


if __name__ == "__main__":
    unittest.main()