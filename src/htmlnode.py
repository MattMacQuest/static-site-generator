class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.propr = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        pass
    
    def __repr__(self):
        pass