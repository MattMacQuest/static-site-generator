from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
from inline_markdown import text_to_textnodes, split_nodes_delimiter, split_nodes_image, split_nodes_link

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    """Inputs a markdown string and breaks it into a list of substrings representing
    the blocks of text

    Args:
        markdown (str): Markdown string

    Returns:
        list[str]: List of found substrings where each item is an individual block
    """
    blocks = markdown.split("\n\n")
    stripped_blocks = [block.strip() for block in blocks]
    
    stripped_blocks[:] = [block for block in stripped_blocks if block != ""]
    
    return stripped_blocks

def block_to_block_type(block: str) -> BlockType:
    """Returns what type of block the provided string is

    Args:
        block (str): Block of markdown txt

    Returns:
        BlockType: 
    """
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")
    
    
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str) -> ParentNode:
    """Generates the top-level ParentNode for an entire markdown text

    Args:
        markdown (str): A markdown document in string format

    Returns:
        HTMLNode: The top-level ParentNode
    """
    blocks = markdown_to_blocks(markdown)
    
    node_list: list[HTMLNode | LeafNode | ParentNode] = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        # A helper function might be useful here for readability
        # All blocks are ParentNodes with children created from text_node_to_html_node
        if block_type == BlockType.PARAGRAPH:
            # It isn't entirely necessary but I believe replacing newlines with spaces will
            # make things easier
            block = block.replace("\n", " ")
            
            children = text_to_children(block)
            
            parent = ParentNode("p", children)
            node_list.append(parent)

        elif block_type == BlockType.HEADING:
            heading_number = 0
            for char in block:
                if char == "#":
                    heading_number += 1
                else:
                    break
            
            if heading_number + 1 >= len(block):
                raise ValueError(f"invalid heading level: {heading_number}")
            
            text = block[heading_number + 1 :]
            
            children = text_to_children(text)
            parent = ParentNode(f"h{heading_number}", children)
            
            node_list.append(parent)
            
        elif block_type == BlockType.CODE:
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError("invalid code block")
            code_block = TextNode(block.strip("```").lstrip("\n"), TextType.TEXT)
            code_block_html = text_node_to_html_node(code_block)
            
            parent = ParentNode("code", [code_block_html])
            node_list.append(ParentNode("pre", [parent]))
                        
        elif block_type == BlockType.QUOTE:
            block = block.replace(">", "").replace("\n", "").strip()
            children = text_to_children(block)
            parent = ParentNode("blockquote", children)
            
            node_list.append(parent)
        
        # List nodes' children will be ParentNodes to each list item
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            children: list[ParentNode] = []
            for line in lines:
                children.append(ParentNode("li", text_to_children(line[2:])))
            parent = ParentNode("ul", children)
            node_list.append(parent)
        
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            children: list[ParentNode] = []
            for line in lines:
                children.append(ParentNode("li", text_to_children(line[3:])))
            parent = ParentNode("ol", children)
            node_list.append(parent)
            
        else:
            raise ValueError("invalid block type")
    
    return ParentNode("div", node_list)


# This function will take the text of a block and break it into the appropriate TextNodes, passing
# those into text_node_to_html_node() function, generating the LeafNodes
def text_to_children(text: str) -> list[LeafNode]:
    """Inputs the text of a block and generates a list of leafnodes, ready to be added to a parent
    
    Args:
        text (str): Block text

    Returns:
        list[LeafNode]: list of children
    """
    text_nodes = text_to_textnodes(text)
    html_nodes: list[LeafNode] = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    
    return html_nodes