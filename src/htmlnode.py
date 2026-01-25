from enum import Enum
import re;

class TextType(Enum):
    TEXT = ""
    PLAIN = ""
    ITALIC = "_"
    BOLD = "**"
    CODE = "`"
    LINK = "a"
    IMAGE = "img"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text;
        self.text_type = text_type;
        self.url = url;

    def __eq__(self, other):
        if isinstance(other, TextNode):
            if [self.text, self.text_type, self.url] == [other.text, other.text_type, other.url]:
                return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

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

class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("ERROR: NO VALUE PROVIDED")

        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.children}, {self.props_to_html()}"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ERROR: NO VALID TAG ASSIGNED")
        
        if not self.children:
            raise ValueError("ERROR: NO VALID CHILDREN")
        children_html = "".join([x.to_html() for x in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"