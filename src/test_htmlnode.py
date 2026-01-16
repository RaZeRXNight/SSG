
import unittest

from htmlnode import HTMLNode;

class TestHTMLNode(unittest.TestCase):
    def test_results(self):
        node = HTMLNode("p", "hello world", [HTMLNode(), HTMLNode()], {"src": "Verizon"})
        print(node)
        self.assertTrue(node)

if __name__ == "__main__":
    unittest.main()

