from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from markdown_blocks import markdown_to_html_node
from enum import Enum

def main():
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
    markdown_to_html_node(md)
    # print(node)
    # print(new_nodes)

if __name__ == "__main__":
    main()