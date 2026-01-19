
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode;

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

class TestParentNode(unittest.TestCase):
    def test_results(self):
        node = ParentNode("p", [LeafNode("c", "hello world"), LeafNode("b", "for zero!")], {"src": "Tester"})
        print(node.to_html())
        self.assertTrue(node)

    def test1_results(self):
        node = ParentNode("p", 
                          [LeafNode("c", "hello world"), ParentNode("z", [LeafNode("c", "hello world"), LeafNode("c", "hello world")])], 
                          {"src": "Tester"}
                          )
        print(node.to_html())
        self.assertTrue(node)

if __name__ == "__main__":
    unittest.main()

