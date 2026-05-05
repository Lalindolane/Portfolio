# binary_trees.py
"""Volume 2: Binary Trees.
<Lane Lindstrom>
<Math 321>
<2/12/2026>
"""

# These imports are used in BST.draw().
from time import perf_counter as time
from matplotlib import pyplot as plt
import random

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout


class DoublyLinkedListNode:
    """A node with a value and references to the previous and next nodes."""
    def __init__(self, data):
        self.value = data
        self.prev, self.next = None, None


class DoublyLinkedList:
    """A doubly linked list with a head and a tail."""
    def __init__(self):
        self.head, self.tail = None, None
        self.size = 0

    def __len__(self):
        '''Return the number of nodes in the list.'''
        return self.size

    def __str__(self):
        '''Format and return the list like a standard Python list.'''
        result = []
        current = self.head
        while current:
            result.append(str(current.value))
            current = current.next
        return '[' + ', '.join(result) + ']'

    # Problem 1
    def insert(self, index, data):
        '''Insert a piece of data as a new node before the given
        index so that the new node is now at index.
        '''
        node = DoublyLinkedListNode(data)
        if index < 0 or index > self.size:
            raise IndexError
        elif self.head is None:
            self.head = self.tail = node
        elif self.size == index:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        elif index == 0:
            node.next = self.head
            self.head.prev = node
            self.head = node
        else:
            current = self.head
            for _ in range(index):
                current = current.next
            current.prev.next = node
            node.prev = current.prev
            current.prev = node
            node.next = current
        self.size += 1

    def iterative_find(self, data):
        """Search iteratively for a node containing the data.
        If there is no such node in the list, including if the list is empty,
        raise a ValueError.

        Returns:
            (DoublyLinkedListNode): the node containing the data.
        """
        current = self.head
        while current is not None:
            if current.value == data:
                return current
            current = current.next
        raise ValueError(str(data) + " is not in the list")

    # Problem 2
    def recursive_find(self, data):
        """Search recursively for the node containing the data.
        If there is no such node in the list, including if the list is empty,
        raise a ValueError.

        Returns:
            (DoublyLinkedListNode): the node containing the data.
        """
        current = self.head
        if current is None:
            raise ValueError(str(data) + ' is not in the list')

        def recursive_find_helper(node, data):
            if node.value == data:
                return node
            elif node.next is None:
                raise ValueError(str(data) + " is not in the list")
            return recursive_find_helper(node.next, data)

        return recursive_find_helper(self.head, data)


class BSTNode:
    """A node class for binary search trees. Contains a value, a
    reference to the parent node, and references to two child nodes.
    """
    def __init__(self, data):
        """Construct a new node and set the value attribute. The other
        attributes will be set when the node is added to a tree.
        """
        self.value = data
        self.prev = None        # A reference to this node's parent node.
        self.left = None        # self.left.value < self.value
        self.right = None       # self.value < self.right.value


