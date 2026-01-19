
import unittest

from htmlnode import HTMLNode, LeafNode;

# class TestHTMLNode(unittest.TestCase):
#     def test_results(self):
#         node = HTMLNode("p", "hello world", [HTMLNode(), HTMLNode()], {"src": "Verizon"})
#         print(node)
#         self.assertTrue(node)

class TestLeafNode(unittest.TestCase):
    def test_results(self):
        node = LeafNode("p", "hello world", [HTMLNode(), HTMLNode()], {"src": "Tester"})
        print(node)
        print(node.to_html())
        self.assertTrue(node)

if __name__ == "__main__":
    unittest.main()

