# nearest_neighbor.py
import numpy as np
from scipy import stats
from scipy import linalg as la
from scipy.spatial import KDTree


# Problem 1
def exhaustive_search(X, z):
    """Solve the nearest neighbor search problem with an exhaustive search.

    Parameters:
        X ((m,k) ndarray): a training set of m k-dimensional points.
        z ((k, ) ndarray): a k-dimensional target point.

    Returns:
        ((k,) ndarray) the element (row) of X that is nearest to z.
        (float) The Euclidean distance from the nearest neighbor to z.
    """
    diff = X - z
    distances = la.norm(diff, axis=1)
    i = np.argmin(distances)
    return X[i], distances[i]


# Problem 2: Write a KDTNode class.
class KDTNode:
    """Node class for K-D Trees.

    Attributes:
        left (KDTNode): a reference to this node's left child.
        right (KDTNode): a reference to this node's right child.
        value ((k,) ndarray): a coordinate in k-dimensional space.
        pivot (int): the dimension of the value to make comparisons on.
    """
    def __init__(self, x):
        if not isinstance(x, np.ndarray):
            raise TypeError

        self.value = x
        self.right = None
        self.left = None
        self.pivot = None


# Problems 3 and 4
class KDT:
    """A k-dimensional binary tree for solving the nearest neighbor problem.

    Attributes:
        root (KDTNode): the root node of the tree. Like all other nodes in
            the tree, the root has a NumPy array of shape (k,) as its value.
        k (int): the dimension of the data in the tree.
    """
    def __init__(self):
        """Initialize the root and k attributes."""
        self.root = None
        self.k = None

    def find(self, data):
        """Return the node containing the data. If there is no such node in
        the tree, or if the tree is empty, raise a ValueError.
        """
        def _step(current):
            """Recursively step through the tree until finding the node
            containing the data. If there is no such node, raise a ValueError.
            """
            if current is None:                     # Base case 1: dead end.
                raise ValueError(str(data) + " is not in the tree")
            elif np.allclose(data, current.value):
                return current                      # Base case 2: data found!
            elif data[current.pivot] < current.value[current.pivot]:
                return _step(current.left)          # Recursively search left.
            else:
                return _step(current.right)         # Recursively search right.

        # Start the recursive search at the root of the tree.
        return _step(self.root)

    # Problem 3
    def insert(self, data):
        """Insert a new node containing the specified data.

        Parameters:
            data ((k,) ndarray): a k-dimensional point to insert into the tree.

        Raises:
            ValueError: if data does not have the same dimensions as other
                values in the tree.
            ValueError: if data is already in the tree
        """
        node = KDTNode(data)
        current = self.root

        # Tree is empty
        if current is None:
            self.root = node
            node.pivot = 0
            self.k = len(data)
            return
        
        # if data doesn't match tree structure
        if len(data) != self.k:
            raise ValueError

        # iterates through the tree making the proper comparisons
        # until a child can be set
        else:
            while True:
                pivot = current.pivot
                # if data is alreay in tree
                if np.allclose(node.value, current.value):
                    raise ValueError
                
                if node.value[pivot] > current.value[pivot]:
                    if current.right is not None:
                        current = current.right
                    else:
                        current.right = node
                        node.pivot = (current.pivot + 1) % self.k
                        break
                elif node.value[pivot] <= current.value[pivot]:
                    if current.left is not None:
                        current = current.left
                    else:
                        current.left = node
                        node.pivot = (current.pivot + 1) % self.k
                        break

    # Problem 4
    def query(self, z):
        """Find the value in the tree that is nearest to z.

        Parameters:
            z ((k,) ndarray): a k-dimensional target point.

        Returns:
            ((k,) ndarray) the value in the tree that is nearest to z.
            (float) The Euclidean distance from the nearest neighbor to z.
        """
        if self.root is None:
            raise ValueError('Tree is empty')
        
        x_star = self.root
        d_star = la.norm(x_star.value - z)

        def KDSearch(current, nearest, dstar):
            if current is None:
                return nearest, dstar
            x = current.value
            i = current.pivot
            dist = la.norm(x - z)
            if dist < dstar:
                dstar = dist
                nearest = current
            if z[i] < x[i]:
                nearest, dstar = KDSearch(current.left, nearest, dstar)
                if z[i] + dstar >= x[i]:
                    nearest, dstar = KDSearch(current.right, nearest, dstar)
            else:
                nearest, dstar = KDSearch(current.right, nearest, dstar)
                if z[i] - dstar <= x[i]:
                    nearest, dstar = KDSearch(current.left, nearest, dstar)
            return nearest, dstar
        node, dstar = KDSearch(x_star, x_star, d_star)
        return node.value, dstar

    def __str__(self):
        """String representation: a hierarchical list of nodes and their axes.

        Example:                           'KDT(k=2)
                    [5,5]                   [5 5]   pivot = 0
                    /   \                   [3 2]   pivot = 1
                [3,2]   [8,4]               [8 4]   pivot = 1
                    \       \               [2 6]   pivot = 0
                    [2,6]   [7,5]           [7 5]   pivot = 0'
        """
        if self.root is None:
            return "Empty KDT"
        nodes, strs = [self.root], []
        while nodes:
            current = nodes.pop(0)
            strs.append("{}\tpivot = {}".format(current.value, current.pivot))
            for child in [current.left, current.right]:
                if child:
                    nodes.append(child)
        return "KDT(k={})\n".format(self.k) + "\n".join(strs)