class BST:
    """Binary search tree data structure class.
    The root attribute references the first node in the tree.
    """
    def __init__(self):
        """Initialize the root attribute."""
        self.root = None

    def find(self, data):
        """Return the node containing the data. If there is no such node
        in the tree, including if the tree is empty, raise a ValueError.
        """

        # Define a recursive function to traverse the tree.
        def _step(current):
            """Recursively step through the tree until the node containing
            the data is found. If there is no such node, raise a Value Error.
            """
            if current is None:                     # Base case 1: dead end.
                raise ValueError(str(data) + " is not in the tree.")
            if data == current.value:               # Base case 2: data found!
                return current
            if data < current.value:                # Recursively search left.
                return _step(current.left)
            else:                                   # Recursively search right.
                return _step(current.right)

        # Start the recursion on the root of the tree.
        return _step(self.root)

    # Problem 3
    def insert(self, data):
        """Insert a new node containing the specified data.

        Raises:
            ValueError: if the data is already in the tree.

        Example:
            >>> tree = BST()                    |
            >>> for i in [4, 3, 6, 5, 7, 8, 1]: |            (4)
            ...     tree.insert(i)              |            / \
            ...                                 |          (3) (6)
            >>> print(tree)                     |          /   / \
            [4]                                 |        (1) (5) (7)
            [3, 6]                              |                  \
            [1, 5, 7]                           |                  (8)
            [8]                                 |
        """

        if self.root is None:
            self.root = BSTNode(data)
            return

        def _insert(node, data):

            if data == node.value:
                raise ValueError
            elif data < node.value:
                if node.left is None:
                    new_node = BSTNode(data)
                    node.left = new_node
                    new_node.prev = node
                    return
                else:
                    _insert(node.left, data)
            else:
                if node.right is None:
                    new_node = BSTNode(data)
                    node.right = new_node
                    new_node.prev = node
                    return
                else:
                    _insert(node.right, data)
        _insert(self.root, data)

    # Problem 4
    def remove(self, data):
        """Remove the node containing the specified data.

        Raises:
            ValueError: if there is no node containing the data, including if
                the tree is empty.

        Examples:
            >>> print(12)                       | >>> print(t3)
            [6]                                 | [5]
            [4, 8]                              | [3, 6]
            [1, 5, 7, 10]                       | [1, 4, 7]
            [3, 9]                              | [8]
            >>> for x in [7, 10, 1, 4, 3]:      | >>> for x in [8, 6, 3, 5]:
            ...     t1.remove(x)                | ...     t3.remove(x)
            ...                                 | ...
            >>> print(t1)                       | >>> print(t3)
            [6]                                 | [4]
            [5, 8]                              | [1, 7]
            [9]                                 |
                                                | >>> print(t4)
            >>> print(t2)                       | [5]
            [2]                                 | >>> t4.remove(1)
            [1, 3]                              | ValueError: <message>
            >>> for x in [2, 1, 3]:             | >>> t4.remove(5)
            ...     t2.remove(x)                | >>> print(t4)
            ...                                 | []
            >>> print(t2)                       | >>> t4.remove(5)
            []                                  | ValueError: <message>
        """
        # Find the target node to remove
        target = self.find(data)
        parent = target.prev

        # Case 1: Target is a leaf node
        if target.left is None and target.right is None:
            if parent is None:
                self.root = None
            elif parent.left == target:
                parent.left = None
            else:
                parent.right = None

        # if Target has two children
        elif target.left is not None and target.right is not None:

            # Find in-order predecessor
            predecessor = target.left
            while predecessor.right is not None:
                predecessor = predecessor.right

            # Copy value
            target.value = predecessor.value

            # Remove predecessor
            pred_parent = predecessor.prev
            child = predecessor.left  # this may be None

            # If predecessor is left child of its parent
            if pred_parent.left == predecessor:
                pred_parent.left = child
            else:
                pred_parent.right = child

            if child is not None:
                child.prev = pred_parent

        # Case 3: Target has only a right child
        elif target.left is None:
            if parent is None:
                self.root = target.right
                self.root.prev = None
            elif parent.left == target:
                parent.left = target.right
                target.right.prev = parent
            else:
                parent.right = target.right
                target.right.prev = parent

        # Case 4: Target has only a left child
        elif target.right is None:
            if parent is None:
                self.root = target.left
                self.root.prev = None
            elif parent.left == target:
                parent.left = target.left
                target.left.prev = parent
            else:
                parent.right = target.left
                target.left.prev = parent

    def __str__(self):
        r"""String representation: a hierarchical view of the BST.

        Example:  (3)
                  / \     '[3]          The nodes of the BST are printed
                (2) (5)    [2, 5]       by depth levels. Edges and empty
                /   / \    [1, 4, 6]'   nodes are not printed.
              (1) (4) (6)
        """
        if self.root is None:                       # Empty tree
            return "[]"
        out, current_level = [], [self.root]        # Nonempty tree
        while current_level:
            next_level, values = [], []
            for node in current_level:
                values.append(node.value)
                for child in [node.left, node.right]:
                    if child is not None:
                        next_level.append(child)
            out.append(values)
            current_level = next_level
        return "\n".join([str(x) for x in out])

    def draw(self, filename):
        """Use NetworkX and Matplotlib to visualize the tree."""
        if self.root is None:
            return

        # Build the directed graph.
        G = nx.DiGraph()
        G.add_node(self.root.value)
        nodes = [self.root]
        while nodes:
            current = nodes.pop(0)
            for child in [current.left, current.right]:
                if child is not None:
                    G.add_edge(current.value, child.value)
                    nodes.append(child)

        # Plot the graph. This requires graphviz_layout (pygraphviz).
        nx.draw(G, pos=graphviz_layout(G, prog="dot"), arrows=True,
                with_labels=True, node_color="C1", font_size=8)
        plt.savefig(filename)


