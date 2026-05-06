# linear_transformations.py
import time
import numpy as np
from random import random
from matplotlib import pyplot as plt


# Problem 1
def stretch(A, a, b):
    """Scale the points in A by a in the x direction and b in the
    y direction.

    Parameters:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        a (float): scaling factor in the x direction.
        b (float): scaling factor in the y direction.
    Return:
        ((2,n) ndarray): Transformed matrix
    """
    return np.array([[a, 0], [0, b]]) @ A


def shear(A, a, b):
    """Slant the points in A by a in the x direction and b in the
    y direction.

    Parameters:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        a (float): scaling factor in the x direction.
        b (float): scaling factor in the y direction.
    Return:
        ((2,n) ndarray): Transformed matrix
    """
    return np.array([[1, a], [b, 1]]) @ A


def reflect(A, a, b):
    """Reflect the points in A about the line that passes through the origin
    and the point (a,b).

    Parameters:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        a (float): x-coordinate of a point on the reflecting line.
        b (float): y-coordinate of the same point on the reflecting line.
    Return:
        ((2,n) ndarray): Transformed matrix
    """
    return np.array([[a**2-b**2, 2*a*b], [2*a*b, b**2-a**2]]) @ A/(a**2 + b**2)


def rotate(A, theta):
    """Rotate the points in A about the origin by theta radians.

    Parameters:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        theta (float): The rotation angle in radians.
    Return:
        ((2,n) ndarray): Transformed matrix
    """
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]) @ A


def horse_test():
    # sets up a test like that of the lab instructions to verify a similar output
    points = np.load('horse.npy')
    fig = plt.figure()
    ax = fig.add_subplot(2, 3, 1)
    ax.plot(points[0], points[1], 'k.')
    ax.set_title('default')
    new = stretch(points, .5, 1.2)
    ax = fig.add_subplot(2, 3, 2)
    ax.plot(new[0], new[1], 'k.')
    ax.set_title('stretch')
    new = shear(points, .5, 0)
    ax = fig.add_subplot(2, 3, 3)
    ax.plot(new[0], new[1], 'k.')
    ax.set_title('shear')
    new = reflect(points, 0, 1)
    ax = fig.add_subplot(2, 3, 4)
    ax.set_title('reflect')
    ax.plot(new[0], new[1], 'k.')
    new = rotate(points, np.pi/2)
    ax = fig.add_subplot(2, 3, 5)
    ax.set_title('rotate')
    ax.plot(new[0], new[1], 'k.')
    plt.suptitle('horsies')
    plt.tight_layout()
    plt.savefig('test')


# Problem 2
def solar_system(T, x_e, x_m, omega_e, omega_m):
    """Plot the trajectories of the earth and moon over the time interval [0,T]
    assuming the initial position of the earth is (x_e,0) and the initial
    position of the moon is (x_m,0).

    Parameters:
        T (float): The final time.
        x_e (float): The earth's initial x coordinate.
        x_m (float): The moon's initial x coordinate.
        omega_e (float): The earth's angular velocity.
        omega_m (float): The moon's angular velocity.
    """
    # sets a set of x's and earth / moon positions to graph them
    xs = [t for t in np.linspace(0, T, 100)]
    earth_x, earth_y = [], []
    moon_x, moon_y = [], []

    # applies rotation and appends the positions to respective lists
    for x in xs:
        e = rotate(np.array([[x_e], [0]]), x * omega_e)
        ex, ey = e[0, 0], e[1, 0]
        earth_x.append(ex)
        earth_y.append(ey)

        m = rotate(np.array([[x_m-x_e], [0]]), x * omega_m)
        mx = m[0, 0] + ex
        my = m[1, 0] + ey
        moon_x.append(mx)
        moon_y.append(my)

    # Plot the figures
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.plot(earth_x, earth_y, label="earth's path")
    ax.plot(moon_x, moon_y, label="moon's path")
    ax.legend()
    ax.set_ylabel('y')
    ax.set_xlabel('x')
    ax.set_title("Moon and Earth trajectories overlaid")
    plt.savefig('trajectories')
    plt.clf()


def random_vector(n):
    """Generate a random vector of length n as a list."""
    return [random() for i in range(n)]


def random_matrix(n):
    """Generate a random nxn matrix as a list of lists."""
    return [[random() for j in range(n)] for i in range(n)]


