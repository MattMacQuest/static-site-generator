from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter
from enum import Enum

def main():
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    # print(node)
    # print(new_nodes)

if __name__ == "__main__":
    main()