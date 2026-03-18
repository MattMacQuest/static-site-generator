import unittest
from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_extra_newlines(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_markdown_to_blocks_to_block_type_simple(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        block_list = markdown_to_blocks(md)
        block_types = []
        for block in block_list:
            block_types.append(block_to_block_type(block))
        
        self.assertListEqual(
            [
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST
            ],
            block_types
        )
        
    def test_markdown_to_blocks_to_block_type_simple(self):
        md = """
This is **bolded** paragraph

1. This
2. Is
3. A
4. Numbered
5. List

> With some
> quotes from
> Mike

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

```
and finally some code
```
"""
        block_list = markdown_to_blocks(md)
        block_types = []
        for block in block_list:
            block_types.append(block_to_block_type(block))
        
        self.assertListEqual(
            [
                BlockType.PARAGRAPH,
                BlockType.ORDERED_LIST,
                BlockType.QUOTE,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST,
                BlockType.CODE
            ],
            block_types
        )
        
        
if __name__ == "__main__":
    unittest.main()