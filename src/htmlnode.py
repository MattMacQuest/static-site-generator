class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        prop_list = []
        for key, value in self.props.items():
            prop_list.append(f" {key}=\"{value}\"")
        
        prop_string = "".join(prop_list)
        return prop_string
    
    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )
    
    def __ne__(self, other):
        return (
            self.tag != other.tag
            or self.value != other.value
            or self.children != other.children
            or self.props != other.props
        )
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"