class AVL(BST):
    """Adelson-Velsky Landis binary search tree data structure class.
    Rebalances after insertion when needed.
    """
    def insert(self, data):
        """Insert a node containing the data into the tree, then rebalance."""
        BST.insert(self, data)      # Insert the data like usual.
        n = self.find(data)
        while n:                    # Rebalance from the bottom up.
            n = self._rebalance(n).prev

    def remove(*args, **kwargs):
        """Disable remove() to keep the tree in balance."""
        raise NotImplementedError("remove() is disabled for this class")

    def _rebalance(self, n):
        """Rebalance the subtree starting at the specified node."""
        balance = AVL._balance_factor(n)
        if balance == -2:                                   # Left heavy
            if AVL._height(n.left.left) > AVL._height(n.left.right):
                n = self._rotate_left_left(n)                   # Left Left
            else:
                n = self._rotate_left_right(n)                  # Left Right
        elif balance == 2:                                  # Right heavy
            if AVL._height(n.right.right) > AVL._height(n.right.left):
                n = self._rotate_right_right(n)                 # Right Right
            else:
                n = self._rotate_right_left(n)                  # Right Left
        return n

    @staticmethod
    def _height(current):
        r"""Calculate the height of a given node by descending recursively until
        there are no further child nodes. Return the number of children in the
        longest chain down.
                                    node | height
        Example:  (c)                  a | 0
                  / \                  b | 1
                (b) (f)                c | 3
                /   / \                d | 1
              (a) (d) (g)              e | 0
                    \                  f | 2
                    (e)                g | 0
        """
        if current is None:     # Base case: the end of a branch.
            return -1           # Otherwise, descend down both branches.
        return 1 + max(AVL._height(current.right), AVL._height(current.left))

    @staticmethod
    def _balance_factor(n):
        return AVL._height(n.right) - AVL._height(n.left)

    def _rotate_left_left(self, n):
        temp = n.left
        n.left = temp.right
        if temp.right:
            temp.right.prev = n
        temp.right = n
        temp.prev = n.prev
        n.prev = temp
        if temp.prev:
            if temp.prev.value > temp.value:
                temp.prev.left = temp
            else:
                temp.prev.right = temp
        if n is self.root:
            self.root = temp
        return temp

    def _rotate_right_right(self, n):
        temp = n.right
        n.right = temp.left
        if temp.left:
            temp.left.prev = n
        temp.left = n
        temp.prev = n.prev
        n.prev = temp
        if temp.prev:
            if temp.prev.value > temp.value:
                temp.prev.left = temp
            else:
                temp.prev.right = temp
        if n is self.root:
            self.root = temp
        return temp

    def _rotate_left_right(self, n):
        temp1 = n.left
        temp2 = temp1.right
        temp1.right = temp2.left
        if temp2.left:
            temp2.left.prev = temp1
        temp2.prev = n
        temp2.left = temp1
        temp1.prev = temp2
        n.left = temp2
        return self._rotate_left_left(n)

    def _rotate_right_left(self, n):
        temp1 = n.right
        temp2 = temp1.left
        temp1.left = temp2.right
        if temp2.right:
            temp2.right.prev = temp1
        temp2.prev = n
        temp2.right = temp1
        temp1.prev = temp2
        n.right = temp2
        return self._rotate_right_right(n)


# Problem 5
def prob5():
    """Compare the build and search times of the DoublyLinkedList, BST, and
    AVL classes. For search times, use DoublyLinkedList.iterative_find(),
    BST.find(), and AVL.find() to search for 5 random elements in each
    structure. Plot the number of elements in the structure versus the build
    and search times. Use log scales where appropriate.
    """
    # initialize all the lists neccesary
    # took me about 45 seconds on an 11th gen i7 cpu to run
    sizes = [n for n in range(100, 4001, 100)]

    dll_build = []
    bst_build = []
    avl_build = []

    dll_search = []
    bst_search = []
    avl_search = []

    for size in sizes:
        # take a random sample so that the tree doesn't just become a linked
        # list and avl trees can rebalance
        nodes = random.sample(range(10*size), size)

        dll = DoublyLinkedList()

        # Time each build method
        start = time()
        for node in nodes:
            dll.insert(0, node)
        dll_build.append(time() - start)

        bst = BST()

        start = time()
        for node in nodes:
            bst.insert(node)
        bst_build.append(time() - start)

        avl = AVL()

        start = time()
        for node in nodes:
            avl.insert(node)
        avl_build.append(time() - start)

        # set up 5 items to search for in the data structures
        search_items = random.sample(nodes, 5)

        start = time()
        for item in search_items:
            dll.iterative_find(item)
        dll_search.append(time() - start)

        start = time()
        for item in search_items:
            bst.find(item)
        bst_search.append(time() - start)

        start = time()
        for item in search_items:
            avl.find(item)
        avl_search.append(time() - start)

    # set up axis for plotting and then plot the build and
    # search data respecively in slots 1 and 2
    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)

    ax1.plot(sizes, dll_build, label="DLL Build")
    ax1.plot(sizes, bst_build, label="BST Build")
    ax1.plot(sizes, avl_build, label="AVL Build")

    ax1.set_xscale("log")
    ax1.set_yscale("log")

    ax1.set_xlabel("Number of Elements (n)")
    ax1.set_ylabel("Build Time (seconds)")
    ax1.set_title("Build Time Comparison")
    ax1.legend()

    ax2.plot(sizes, dll_search, label="DLL Search")
    ax2.plot(sizes, bst_search, label="BST Search")
    ax2.plot(sizes, avl_search, label="AVL Search")

    ax2.set_xscale("log")
    ax2.set_yscale("log")

    ax2.set_xlabel("Number of Elements (n)")
    ax2.set_ylabel("Search Time (seconds)")
    ax2.set_title("Search Time Comparison")
    ax2.legend()
    plt.tight_layout()
    plt.savefig('Time_tests.png')


if __name__ == "__main__":
    prob5()
