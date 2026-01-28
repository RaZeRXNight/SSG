import unittest

from extraction_nodes import *
from htmlnode import *;
from blocks import *;

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




if __name__ == "__main__":
    unittest.main()

