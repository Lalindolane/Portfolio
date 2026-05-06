# image_segmentation.py

import numpy as np
from scipy import sparse
from imageio.v3 import imread
from scipy import linalg as la
from scipy.sparse import linalg as spla
from matplotlib import pyplot as plt


# Problem 1
def laplacian(A):
    """Compute the Laplacian matrix of the graph G that has adjacency matrix A.

    Parameters:
        A ((N,N) ndarray): The adjacency matrix of an undirected graph G.

    Returns:
        L ((N,N) ndarray): The Laplacian matrix of G.
    """
    degrees = np.sum(A, axis=1)
    D = np.diag(degrees)
    L = D - A
    return L


# Problem 2
def connectivity(A, tol=1e-8):
    """Compute the number of connected components in the graph G and its
    algebraic connectivity, given the adjacency matrix A of G.

    Parameters:
        A ((N,N) ndarray): The adjacency matrix of an undirected graph G.
        tol (float): Eigenvalues that are less than this tolerance are
            considered zero.

    Returns:
        (int): The number of connected components in G.
        (float): the algebraic connectivity of G.
    """
    L = laplacian(A)
    eigs = la.eigvals(L)
    eigs = np.real(eigs)
    eigs = np.sort(eigs)
    num_components = np.sum(np.abs(eigs) < tol)
    nonzero_eigs = eigs[np.abs(eigs) >= tol]
    if len(nonzero_eigs) == 0:
        algebraic_connectivity = 0.0
    else:
        algebraic_connectivity = eigs[1]
    return int(num_components), algebraic_connectivity


# Helper function for problem 4.
def get_neighbors(index, radius, height, width):
    """Calculate the flattened indices of the pixels that are within the given
    distance of a central pixel, and their distances from the central pixel.

    Parameters:
        index (int): The index of a central pixel in a flattened image array
            with original shape (radius, height).
        radius (float): Radius of the neighborhood around the central pixel.
        height (int): The height of the original image in pixels.
        width (int): The width of the original image in pixels.

    Returns:
        (1-D ndarray): the indices of the pixels that are within the specified
            radius of the central pixel, with respect to the flattened image.
        (1-D ndarray): the euclidean distances from the neighborhood pixels to
            the central pixel.
    """
    # Calculate the original 2-D coordinates of the central pixel.
    row, col = index // width, index % width

    # Get a grid of possible candidates that are close to the central pixel.
    r = int(radius)
    x = np.arange(max(col - r, 0), min(col + r + 1, width))
    y = np.arange(max(row - r, 0), min(row + r + 1, height))
    X, Y = np.meshgrid(x, y)

    # Determine which candidates are within the given radius of the pixel.
    R = np.sqrt(((X - col)**2 + (Y - row)**2))
    mask = R < radius
    return (X[mask] + Y[mask]*width).astype(int), R[mask]


# Problems 3-6
class ImageSegmenter:
    """Class for storing and segmenting images."""

    # Problem 3
    def __init__(self, filename):
        """Read the image file. Store its brightness values as a flat array."""
        image = imread(filename).astype(float) / 255
        self.image = image
        if len(image.shape) == 3:
            brightness = np.mean(image, axis=2)
        else:
            brightness = image
        self.brightness = brightness
        self.flat_brightness = brightness.flatten()

    # Problem 3
    def show_original(self):
        """Display the original image."""
        if len(self.image.shape) == 2:
            plt.imshow(self.image, cmap="gray")
        else:
            plt.imshow(self.image)
        plt.axis("off")
        plt.title("Original Image")
        plt.savefig("Original.png")

    # Problem 4
    def adjacency(self, r=5., sigma_B2=.02, sigma_X2=3):
        """Compute the Adjacency and Degree matrices for the image graph."""

        n = self.flat_brightness.size
        height, width = self.brightness.shape
        A = sparse.lil_matrix((n, n))
        D = np.zeros(n)

        for i in range(n):
            neighbors, distances = get_neighbors(i, r, height, width)

            b_i = self.flat_brightness[i]
            b_neighbors = self.flat_brightness[neighbors]

            weights = np.exp(
                - (np.abs(b_i - b_neighbors) / sigma_B2)
                - (distances / sigma_X2)
            )

            for j, w in zip(neighbors, weights):
                A[i, j] = w
                A[j, i] = w

            D[i] = np.sum(weights)

        A = A.tocsc()

        return A, D

    # Problem 5
    def cut(self, A, D):
        """Compute the boolean mask that segments the image."""
        L = sparse.csgraph.laplacian(A)
        D_safe = np.where(D > 0, D, 1)
        D_inv_sqrt = sparse.diags(1 / np.sqrt(D_safe))
        M = D_inv_sqrt @ L @ D_inv_sqrt

        eigvals, eigvecs = spla.eigsh(M, k=2, which='SM')

        idx = np.argsort(eigvals)
        f = eigvecs[:, idx[1]]
        f_img = f.reshape(self.brightness.shape)

        mask = f_img > 0
        return mask

    # Problem 6
    def segment(self, r=6., sigma_B=.02, sigma_X=3.):
        """Display the original image and its segments."""
        A, D = self.adjacency(r, sigma_B, sigma_X)
        mask = self.cut(A, D)

        seg_pos = self.image.copy()
        seg_neg = self.image.copy()

        seg_pos[~mask] = 0
        seg_neg[mask] = 0

        plt.subplot(1, 3, 1)
        if len(self.image.shape) == 2:
            plt.imshow(self.image, cmap="gray")
        else:
            plt.imshow(self.image)
        plt.title("Original")
        plt.axis("off")
        plt.subplot(1, 3, 2)

        if len(self.image.shape) == 2:
            plt.imshow(seg_pos, cmap="gray")
        else:
            plt.imshow(seg_pos)
        plt.title("Segment 1")
        plt.axis("off")
        plt.subplot(1, 3, 3)

        if len(self.image.shape) == 2:
            plt.imshow(seg_neg, cmap="gray")
        else:
            plt.imshow(seg_neg)
        plt.title("Segment 2")
        plt.axis("off")
        plt.savefig("segments.png")


if __name__ == '__main__':
    ImageSegmenter("dream.png").segment()
'''if __name__ == "__main__":
    # test
    D1 = np.diag([3, 3, 2, 3, 3, 2])
    D2 = np.diag([3, 3, 1, 3.5, 3, 1.5])
    A1 = np.array([
    [0, 1, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1],
    [1, 1, 0, 1, 0, 0],
    [1, 0, 0, 1, 0, 0]])
    A2 = np.array([
    [0, 3, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 2, 0.5],
    [0, 0, 0, 2, 0, 1],
    [0, 0, 0, 0.5, 1, 0]])
    L1 = laplacian(A1)
    L2 = laplacian(A2)
    if np.allclose(L1, np.diag(np.sum(A1, axis=1)) - A1):
        print("L1 passed")
    if np.allclose(L2, np.diag(np.sum(A2, axis=1)) - A2):
        print("L2 passed")'''
