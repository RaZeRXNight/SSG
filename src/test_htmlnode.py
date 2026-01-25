
import unittest

from extraction import *
from htmlnode import HTMLNode, LeafNode, ParentNode, TextType, TextNode;
from extraction import *;

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

class TextSplit_Nodes(unittest.TestCase):
    # def test_split_nodes_image1(self):
    #     matches = split_nodes_image([TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)])
    #     print(matches)
    #     # self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    # def test_split_nodes_image2(self):
    #     matches = split_nodes_image([TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)])
    #     print(matches)
    #     self.assertEqual(4, len(matches))

    def test_split_node_links(self):
        matches = split_nodes_link([TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)])
        print(matches)
        self.assertIn(TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), matches)
        
    def test_text_to_html_nodes(self):
        matches = text_to_html_nodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        for node in matches:
            print(node)
        self.assertIn(TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), matches)


if __name__ == "__main__":
    unittest.main()

