"""Volume 1: The SVD and Image Compression."""

import numpy as np
from imageio.v3 import imread
from scipy import linalg as la
from matplotlib import pyplot as plt

# Problem 1
def compact_svd(A, tol=1e-6):
    """Compute the truncated SVD of A.

    Parameters:
        A ((m,n) ndarray): The matrix (of rank r) to factor.
        tol (float): The tolerance for excluding singular values.

    Returns:
        ((m,r) ndarray): The orthonormal matrix U in the SVD.
        ((r,) ndarray): The singular values of A as a 1-D array.
        ((r,n) ndarray): The orthonormal matrix V^H in the SVD.
    """
    vals, V = la.eigh(A.conj().T @ A)
    idx = np.argsort(vals)[::-1]
    evals_sorted = vals[idx]
    V_sorted = V[:, idx]
    s = np.sqrt(np.maximum(evals_sorted, 0))
    mask = s > tol
    s = s[mask]
    V = V_sorted[:, mask]
    U = A @ V / s

    return U, s, V.T.conj()


# Problem 2
def visualize_svd(A):
    """Plot the effect of the SVD of A as a sequence of linear transformations
    on the unit circle and the two standard basis vectors.
    """
    theta = np.linspace(0, 2*np.pi, 200)
    S = np.vstack((np.cos(theta), np.sin(theta)))
    E = np.array([[1, 0, 0], [0, 0, 1]])
    U, s, VT = la.svd(A)
    Sigma = np.zeros(A.shape)
    np.fill_diagonal(Sigma, s)
    plt.subplot(2, 2, 1)
    plt.plot(E[0, :], E[1, :])
    plt.plot(S[0], S[1])
    plt.title("Original S and E")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")

    plt.subplot(2, 2, 2)
    plt.plot((VT @ E)[0], (VT @ E)[1])
    plt.plot((VT @ S)[0], (VT @ S)[1])
    plt.title("VT applied")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")

    plt.subplot(2, 2, 3)
    plt.plot((Sigma @ VT @ E)[0, :], (Sigma @ VT @ E)[1, :])
    plt.plot((Sigma @ VT @ S)[0, :], (Sigma @ VT @ S)[1, :])
    plt.title("then Sigma")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")

    plt.subplot(2, 2, 4)
    plt.plot((U @ Sigma @ VT @ E)[0, :], (U @ Sigma @ VT @ E)[1, :])
    plt.plot((U @ Sigma @ VT @ S)[0, :], (U @ Sigma @ VT @ S)[1, :])
    plt.title("then U")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")

    plt.tight_layout()
    plt.savefig('transform_steps.png')


# Problem 3
def svd_approx(A, s):
    """Return the best rank s approximation to A with respect to the 2-norm
    and the Frobenius norm, along with the number of bytes needed to store
    the approximation via the truncated SVD.

    Parameters:
        A ((m,n), ndarray)
        s (int): The rank of the desired approximation.

    Returns:
        ((m,n), ndarray) The best rank s approximation of A.
        (int) The number of entries needed to store the truncated SVD.
    """
    m, n = A.shape
    U, S, VT = compact_svd(A)

    if s > len(S):
        raise ValueError("s is larger than rank(A)")
    U_s = U[:, :s]
    S_s = S[:s]
    VT_s = VT[:s, :]
    entries = U_s.size + S_s.size + VT_s.size
    return U_s @ np.diag(S_s) @ VT_s, entries


# Problem 4
def lowest_rank_approx(A, err):
    """Return the lowest rank approximation of A with error less than 'err'
    with respect to the matrix 2-norm, along with the number of bytes needed
    to store the approximation via the truncated SVD.

    Parameters:
        A ((m, n) ndarray)
        err (float): Desired maximum error.

    Returns:
        A_s ((m,n) ndarray) The lowest rank approximation of A satisfying
            ||A - A_s||_2 < err.
        (int) The number of entries needed to store the truncated SVD.
    """
    U, s, VT = compact_svd(A)
    target_index = None
    for i in range(len(s)):
        if s[i] < err:
            target_index = i
            break
    if target_index is None:
        raise ValueError("A cannot be approximated within this tolerance")
    approx, entries = svd_approx(A, target_index)
    return approx, entries


# Problem 5
def compress_image(filename, s):
    """Plot the original image found at 'filename' and the rank s approximation
    of the image found at 'filename.' State in the figure title the difference
    in the number of entries used to store the original image and the
    approximation.

    Parameters:
        filename (str): Image file path.
        s (int): Rank of new image.
    """
    image = imread(filename) / 255.0

    if image.ndim == 2:
        approx, entries = svd_approx(image, s)
        approx = np.clip(approx, 0, 1)
    else:
        R = image[:, :, 0]
        G = image[:, :, 1]
        B = image[:, :, 2]
        R_s, r_entries = svd_approx(R, s)
        G_s, g_entries = svd_approx(G, s)
        B_s, b_entries = svd_approx(B, s)
        approx = np.dstack((R_s, G_s, B_s))
        approx = np.clip(approx, 0, 1)
        entries = r_entries + g_entries + b_entries

    plt.subplot(1, 2, 1)
    if image.ndim == 2:
        plt.imshow(image, cmap="gray")
    else:
        plt.imshow(image)
    plt.axis("off")
    plt.title("Original")

    plt.subplot(1, 2, 2)
    if image.ndim == 2:
        plt.imshow(approx, cmap="gray")
    else:
        plt.imshow(approx)
    plt.axis("off")
    plt.title(f"Rank {s} approximation")
    plt.suptitle(f"original entries: {image.size} compressed entries: {entries}")
    plt.tight_layout()
    plt.savefig("imagecomparison.png")

if __name__ == "__main__":
    A = np.array([[3, 1], [0, 2]])
    A1, entries1 = svd_approx(A, 1)
    print("Rank-1 approximation:")
    print(A1)
    print("Entries stored:", entries1)

    A2, entries2 = svd_approx(A, 2)
    print("Rank-2 approximation (should equal A):")
    print(A2)
    print("Entries stored:", entries2)
    print(np.allclose(A2, A))

    print("Error ||A - A1||_2:", np.linalg.norm(A - A1, 2))
    print("Error ||A - A2||_2:", np.linalg.norm(A - A2, 2))

    compress_image("hubble.jpg", 50)