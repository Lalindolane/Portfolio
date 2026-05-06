# qr_decomposition.py

import numpy as np
from scipy import linalg as la


# Problem 1
def qr_gram_schmidt(A):
    """Compute the reduced QR decomposition of A via Modified Gram-Schmidt.

    Parameters:
        A ((m,n) ndarray): A matrix of rank n.

    Returns:
        Q ((m,n) ndarray): An orthonormal matrix.
        R ((n,n) ndarray): An upper triangular matrix.
    """
    m, n = A.shape
    Q = A.astype(float).copy()
    R = np.zeros((n, n))
    for i in range(n):
        R[i, i] = la.norm(Q[:, i])
        Q[:, i] = Q[:, i]/R[i, i]
        for j in range(i+1, n):
            R[i, j] = Q[:, i] @ Q[:, j]
            Q[:, j] = Q[:, j] - (R[i, j] * Q[:, i])
    return Q, R


# Problem 2
def abs_det(A):
    """Use the QR decomposition to efficiently compute the absolute value of
    the determinant of A.

    Parameters:
        A ((n,n) ndarray): A square matrix.

    Returns:
        (float) the absolute value of the determinant of A.
    """
    m, n = np.shape(A)
    Q, R = qr_gram_schmidt(A)
    my_det = 1
    for i in range(n):
        my_det *= R[i, i]
    return abs(my_det)

# Problem 3
def solve(A, b):
    """Use the QR decomposition to efficiently solve the system Ax = b.

    Parameters:
        A ((n,n) ndarray): An invertible matrix.
        b ((n, ) ndarray): A vector of length n.

    Returns:
        x ((n, ) ndarray): The solution to the system Ax = b.
    """
    m, n = A.shape
    Q, R = qr_gram_schmidt(A)
    y = Q.T @ b
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        sums = 0
        for j in range(i+1, n):
            sums += R[i, j] * x[j]
        x[i] = (y[i] - sums)/R[i, i]
    return x


# Problem 4
def qr_householder(A):
    """Compute the full QR decomposition of A via Householder reflections.

    Parameters:
        A ((m,n) ndarray): A matrix of rank n.

    Returns:
        Q ((m,m) ndarray): An orthonormal matrix.
        R ((m,n) ndarray): An upper triangular matrix.
    """
    m, n = A.shape
    R = A.astype(float).copy()
    Q = np.eye(m)

    for k in range(n):
        u = R[k:, k].copy()
        u[0] = u[0] + np.sign(u[0]) * la.norm(u)
        u /= la.norm(u)
        R[k:, k:] -= 2 * np.outer(u, (u.T @ R[k:, k:]))
        Q[k:, :] -= 2 * np.outer(u, (u.T @ Q[k:, :]))
    return Q.T, R

# Problem 5
def hessenberg(A):
    """Compute the Hessenberg form H of A, along with the orthonormal matrix Q
    such that A = QHQ^T.

    Parameters:
        A ((n,n) ndarray): An invertible matrix.

    Returns:
        H ((n,n) ndarray): The upper Hessenberg form of A.
        Q ((n,n) ndarray): An orthonormal matrix.
    """
    m, n = A.shape
    H = A.copy()
    Q = np.eye(m)
    for k in range(n-2):
        u = H[k+1:, k].copy()
        u[0] = u[0] + np.sign(u[0]) * la.norm(u)
        u = u/la.norm(u)
        H[k+1:, k:] = H[k+1:, k:] - 2 * np.outer(u, (u @ H[k+1:, k:]))
        H[:, k+1:] = H[:, k+1:] - 2 * np.outer((H[:, k+1:] @ u), u)
        Q[k+1:, :] = Q[k+1:, :] - 2 * np.outer(u, (u @ Q[k+1:, :]))

    return H, Q.T

if __name__ == "__main__":
    A = np.random.random((5, 5))
    H, Q = la.hessenberg(A, calc_q = True)
    h, q = hessenberg(A)
    print(A.shape, Q.shape, H.shape)
    print(A.shape, q.shape, h.shape)
    print(np.allclose(q @ h @ q.T, A))