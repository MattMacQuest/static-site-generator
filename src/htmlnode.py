from __future__ import annotations

class HTMLNode():
    def __init__(self, tag: str=None, value: str=None, children: HTMLNode=None, props: dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
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
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict=None):
        super(LeafNode, self).__init__()
        self.tag = tag
        self.value = value
        self.props = props
        
    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: HTMLNode, props: dict=None):
        super(ParentNode, self).__init__()
        self.tag = tag
        self.children = children
        self.props = props
        
    def to_html(self) -> str:
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

