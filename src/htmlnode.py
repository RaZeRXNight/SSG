from enum import Enum
from extraction import extract_markdown_images, extract_markdown_links;
import re;

class TextType(Enum):
    TEXT = ""
    PLAIN = "plain"
    BOLD = "b"
    CODE = "code"
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


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise Exception("ERROR: OBJECT ENTERED IS NOT A TEXT NODE.")

    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", None, {"src": text_node.url})

def split_nodes_from_markdown(old_nodes, delimiter, text_type):
    new_nodes = list()
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise Exception("ERROR: INVALID DATA TYPE PASSED INTO SPLIT NODES")
        
        if node.text_type != text_type.TEXT or delimiter not in node.text:
            new_nodes.append(node)
            continue


        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"ERROR: ODD AMOUNT OF {delimiter} IN {node}")

        # Begin Splitting up the Text into Nodes
        collection = []
        counting = False
        for split_node in re.split(r'(\s+)', node.text):
            if split_node.startswith(delimiter) and split_node.endswith(delimiter):
                if collection:
                    new_nodes.append(TextNode("".join(collection), TextType.TEXT))
                    collection = []
                new_nodes.append(TextNode(split_node.strip(delimiter), text_type))
                continue
            else:
                if split_node.startswith(delimiter) and not counting:
                    new_nodes.append(TextNode("".join(collection), TextType.TEXT))
                    collection = []
                    collection.append(split_node.strip(delimiter))
                    counting = True
                    continue

                if split_node.endswith(delimiter) and counting:
                    collection.append(split_node.strip(delimiter))
                    counting = False
                    new_nodes.append(TextNode("".join(collection), text_type))
                    collection = []
                    continue

                if delimiter not in split_node and split_node:
                    collection.append(split_node)
        if collection:
            new_nodes.append(TextNode("".join(collection), TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    split_node_pattern = re.compile(r'(\!(.*?)*(?:\)))')
    
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise Exception("ERROR: INVALID DATA TYPE ENTERED")
        
        if not old_node.text_type == TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        split_nodes = list(filter(lambda x: x, re.split(split_node_pattern, old_node.text)))
        
        for index, node in enumerate(split_nodes):
            new_node = None
            extract = extract_markdown_images(node)

            if extract:
                new_node = TextNode(extract[0][0], TextType.IMAGE, extract[0][1])
            else:
                new_node = TextNode(node, TextType.TEXT, None)

            new_nodes.append(new_node)
    return new_nodes

node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)

def split_nodes_link(old_nodes):
    new_nodes = []
    split_node_pattern = re.compile(r'((?<!\!)\[(.*?)*(?:\)))')
    
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise Exception("ERROR: INVALID DATA TYPE ENTERED")
        
        if not old_node.text_type == TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        split_nodes = list(filter(lambda x: x, re.split(split_node_pattern, old_node.text)))
        
        for index, node in enumerate(split_nodes):
            new_node = None
            extract = extract_markdown_links(node)

            if extract:
                new_node = TextNode(extract[0][0], TextType.IMAGE, extract[0][1])
            else:
                new_node = TextNode(node, TextType.TEXT, None)

            new_nodes.append(new_node)
    return new_nodes