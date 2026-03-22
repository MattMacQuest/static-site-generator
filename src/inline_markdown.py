from textnode import TextNode, TextType
import re

# TODO: Integrate nested markdown for things like combo **__bold italics__**

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """This inputs a list of TextNodes and breaks each node into a new list of TextNodes, splitting based on
 the provided delimiter and text type. Ex: inputting [TextNode(This is text with a **bolded** word, TextType.TEXT)]
 will split into ["This is text with a ", "bolded", " word"]

    Args:
        old_nodes (list[TextNode]): List of TextNodes to process
        delimiter (str): Delimiter to split the node on
        text_type (TextType): Target text type

    Raises:
        ValueError: Unclosed markdown tags

    Returns:
        list[TextNode]: New list of TextNodes with text_type extracted
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        holder = []
        split_node_text = node.text.split(delimiter)
        if len(split_node_text) % 2 == 0:
            raise ValueError("Invalid markdown, unclosed tag")
        
        for i in range(len(split_node_text)):
            # This is important because without it, the modulus will create a superfluous node when 
            # the last item is one of the markdown items, such as:
            # "This is **bolded** text with **another**"
            # The split function will split it into:
            # ["This is ", "bolded", " text with ", "another", ""]
            if split_node_text[i] == "":
                continue
            if i % 2 != 0:
                holder.append(TextNode(split_node_text[i], text_type))
            else:
                holder.append(TextNode(split_node_text[i], TextType.TEXT))
        new_nodes.extend(holder)
    return new_nodes

# This inputs a string of text and extracts any images that are present in markdown format and returns
# the combo as a tuple in the form (alt_text, URL)
def extract_markdown_images(text: str) -> list[tuple]:
    """Extracts all images using markdown syntax ![alt text](URL). Returns tuple of found (alt text, URL)"""
    
    # Image syntax: ![alt text](URL)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)
    
# This inputs a string of text and extracts any links that are present in markdown format and returns
# the combo as a tuple in the form (link_text, URL)
def extract_markdown_links(text: str) -> list[tuple]:
    """Extracts all links using markdown syntax [link text](URL). Returns tuple of found (link text, URL)"""

    # Link syntax: [link text](URL)
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

# The following functions do the same as split_nodes_delimiter but with links and images instead of 
# TextTypes
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """Splits list of text nodes on images found using markdown syntax

    Args:
        old_nodes (list[TextNode]): Old list of text nodes

    Returns:
        list[TextNode]: New list of text nodes with image information split into their own nodes
    """
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        # Extracts list of tuples of matched text from the node's text field. In this case matching the
        # ![alt text](URL) syntax
        image_tuples = extract_markdown_images(node.text)
        node_text = node.text
        
        # No images found, append the node
        if len(image_tuples) == 0:
            new_nodes.append(node)
            continue
        
        # Go over each tuple and split the text along the provided string and cuts empty portions
        for tuple in image_tuples:
            before, after = node_text.split(f"![{tuple[0]}]({tuple[1]})", 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(tuple[0], TextType.IMAGE, tuple[1]))
            node_text = after
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
            
    return new_nodes
        

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Splits list of text nodes on links found using markdown syntax

    Args:
        old_nodes (list[TextNode]): Old list of text nodes

    Returns:
        list[TextNode]: New list of text nodes with link information split into their own nodes
    """
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        link_tuples = extract_markdown_links(node.text)
        node_text = node.text
        
        if len(link_tuples) == 0:
            new_nodes.append(node)
            continue
        
        for tuple in link_tuples:
            # This uses the re module to avoid a situation where if someone writes something like:
            # "This is text with a ![link](same link) and a [link](same link)". Using the standard split
            # method, that would split improperly at the image. This covers that edge case. It is not
            # necessary for split_nodes_image as it is not a subset of split_nodes_link.
            before, after = re.split(r"(?<!!)\[" + re.escape(f"{tuple[0]}]({tuple[1]})"), node_text, maxsplit=1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(tuple[0], TextType.LINK, tuple[1]))
            node_text = after
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
            
    return new_nodes

# Function that simply calls the rest for ease of use
def text_to_textnodes(text: str) -> list[TextNode]:
    """Converts provided text into a list of text nodes"""
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes