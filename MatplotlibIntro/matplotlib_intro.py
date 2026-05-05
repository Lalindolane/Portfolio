# matplotlib_intro.py
"""Python Essentials: Intro to Matplotlib.
<Lane Lindstrom>
<Math 321>
<01/22/2026>
"""

import numpy as np
import matplotlib.pyplot as plt


# Problem 1
def var_of_means(n):
    # Creates a normal distribution nxn matrix, returns the variance of the mean values of the rows
    """ Create an (n x n) array of values randomly sampled from the standard
    normal distribution. Compute the mean of each row of the array. Return the
    variance of these means.

    Parameters:
        n (int): The number of rows and columns in the matrix.

    Returns:
        (float) The variance of the means of each row.
    """
    array = np.random.normal(size=(n, n))
    row_avgs = np.average(array, axis=1)
    variance = np.var(row_avgs)
    return variance
    

def prob1():
    """ Create an array of the results of var_of_means() with inputs
    n = 100, 200, ..., 1000. Plot and show the resulting array.
    """
    ns = np.arange(100, 1100, 100)
    y = np.array([var_of_means(n) for n in ns])
    plt.plot(ns, y)
    plt.xlabel("n")
    plt.ylabel("y")
    plt.title("variance of means of nxn matrices")
    plt.tight_layout()
    plt.savefig("graph1.jpg")
    plt.clf()


# Problem 2
def prob2():
    # plots sin(x) cos(x) and arctan(x) on -2pi to 2pi with resolution n = 1000
    """ Plot the functions sin(x), cos(x), and arctan(x) on the domain
    [-2pi, 2pi]. Make sure the domain is refined enough to produce a figure
    with good resolution.
    """
    xs = np.arange(-2 * np.pi, 2 * np.pi, 4 * np.pi / 1000)
    y_sin = np.array(np.sin(xs))
    y_cos = np.array(np.cos(xs))
    y_arctan = np.array(np.arctan(xs))
    plt.plot(xs, y_sin, label="sin(x)")
    plt.plot(xs, y_cos, label="cos(x)")
    plt.plot(xs, y_arctan, label="arctan(x)")
    plt.title("cos, sin, and arctan")
    plt.xlabel("x")
    plt.ylabel('y')
    plt.legend()
    plt.tight_layout()
    plt.savefig("sin_cos_arctan.jpg")


# Problem 3
def prob3():
    # plots f(x) = 1/(x-1) on [-2,6]
    """ Plot the curve f(x) = 1/(x-1) on the domain [-2,6].
        1. Split the domain so that the curve looks discontinuous.
        2. Plot both curves with a thick, dashed magenta line.
        3. Set the range of the x-axis to [-2,6] and the range of the
           y-axis to [-6,6].
    """
    xs_1 = np.arange(-2, 1, 3/300)
    xs_2 = np.arange(1.001, 6, 5 / 500)
    ys_1 = np.array([1 / (x-1) for x in xs_1])
    ys_2 = np.array([1 / (x-1) for x in xs_2])
    plt.plot(xs_1, ys_1, 'm--', linewidth=4)
    plt.plot(xs_2, ys_2, 'm--', linewidth=4)
    plt.title("f(x) = 1/(x-1) on [-2,6]")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(-2, 6)
    plt.ylim(-6, 6)
    plt.savefig("weird_graph.jpg")


