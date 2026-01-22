
import unittest

from extraction import *
from htmlnode import HTMLNode, LeafNode, ParentNode, TextType, TextNode, text_node_to_html_node, split_nodes_from_markdown;

# class TestHTMLNode(unittest.TestCase):
#     def test_results(self):
#         node = HTMLNode("p", "hello world", [HTMLNode(), HTMLNode()], {"src": "Verizon"})
#         print(node)
#         self.assertTrue(node)

# class TestLeafNode(unittest.TestCase):
#     def test_results(self):
#         node = LeafNode("p", "hello world", [HTMLNode(), HTMLNode()], {"src": "Tester"})
#         print(node)
#         print(node.to_html())
#         self.assertTrue(node)

# class TestParentNode(unittest.TestCase):
#     def test_results(self):
#         node = ParentNode("p", [LeafNode("c", "hello world"), LeafNode("b", "for zero!")], {"src": "Tester"})
#         print(node.to_html())
#         self.assertTrue(node)

#     def test1_results(self):
#         node = ParentNode("p", 
#                           [LeafNode("c", "hello world"), ParentNode("z", [LeafNode("c", "hello world"), LeafNode("c", "hello world")])], 
#                           {"src": "Tester"}
#                           )
#         print(node.to_html())
#         self.assertTrue(node)

#     def test_2results(self):
#         node = TextNode("This is a text node", TextType.TEXT)
#         html_node = text_node_to_html_node(node)
#         self.assertEqual(html_node.tag, None)
#         self.assertEqual(html_node.value, "This is a text node")

# class TestMD_To_TextNode(unittest.TestCase):
#     def test_1result(self):
#         Texttype = TextType.CODE
#         node = split_nodes_from_markdown([TextNode("I have super `HELLO WORLD` `loud` powers", TextType.TEXT)], "`", Texttype)
#         # self.assertTrue(len(node) == 4)
#         print("PASSED", node)
#     def test_2result(self):
#         Texttype = TextType.CODE
#         node = split_nodes_from_markdown([TextNode("I have super `HELLO WORLD` `loud` powers", TextType.TEXT)], "`", Texttype)
#         # self.assertTrue(len(node) == 4)
#         print("PASSED", node)
#     def test_3result(self):
#         Texttype = TextType.BOLD
#         node = split_nodes_from_markdown([TextNode("I have super **HELLO WORLD** `loud` powers", TextType.TEXT)], "**", Texttype)
#         # self.assertTrue(len(node) == 3)
        # print("PASSED", node)

class TextExtration(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

if __name__ == "__main__":
    unittest.main()

