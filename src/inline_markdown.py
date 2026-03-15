from textnode import TextNode, TextType

# TODO: Integrate nested markdown for things like combo **__bold italics__**
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    # print(old_nodes[0])
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