# Problem 4
def prob4():
    # Plot the functions sin(x), sin(2x), 2sin(x), and 2sin(2x) on the
    # domain [0, 2pi], each in a separate subplot of a single figure
    """ Plot the functions sin(x), sin(2x), 2sin(x), and 2sin(2x) on the
    domain [0, 2pi], each in a separate subplot of a single figure.
        1. Arrange the plots in a 2 x 2 grid of subplots.
        2. Set the limits of each subplot to [0, 2pi]x[-2, 2].
        3. Give each subplot an appropriate title.
        4. Give the overall figure a title.
        5. Use the following line colors and styles.
              sin(x): green solid line.
             sin(2x): red dashed line.
             2sin(x): blue dashed line.
            2sin(2x): magenta dotted line.
    """
    xs = np.arange(0, 2*np.pi, 2*np.pi/1000)
    ys_sin = np.sin(xs)
    ys_sin_2 = np.sin(2*xs)
    ys_2sin = 2*np.sin(xs)
    ys_2sin_2 = 2*np.sin(2*xs)
 
    # first subplot
    ax1 = plt.subplot(2, 2, 1)
    ax1.plot(xs, ys_sin, 'g-')
    ax1.set_title("sin(x)")
    ax1.set_xlim(0, 2*np.pi)
    ax1.set_ylim(-2, 2)
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")

    # second subplot
    ax2 = plt.subplot(2, 2, 2)
    ax2.plot(xs, ys_sin_2, 'r--')
    ax2.set_title("sin(2x)")
    ax2.set_xlim(0, 2*np.pi)
    ax2.set_ylim(-2, 2)
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")

    # third
    ax3 = plt.subplot(2, 2, 3)
    ax3.plot(xs, ys_2sin, 'b--')
    ax3.set_title("2sin(x)")
    ax3.set_xlim(0, 2*np.pi)
    ax3.set_ylim(-2, 2)
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")

    # fourth
    ax4 = plt.subplot(2, 2, 4)
    ax4.plot(xs, ys_2sin_2, 'm:')
    ax4.set_title("2sin(2x)")
    ax4.set_xlim(0, 2*np.pi)
    ax4.set_ylim(-2, 2)
    ax4.set_xlabel("x")
    ax4.set_ylabel("y")

    plt.suptitle("Four variations of sine functions")
    plt.tight_layout()
    plt.savefig("variationsofsin.jpg")


# Problem 5
def prob5():
    # creates a scatter plot and histograb based on the FARS information given
    """ Visualize the data in FARS.npy. Use np.load() to load the data, then
    create a single figure with two subplots:
        1. A scatter plot of longitudes against latitudes. Because of the
            large number of data points, use black pixel markers (use "k,"
            as the third argument to plt.plot()). Label both axes.
        2. A histogram of the hours of the day, with one bin per hour.
            Label and set the limits of the x-axis.
    """
    array = np.load("FARS.npy")
    latitudes = array[:, 2]
    longitudes = array[:, 1]
    hours = array[:, 0]

    # first plot scatter plot
    plt.subplot(1, 2, 1)
    plt.plot(longitudes, latitudes, "k,")
    plt.xlabel("longitude")
    plt.ylabel("latitude")
    plt.axis("equal")

    # second plot histogram
    plt.subplot(1, 2, 2)
    plt.hist(hours, bins=np.arange(.5, 23.5, 1), edgecolor="black")
    plt.xlim(0, 24)
    plt.xlabel("Time")
    plt.ylabel("Crashes")
    
    # save and close figure
    plt.suptitle('Crash Data from FARS')
    plt.tight_layout()
    plt.savefig("scatter_histogram.jpg")


# Problem 6
def prob6():
    # creates a heat map as well as a contour map of g(x,y)
    # from -2pi to 2pi for both x and y
    """ Plot the function g(x,y) = sin(x)sin(y)/xy on the domain
    [-2pi, 2pi]x[-2pi, 2pi].
        1. Create 2 subplots: one with a heat map of g, and one with a contour
            map of g. Choose an appropriate number of level curves, or specify
            the curves yourself.
        2. Set the limits of each subplot to [-2pi, 2pi]x[-2pi, 2pi].
        3. Choose a non-default color scheme.
        4. Include a color scale bar for each subplot.
    """
    xs = np.arange(-2*np.pi, 2*np.pi, 4*np.pi/1000)
    ys = xs.copy()
    X, Y = np.meshgrid(xs, ys)
    Z = np.sin(X) * np.sin(Y) / (X * Y)
    
    plt.subplot(1, 2, 1)
    plt.pcolormesh(X, Y, Z, cmap="viridis", shading="auto")
    plt.colorbar()
    plt.xlim(-2*np.pi, 2*np.pi)
    plt.ylim(-2*np.pi, 2*np.pi)
    plt.xlabel("x")
    plt.ylabel("y")
    
    plt.subplot(1, 2, 2)
    plt.contour(X, Y, Z, 10, cmap="magma")
    plt.colorbar()
    plt.xlim(-2*np.pi, 2*np.pi)
    plt.ylim(-2*np.pi, 2*np.pi)
    plt.xlabel("x")
    plt.ylabel("y")

    plt.suptitle("Heat and Contour Maps of g(x,y)")
    plt.tight_layout()
    plt.savefig("heat_contour_maps.jpg")


if __name__ == "__main__":
    prob1()
    plt.clf()
    prob2()
    plt.clf()
    prob3()
    plt.clf()
    prob4()
    plt.clf()
    prob5()
    plt.clf()
    prob6()

