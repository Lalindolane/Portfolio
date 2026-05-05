"""Unit testing file for binary_trees.py"""

import binary_trees
import pytest


@pytest.fixture # pytest fixture to help in the construction of a tree
def build_the_tree():
    tree_1 = binary_trees.BST()
    for i in [4, 3, 8, 1, 2, 9, 23, 6, 5, 7]:
        tree_1.insert(i)
    return tree_1


def test_dll_insert():
    """Unit test problem 1, creating an insert method for your DoublyLinkedList class."""
    list1 = binary_trees.DoublyLinkedList()

    list1.insert(0, 0)
    assert list1.__str__() == '[0]', 'failed to insert in an empty list'

    list1.insert(0, 1)
    assert list1.__str__() == '[1, 0]', 'failed to insert at beginning of list'

    list1.insert(2, 2)
    assert list1.__str__() == '[1, 0, 2]', 'failed to insert at end of list'

    list1.insert(2, 3)
    assert list1.__str__() == '[1, 0, 3, 2]', 'failed to insert in middle of list'

    assert list1.head.value == 1, 'failed to track head attribute'
    assert list1.tail.value == 2, 'failed to track tail attribute'

    with pytest.raises(IndexError):
        list1.insert(5, 4), "Did not raise an index error for trying to insert at an invalid index"


def test_bst_insert(build_the_tree):
    """Unit test problem 3, creating an insert method for your BST class."""

    tree1 = build_the_tree
    assert tree1.root.value == 4, "root inserted incorrectly"

    parent = tree1.root
    assert parent.right.value == 8, "right child of root inserted incorrectly"
    assert parent.left.value == 3, "left child of root inserted incorrectly"

    val1 = parent.left
    assert val1.left.value == 1, "left child with no right child inserted incorrectly"
    assert val1.right is None, "right child of node should be None"

    val2 = parent.right.left
    assert val2.left.value == 5, "left child of node in middle of tree is incorrect"
    assert val2.right.value == 7, "right child of node in middle of tree is incorrect"

    val3 = parent.right.right.right
    assert val3.left is None, "base level of tree should have no left child"
    assert val3.right is None, "base level of tree should have no right child"

    with pytest.raises(ValueError):
        tree1.insert(1), "Did not raise a value error for trying to insert a duplicate node"

    #check if insertion of one node is correct
    tree2 = binary_trees.BST()
    tree2.insert(1)
    val4 = tree2.root

    assert val4.left is None
    assert val4.right is None
    assert val4.prev is None


def test_bst_remove():
    tree = binary_trees.BST()
    for i in [5, 3, 4, 1, 7, 6]:
        tree.insert(i)

    # Remove a leaf node
    tree.remove(4)
    assert tree.root.value == 5
    assert tree.root.left.value == 3
    assert tree.root.left.right is None

    # Remove a node with one child
    tree.remove(7)
    assert tree.root.right.value == 6
    assert tree.root.right.left is None
    assert tree.root.right.right is None

    # Remove root node with two children
    tree.remove(5)
    assert tree.root.value == 3
    # Check that the tree still contains valid BST structure
    assert tree.root.left.value == 1
    assert tree.root.right.value == 6

    # check for the case that removal is happening and the predecessor is the child of the target
    tree = binary_trees.BST()
    nodes = [5, 4, 6, 3, 7]
    for node in nodes:
        tree.insert(node)
    tree.remove(4)
    assert tree.root.value == 5
    assert tree.root.left.value == 3
