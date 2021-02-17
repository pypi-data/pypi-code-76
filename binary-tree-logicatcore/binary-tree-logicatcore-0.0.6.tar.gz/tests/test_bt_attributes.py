import pytest
from binary_tree.binary_tree import BT, Node

class TestBinaryTreeAttributes:

    def test_depth(self):
        """
        For a 10 elemets tree the tree would be as follows
                       1
                      / \
                     2   3
                    /\   /\
                   4  5 6  7
                  /\  |
                 8 9  10
        which has maximum depth/height of 3 for elements 8,9, and 10
        :return: None
        """
        import math
        bt = BT([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        assert math.floor(math.log2(10)) == bt.depth, "The calculated depth differs from the theoretical depth"

    def test_nodes_and_leafs_count(self):
        """
        For a 10 elemets tree the tree would be as follows
                       1
                      / \
                     2   3
                    /\   /\
                   4  5 6  7
                  /\  |
                 8 9  10
        which has 5 nodes and 5 leafs exactly
        :return: None
        """
        bt = BT([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        assert 5 == bt.nodes, "Number of nodes differs from the expected value"
        assert 5 == bt.leafs, "Number of leafs differs from the expected value"

    def test_conversion_to_elements(self):
        """
        Binary tree can be created in two different ways, one by supplying a Node object, second by supplying a list of
        elements. This test case checks the 'elements' attribute of the binary tree
        :return: None
        """
        x = BT(Node(1, Node(2, Node(4), Node(5)), Node(3, Node(6), Node(7))))
        assert [1, 2, 3, 4, 5, 6, 7] == x.elements, "The elements of the binary tree do not match"

        x = BT(list(range(10)))
        assert list(range(10)) == x.elements, "The elements of the binary tree do not match"