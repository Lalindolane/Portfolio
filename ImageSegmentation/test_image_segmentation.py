"""Unit testing file for Image Segmentation"""

import image_segmentation
import pytest
import numpy as np
from scipy import sparse as sp

@pytest.fixture
def set_up_matrices():
    # Sets up test cases
    A = np.array([[0, 1, 0, 0, 1, 1],
                  [1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 0],
                  [0, 0, 1, 0, 1, 1],
                  [1, 1, 0, 1, 0, 0],
                  [1, 0, 0, 1, 0, 0]], dtype=float)

    B = np.array([[0, 3, 0, 0, 0, 0],
                  [3, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0],
                  [0, 0, 1, 0, 2, .5],
                  [0, 0, 0, 2, 0, 1],
                  [0, 0, 0, .5, 1, 0]], dtype=float)

    C = np.array([[0, 4, 2, 100],
                  [4, 0, 23, 54],
                  [2, 23, 0, 23],
                  [100, 54, 23, 0]], dtype=float)

    return A, B, C


def test_laplacian(set_up_matrices):
    A, B, C = set_up_matrices

    # Checks for the correct laplacian
    assert (image_segmentation.laplacian(A) == sp.csgraph.laplacian(A)).all(), "Incorrect Laplacian"
    assert (image_segmentation.laplacian(B) == sp.csgraph.laplacian(B)).all(), "Incorrect Laplacian"
    assert (image_segmentation.laplacian(C) == sp.csgraph.laplacian(C)).all(), "Incorrect Laplacian"

def test_connectivity():
    """
    Write at least one unit test for the connectivity function.
    """
    A = np.array([
        [0,1,1],
        [1,0,1],
        [1,1,0]
    ])
    components, conn = image_segmentation.connectivity(A)

    assert np.allclose(components, 1)
    assert np.allclose(conn, 3)

    A = np.array([
        [0,1,0],
        [1,0,0],
        [0,0,0]
    ])
    components, conn = image_segmentation.connectivity(A)

    assert np.allclose(components, 2)
    assert np.allclose(conn, 0)

    A = np.array([
        [0,1,0,0],
        [1,0,0,0],
        [0,0,0,1],
        [0,0,1,0]
    ])
    components, conn = image_segmentation.connectivity(A)

    assert np.allclose(components, 2)
    assert np.allclose(conn, 0)
