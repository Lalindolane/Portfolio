# lstsq_eigs.py

import numpy as np
from cmath import sqrt
from scipy import linalg as la
from matplotlib import pyplot as plt


# Problem 1
def least_squares(A, b):
    """Calculate the least squares solutions to Ax = b by using the QR
    decomposition.

    Parameters:
        A ((m,n) ndarray): A matrix of rank n <= m.
        b ((m, ) ndarray): A vector of length m.

    Returns:
        x ((n, ) ndarray): The solution to the normal equations.
    """
    Q, R = la.qr(A, mode="economic")
    x = la.solve_triangular(R, Q.T @ b)
    return x

# Problem 2
def line_fit(dataset="housing.npy"):
    """Find the least squares line that relates the year to the housing price
    index for the data in housing.npy. Plot both the data points and the least
    squares line.
    """
    data = np.load(dataset)
    years = data[:, 0]
    index = data[:, 1]
    A = np.column_stack((np.ones(len(years)), years))
    b = index
    x = least_squares(A, b)
    x1, x2 = x
    y_fit = x1 + x2 * years
    plt.scatter(years, index)
    plt.plot(years, y_fit)
    plt.xlabel("Year")
    plt.ylabel('Housing Price Index')
    plt.savefig("Housingmodel")


# Problem 3
def polynomial_fit(dataset="housing.npy"):
    """Find the least squares polynomials of degree 3, 6, 9, and 12 that relate
    the year to the housing price index for the data in housing.npy. Plot both
    the data points and the least squares polynomials in individual subplots.
    """
    data = np.load(dataset)

    years = data[:, 0]
    index = data[:, 1]

    def fit_polynomial(x, y, degree):
        A = np.column_stack([x**i for i in range(degree+1)])
        return la.lstsq(A, y)[0]

    def evaluate_polynomial(coeffs, x):
        y = np.zeros_like(x, dtype=float)
        for i, c in enumerate(coeffs):
            y += c*x**i
        return y

    x_smooth = np.linspace(years.min(), years.max(), 200)

    degrees = [3, 6, 9, 12]

    for i, d in enumerate(degrees):

        coeffs = fit_polynomial(years, index, d)
        y_fit = evaluate_polynomial(coeffs, x_smooth)

        plt.subplot(2, 2, i+1)
        plt.scatter(years, index)
        plt.plot(x_smooth, y_fit)
        plt.title(f"Degree {d}")
    plt.suptitle("polynomial comparisons")
    plt.tight_layout()
    plt.savefig("polyfit")


def plot_ellipse(a, b, c, d, e):
    """Plot an ellipse of the form ax^2 + bx + cxy + dy + ey^2 = 1."""
    theta = np.linspace(0, 2*np.pi, 200)
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    A = a*(cos_t**2) + c*cos_t*sin_t + e*(sin_t**2)
    B = b*cos_t + d*sin_t
    r = (-B + np.sqrt(B**2 + 4*A)) / (2*A)

    plt.plot(r*cos_t, r*sin_t)
    plt.gca().set_aspect("equal", "datalim")

# Problem 4
def ellipse_fit(dataset="ellipse.npy"):
    """Calculate the parameters for the ellipse that best fits the data in
    ellipse.npy. Plot the original data points and the ellipse together, using
    plot_ellipse() to plot the ellipse.
    """
    data = np.load(dataset)
    x = data[:, 0]
    y = data[:, 1]

    A = np.column_stack((x**2, x, x*y, y, y**2))
    b = np.ones(len(x))

    coeffs = la.lstsq(A, b)[0]
    a, b_, c, d, e = coeffs
    plt.scatter(x, y, label="Data")
    plot_ellipse(a, b_, c, d, e)
    plt.legend()
    plt.title("Ellipse Fit")
    plt.savefig("Ellipsefit.png")

# Problem 5
def power_method(A, N=20, tol=1e-12):
    """Compute the dominant eigenvalue of A and a corresponding eigenvector
    via the power method.

    Parameters:
        A ((n,n) ndarray): A square matrix.
        N (int): The maximum number of iterations.
        tol (float): The stopping tolerance.

    Returns:
        (float): The dominant eigenvalue of A.
        ((n,) ndarray): An eigenvector corresponding to the dominant
            eigenvalue of A.
    """
    n = A.shape[0]
    x = np.random.random(n)
    x = x / la.norm(x)
    for _ in range(N):
        x_new = A @ x
        x_new = x_new/la.norm(x_new)
        if la.norm(x_new - x) < tol:
            x = x_new
            break
        x = x_new
    eigen_value = x @ (A @ x)
    return eigen_value, x


# Problem 6
def qr_algorithm(A, N=50, tol=1e-12):
    """Compute the eigenvalues of A via the QR algorithm.

    Parameters:
        A ((n,n) ndarray): A square matrix.
        N (int): The number of iterations to run the QR algorithm.
        tol (float): The threshold value for determining if a diagonal S_i
            block is 1x1 or 2x2.

    Returns:
        ((n,) ndarray): The eigenvalues of A.
    """
    S = la.hessenberg(A.copy())
    for _ in range(N):
        Q, R = la.qr(S)
        S = R @ Q

    n = S.shape[0]
    eigs = []
    i = 0

    while i < n:
        if i == n - 1 or abs(S[i+1, i]) < tol:
            eigs.append(S[i, i])
            i += 1
        else:
            a = S[i, i]
            b = S[i, i+1]
            c = S[i+1, i]
            d = S[i+1, i+1]

            trace = a + d
            det = a * d - b * c

            disc = sqrt(trace**2 - 4*det)

            eigs.append((trace + disc) / 2)
            eigs.append((trace - disc) / 2)

            i += 2

    return np.array(eigs)


if __name__ == '__main__':
    ellipse_fit()
    plt.clf()
    polynomial_fit()