def matrix_vector_product(A, x):
    """Compute the matrix-vector product Ax as a list."""
    m, n = len(A), len(x)
    return [sum([A[i][k] * x[k] for k in range(n)]) for i in range(m)]


def matrix_matrix_product(A, B):
    """Compute the matrix-matrix product AB as a list of lists."""
    m, n, p = len(A), len(B), len(B[0])
    return [[sum([A[i][k] * B[k][j] for k in range(n)])
                                    for j in range(p)]
                                    for i in range(m)]


# Problem 3
def prob3():
    """Use time.time(), timeit.timeit(), or %timeit to time
    matrix_vector_product() and matrix-matrix-mult() with increasingly large
    inputs. Generate the inputs A, x, and B with random_matrix() and
    random_vector() (so each input will be nxn or nx1).
    Only time the multiplication functions, not the generating functions.

    Report your findings in a single figure with two subplots: one with matrix-
    vector times, and one with matrix-matrix times. Choose a domain for n so
    that your figure accurately describes the growth, but avoid values of n
    that lead to execution times of more than 1 minute.
    """
    mat_vec_times = []
    mat_mat_times = []
    ns = [n for n in range(1, 301, 20)]
    for n in ns:
        A = random_matrix(n)
        B = random_matrix(n)
        x = random_vector(n)
        start = time.time()
        matrix_vector_product(A, x)
        mat_vec_times.append(time.time() - start)
        start = time.time()
        matrix_matrix_product(A, B)
        mat_mat_times.append(time.time() - start)
    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1)
    ax.plot(ns, mat_vec_times)
    ax.set_xlabel('n')
    ax.set_ylabel('time (seconds)')
    ax.set_title('Matrix-Vector Multiplication')
    ax = fig.add_subplot(1, 2, 2)
    ax.plot(ns, mat_mat_times)
    ax.set_title('Matrix-Matrix Multiplication')
    ax.set_xlabel('n')
    ax.set_ylabel('time (seconds)')
    plt.tight_layout()
    plt.savefig('matrix_multiplication')
    plt.clf()


# Problem 4
def prob4():
    """Time matrix_vector_product(), matrix_matrix_product(), and np.dot().

    Report your findings in a single figure with two subplots: one with all
    four sets of execution times on a regular linear scale, and one with all
    four sets of exections times on a log-log scale.
    """
    mat_vec_times = []
    mat_mat_times = []
    numpy_mat_mat_times = []
    numpy_mat_vec_times = []
    ns = [n for n in range(1, 301, 10)]
    for n in ns:
        A = random_matrix(n)
        B = random_matrix(n)
        x = random_vector(n)
        start = time.time()
        matrix_vector_product(A, x)
        mat_vec_times.append(time.time() - start)
        start = time.time()
        matrix_matrix_product(A, B)
        mat_mat_times.append(time.time() - start)
        Anp = np.random.random((n, n))
        Bnp = np.random.random((n, n))
        xnp = np.random.random(n)
        start = time.time()
        cnp = Anp @ Bnp
        numpy_mat_mat_times.append(time.time() - start)
        start = time.time()
        dnp = Anp @ xnp
        numpy_mat_vec_times.append(time.time() - start)
    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1)
    ax.plot(ns, mat_vec_times, label="matrix-vector")
    ax.plot(ns, mat_mat_times, label="matrix-matrix")
    ax.plot(ns, numpy_mat_mat_times, label='matrix-matrix-np')
    ax.plot(ns, numpy_mat_vec_times, label="matrix-vector-np")
    ax.set_xlabel('n')
    ax.set_ylabel('time (seconds)')
    ax.set_title('Comparison on log scale')
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.legend()
    ax = fig.add_subplot(1, 2, 2)
    ax.plot(ns, mat_vec_times, label="matrix-vector")
    ax.plot(ns, mat_mat_times, label="matrix-matrix")
    ax.plot(ns, numpy_mat_mat_times, label='matrix-matrix-np')
    ax.plot(ns, numpy_mat_vec_times, label="matrix-vector-np")
    ax.set_xlabel('n')
    ax.set_ylabel('time (seconds)')
    ax.set_title('Comparison on linear scale')
    plt.legend()
    plt.tight_layout()
    plt.savefig('matrix_multiplication_with_numpy')
    plt.clf()


if __name__ == "__main__":
    prob3()
    horse_test()
    solar_system(3*np.pi/2, 10, 11, 1, 13)
