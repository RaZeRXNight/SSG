from enum import Enum
import re 
from htmlnode import *;

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "#"
    CODE = "`"
    QUOTE = "\""
    UNORDERED_LIST = ""
    ORDERED_LIST = ""

def extract_markdown_images(text):
    """
    Returns a Tuple (Image Alt, Image Link)
    """
    return re.findall(r'\!\[(.*?)\]\((.*?)\)', text)

def extract_markdown_links(text):
    """
    Returns a Tuple (Image Alt, Image Link)
    """
    return re.findall(r'(?<!\!)\[(.*?)\]\((.*?)\)', text)

def block_to_block_type(old_block):
    """
    Retrieves the Block Type of a Block stripped from Markdown.
    """
    if re.match(r'^#*\ ', old_block):
        return BlockType.HEADING
    elif old_block.startswith("```") and old_block.endswith("```"):
        return BlockType.CODE
    elif re.match(r'(?m)^(\>\ )'):
        return BlockType.QUOTE
    elif re.match(r'(?m)(-\. )', old_block, re.MULTILINE):
        return BlockType.UNORDERED_LIST
    elif re.match(r'(\d\. )', old_block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    split_md, new_blocks = markdown.split("\n\n"), []

    for line in split_md:
        new_line = line.strip()
        if not new_line:
            continue
        new_blocks.append(new_line)

    return new_blocks

def text_to_html_nodes(text):
    first_nodes = [TextNode(text, TextType.TEXT, None)] # We turn the Text into a Text Node.
    
    # We're going to cycle through all the TextTypes we have covered, and convert the first_nodes into it's relevant nodes.

    first_nodes = split_nodes_link(split_nodes_image(first_nodes))
    
    for num in [TextType.BOLD, TextType.ITALIC, TextType.CODE]:
        first_nodes = split_nodes_from_markdown(first_nodes, num.value, num)

    return first_nodes

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