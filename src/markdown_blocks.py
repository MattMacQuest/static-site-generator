from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    stripped_blocks = [block.strip() for block in blocks]
    
    stripped_blocks[:] = [block for block in stripped_blocks if block != ""]
    
    return stripped_blocks

def block_to_block_type(markdown: str):
    pass