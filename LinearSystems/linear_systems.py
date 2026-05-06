# linear_systems.py

import numpy as np
from time import perf_counter as time
from scipy import sparse
from scipy import linalg as la
from scipy.sparse import linalg as spla
from matplotlib import pyplot as plt


# Problem 1
def ref(A):
    """Reduce the square matrix A to REF. You may assume that A is invertible
    and that a 0 will never appear on the main diagonal. Avoid operating on
    entries that you know will be 0 before and after a row operation.

    Parameters:
        A ((n,n) ndarray): The square invertible matrix to be reduced.

    Returns:
        ((n,n) ndarray): The REF of A.
    """
    A = A.astype(float)
    for j in range(len(A)):
        for i in range(j+1, len(A)):
            multiplier = A[i, j] / A[j, j]
            A[i, j:] = A[i, j:] - multiplier * A[j, j:]
    return A


# Problem 2
def lu(A):
    """Compute the LU decomposition of the square matrix A. You may
    assume that the decomposition exists and requires no row swaps.

    Parameters:
        A ((n,n) ndarray): The matrix to decompose.

    Returns:
        L ((n,n) ndarray): The lower-triangular part of the decomposition.
        U ((n,n) ndarray): The upper-triangular part of the decomposition.
    """
    A = A.astype(float)
    m, n = np.shape(A)
    U = np.copy(A)
    L = np.identity(m)
    for j in range(n):
        for i in range(j+1, m):
            L[i, j] = U[i, j] / U[j, j]
            U[i, j:] = U[i, j:] - L[i, j] * U[j, j:]
    return L, U


# Problem 3
def solve(A, b):
    """Use the LU decomposition and back substitution to solve the linear
    system Ax = b. You may again assume that no row swaps are required.

    Parameters:
        A ((n,n) ndarray)
        b ((n,) ndarray)

    Returns:
        x ((n,) ndarray): The solution to the linear system.
    """
    L, U = lu(A)
    n = len(A)
    y = np.zeros(n)
    x = np.zeros(n)
    y_total = 0
    x_total = 0
    for k in range(n):
        for j in range(0, k):
            y_total += L[k, j] * y[j]
        y[k] = b[k] - y_total
        y_total = 0
    for k in range(n-1, -1, -1):
        for j in range(k+1, n):
            x_total += U[k, j] * x[j]
        x[k] = (1/U[k, k]) * (y[k] - x_total)
        x_total = 0
    return x


# Problem 4
def prob4():
    """Time different scipy.linalg functions for solving square linear systems.

    For various values of n, generate a random nxn matrix A and a random
    n-vector b using np.random.random(). Time how long it takes to solve the
    system Ax = b with each of the following approaches:

        1. Invert A with la.inv() and left-multiply the inverse to b.
        2. Use la.solve().
        3. Use la.lu_factor() and la.lu_solve() to solve the system with the
            LU decomposition.
        4. Use la.lu_factor() and la.lu_solve(), but only time la.lu_solve()
            (not the time it takes to do the factorization).

    Plot the system size n versus the execution times. Use log scales if
    needed.
    """
    invert_times = []
    lasolve_times = []
    lalu_times = []
    only_lalu_times = []
    ns = np.linspace(50, 2500, 40, dtype=int)
    for n in ns:
        A = np.random.random((n, n))
        b = np.random.random(n)
        start = time()
        inv = la.inv(A)
        answer = inv @ b
        invert_times.append(time() - start)
        start = time()
        answer = la.solve(A, b)
        lasolve_times.append(time() - start)
        start = time()
        L, piv = la.lu_factor(A)
        only_lalu_times.append(time() - start)
        start = time()
        answer = la.lu_solve((L, piv), b)
        lalu_times.append(time() - start)
    plt.plot(ns, invert_times, label="Using Inversion")
    plt.plot(ns, lasolve_times, label="Using la.solve")
    plt.plot(ns, only_lalu_times, label="Computing LU decomp")
    plt.plot(ns, lalu_times, label="Using la.lu_solve()")
    plt.legend()
    plt.xlabel("Size n")
    plt.ylabel("Time (seconds)")
    plt.title("Comparing solution times")
    plt.savefig("timecomparisons.png")


# Problem 5
def prob5(n):
    """Let I be the n × n identity matrix, and define
                    [B I        ]        [-4  1            ]
                    [I B I      ]        [ 1 -4  1         ]
                A = [  I . .    ]    B = [    1  .  .      ],
                    [      . . I]        [          .  .  1]
                    [        I B]        [             1 -4]
    where A is (n**2,n**2) and each block B is (n,n).
    Construct and returns A as a sparse matrix.

    Parameters:
        n (int): Dimensions of the sparse matrix B.

    Returns:
        A ((n**2,n**2) SciPy sparse matrix)
    """
    N = n**2
    main = [-4] * N
    off1 = [1] * (N-1)
    offn = [1] * (N-n)
    for k in range(1, n):
        off1[k * n - 1] = 0
    diagonals = [offn, off1, main, off1, offn]
    offsets = [-n, -1, 0, 1, n]
    A = sparse.diags(diagonals, offsets, shape=(N, N))
    return A


# Problem 6
def prob6():
    """Time regular and sparse linear system solvers.

    For various values of n, generate the (n**2,n**2) matrix A described of
    prob5() and vector b of length n**2. Time how long it takes to solve the
    system Ax = b with each of the following approaches:

        1. Convert A to CSR format and use scipy.sparse.linalg.spsolve()
        2. Convert A to a NumPy array and use scipy.linalg.solve().

    In each experiment, only time how long it takes to solve the system (not
    how long it takes to convert A to the appropriate format). Plot the system
    size n**2 versus the execution times. As always, use log scales where
    appropriate and use a legend to label each line.
    """
    sparse_times = []
    dense_times = []
    ns = np.arange(5, 80, 5)

    for n in ns:
        A = prob5(n)
        b = np.random.random(n**2)

        A_csr = A.tocsr()
        A_dense = A.toarray()

        start = time()
        x = spla.spsolve(A_csr, b)
        sparse_times.append(time()-start)

        start = time()
        x = la.solve(A_dense, b)
        dense_times.append(time() - start)
    system_sizes = ns**2
    plt.figure()
    plt.loglog(system_sizes, sparse_times, 'o-', label='Sparse Solve (spsolve)')
    plt.loglog(system_sizes, dense_times, 'o-', label='Dense Solve (la.solve)')

    plt.xlabel('System size (n^2)')
    plt.ylabel('Time (seconds)')
    plt.title('Sparse vs Dense Linear System Solvers')
    plt.legend()
    plt.savefig('prob6.png')

if __name__ == "__main__":
    plt.spy(prob5(5))
    plt.savefig('Test')
    plt.clf()
    prob4()
    plt.clf()
    prob6()

