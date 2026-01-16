

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # The Tag/Elements
        self.value = value # value contained inside of this HTMLNode
        self.children = children # Elements underneath this HTMLNode
        self.props = props # These are Attributes given to an html element `src='url_here'`

    def to_html(self):
        raise NotImplementedError("ERROR: THIS FEATURE HAS NOT BEEN IMPLEMENTED YET!")

    def props_to_html(self):
        if not self.props:
            return ""

        attributes = ""
        for prop in self.props:
            attributes+=f" {prop}=\"{self.props[prop]}\""
        return attributes

    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.children}, {self.props_to_html()}"
