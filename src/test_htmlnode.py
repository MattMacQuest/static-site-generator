import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_ne(self):
        node = HTMLNode("a", "googler", None, None)
        node2 = HTMLNode("a", "google", None, None)
        self.assertNotEqual(node, node2)
    
    def test_eq(self):
        node = HTMLNode("a", "google", None, None)
        node2 = HTMLNode("a", "google", None, None)
        self.assertEqual(node, node2)
    
    def test_props_to_html(self):
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

if __name__ == "__main__":
    unittest.main()