# Problem 5: Write a KNeighborsClassifier class.
class KNeighborsClassifier:
    """A k-nearest neighbors classifier that uses SciPy's KDTree to solve
    the nearest neighbor problem efficiently.
    """
    def __init__(self, n_neighbors):
        self.k = n_neighbors
        self.tree = None
        self.labels = None
    
    def fit(self, X, y):
        if X.ndim != 2:
            raise ValueError('X must be 2D')
        if y.ndim != 1:
            raise ValueError('y must be 1D')
        if X.shape[0] != y.shape[0]:
            raise ValueError('X needs as many rows as length of y')
        self.tree = KDTree(X)
        self.labels = y
        return self

    def predict(self, z):
        if self.tree is None:
            raise ValueError('tree has not been fit')
        if z.ndim != 1:
            raise ValueError('input needs to be 1D')
        distances, indices = self.tree.query(z, k=self.k)
        if self.k == 1:
            return self.labels[indices]
        neighbor_labels = self.labels[indices]
        unique_labels, counts = np.unique(neighbor_labels, return_counts=True)
        most_common_index = np.argmax(counts)
        return unique_labels[most_common_index]


# Problem 6
def prob6(n_neighbors, filename="mnist_subset.npz"):
    """Extract the data from the given file. Load a KNeighborsClassifier with
    the training data and the corresponding labels. Use the classifier to
    predict labels for the test data. Return the classification accuracy, the
    percentage of predictions that match the test labels.

    Parameters:
        n_neighbors (int): the number of neighbors to use for classification.
        filename (str): the name of the data file. Should be an npz file with
            keys 'X_train', 'y_train', 'X_test', and 'y_test'.

    Returns:
        (float): the classification accuracy.
    """
    data = np.load(filename)
    X_train = data["X_train"].astype(np.float64)          # Training data
    y_train = data["y_train"]                           # Training labels
    X_test = data["X_test"].astype(np.float64)            # Test data
    y_test = data["y_test"]
    classifier = KNeighborsClassifier(n_neighbors)
    classifier.fit(X_train, y_train)
    correct = 0
    for i in range(len(X_test)):
        prediction = classifier.predict(X_test[i])
        if (prediction == y_test[i]):
            correct += 1
    return correct/len(X_test)


if __name__ == '__main__':
    '''tree = KDT()
    vectors = np.array([[3, 1, 4], [1, 2, 7], [2, 4, 5], [1, 4, 3], [4, 3, 5], [2, 0, 3], [6, 1, 4], [0, 5, 7], [5, 2, 5]])
    for vector in vectors:
        tree.insert(vector)
        print(tree)'''
    print(prob6(4))
