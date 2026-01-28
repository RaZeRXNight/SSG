import re
from enum import Enum
from htmlnode import TextNode, HTMLNode, ParentNode
from extraction_nodes import text_to_html_nodes, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"

def block_to_block_type(old_block):
    """
    Retrieves the Block Type of a Block stripped from Markdown.
    """
    if re.match(r'^#*\ ', old_block):
        return BlockType.HEADING
    elif old_block.startswith("```") and old_block.endswith("```"):
        return BlockType.CODE
    elif re.match(r'^(\>\ )', old_block, flags=re.MULTILINE):
        return BlockType.QUOTE
    elif re.match(r'(?m)(\-\ )', old_block, re.MULTILINE):
        return BlockType.UNORDERED_LIST
    elif re.match(r'(?m)(\d\.\ )', old_block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    """_Converts the markdown text into blocks, being able to be parse easier for htmlnodes._

    Args:
        markdown (_type_): _Markdown Text_

    Returns:
        _list_: _A List of blocks, made up of each separate line from the markdown text._
    """
    split_md, new_blocks = markdown.split("\n\n"), []

    for line in split_md:
        new_line = line.strip()
        if not new_line:
            continue
        new_blocks.append(new_line)

    return new_blocks

def html_node_from_block(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode(BlockType.PARAGRAPH.value, block)
        case BlockType.HEADING:
            count = 0
            for char in block:
                if char != "#":
                    break
                count+=1
            return ParentNode(f"h{str(count)}", block)
        case BlockType.CODE:
            return ParentNode(BlockType.CODE.value, block)
        case BlockType.QUOTE:
            return ParentNode(BlockType.QUOTE.value, block)
        case BlockType.UNORDERED_LIST:
            return ParentNode(BlockType.UNORDERED_LIST.value, block)
        case BlockType.ORDERED_LIST:
            return ParentNode(BlockType.ORDERED_LIST.value, block)

def text_to_children(text):
    text_nodes = text_to_html_nodes(text)
    leaf_nodes = list(map(lambda x: text_node_to_html_node(x), text_nodes))
    return leaf_nodes

def markdown_to_html_node(markdown):
    parent_node = ParentNode("div", [])

    # break down the text line by line into blocks, and iterate through them.
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = html_node_from_block(block, block_type)

        # We get the inline children from the HTML Node with the text_to_children function.
        if block_type == BlockType.CODE:
            html_node.children = text_to_children(markdown)
        else: 
            html_node.children = text_to_children(markdown)

        parent_node.children.append(html_node)
    
    return parent_node


