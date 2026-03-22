from __future__ import annotations

# Parent class for Leaf and Parent nodes
class HTMLNode():
    """Parent class for containing the HTML objects
    """
    def __init__(self, tag: str=None, value: str=None, children: HTMLNode=None, props: dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    # To be implemented by the inheritors
    def to_html(self):
        raise NotImplementedError()
    
    # Converts the properties of a node object into HTML. For things like
    # <a href="link"> where 'href="link"' is the prop
    def props_to_html(self) -> str:
        if self.props == None:
            return ""
        prop_list = []
        for key, value in self.props.items():
            prop_list.append(f" {key}=\"{value}\"")
        
        prop_string = "".join(prop_list)
        return prop_string
    
    def __eq__(self, other: HTMLNode) -> bool:
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )
    
    def __ne__(self, other: HTMLNode) -> bool:
        return (
            self.tag != other.tag
            or self.value != other.value
            or self.children != other.children
            or self.props != other.props
        )
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
# Class representing a node with no children. This, combined with the ParentNode class enables nested
# HTML handling
class LeafNode(HTMLNode):
    """Represents an HTML node with no children. Has a tag, a value, and optionally props

    Args:
        HTMLNode (_type_): Parent class
    """
    def __init__(self, tag: str, value: str, props: dict=None):
        super(LeafNode, self).__init__()
        self.tag = tag
        self.value = value
        self.props = props
        
    # Inheritor implementation of the to_html method. Takes the value of the LeafNode and converts
    # it into workable HTML
    def to_html(self) -> str:
        """converts the node to usable HTML string

        Raises:
            ValueError: Missing value field

        Returns:
            str: HTML string
        """
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
    
# Class representing a node with one or more children
class ParentNode(HTMLNode):
    """Represents an HTML node with children. Has a tag, children, and optionally props

    Args:
        HTMLNode (_type_): Parent class
    """
    def __init__(self, tag: str, children: list[ParentNode | LeafNode], props: dict=None):
        super(ParentNode, self).__init__()
        self.tag = tag
        self.children = children
        self.props = props
        
    # Inheritor implementation of the to_html method. Same as above. 
    # Does not pretty-print
    def to_html(self) -> str:
        """Converts the node and its children into workable HTML strings

        Raises:
            ValueError: In case of no tag
            ValueError: In case of missing child(ren)

        Returns:
            str: HTML string
        """
        if self.tag is None:
            raise ValueError("Tag missing")
        if self.children is None:
            raise ValueError("Child missing")
        
        html_string = f"<{self.tag}>"
        # print(html_string)
        for child in self.children:
            html_string += f"{child.to_html()}"
            # print(html_string)
        html_string += f"</{self.tag}>"
        return html_string

