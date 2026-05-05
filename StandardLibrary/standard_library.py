import itertools as it
import box as b
import sys
import random as r
import time
import calculator as c

# standard_library.py
"""Python Essentials: The Standard Library.
<Lane Lindstrom>
<Math 321>
<01/15/2026>
"""


# Problem 1
def prob1(L):
    # returns min, max, and avg of a set L in that order, separated by commas
    """Return the minimum, maximum, and average of the entries of L
    (in that order).
    """
    return min(L), max(L), sum(L)/len(L)


# Problem 2
def prob2():
    # prints a verifying comparison of mutability. true means that the data type IS mutable
    """Determine which Python objects are mutable and which are immutable.
    Test integers, strings, lists, tuples, and sets. Print your results.
    """
    integer = int(1)
    integ = integer
    integ += 1
    print(f'Is an integer mutable? {integ == integer}')

    string = 'mystring'
    strin = string
    strin += '123'
    print(f'Is a string mutable? {string == strin}')

    lis = [1, 2, 'you']
    li = lis
    li.append('me')
    print(f'Is a list mutable? {lis == li}')

    tup = (1, 2, 3)
    newtup = tup
    newtup += (1, 0)
    print(f'Is a tuple mutable? {tup == newtup}')

    myset = {1, 4, 6}
    newset = myset
    newset.remove(1)
    print(f'Is a set mutable? {myset == newset}')


# Problem 3
def hypot(a, b):
    # returns sqrt(a**2 + b**2) using only functions from calculator.py
    """Calculate and return the length of the hypotenuse of a right triangle.
    Do not use any functions other than sum(), product() and sqrt() that are
    imported from your 'calculator' module.

    Parameters:
        a: the length one of the sides of the triangle.
        b: the length the other non-hypotenuse side of the triangle.
    Returns:
        The length of the triangle's hypotenuse.
    """
    return c.sqrt(c.sum(c.product(a, a), c.product(b, b)))


# Problem 4
def power_set(A):
    """Use itertools to compute the power set of A.

    Parameters:
        A (iterable): a str, list, set, tuple, or other iterable collection.

    Returns:
        (list(sets)): The power set of A as a list of sets.
    """
    # returns the power set of input iterator A
    ans_set = []
    for i in range(len(A) + 1):
        ans_set.extend(set(c) for c in it.combinations(A, i))
    return ans_set
    # this must be a list of sets because sets cannot contain mutable objects, ie sets of sets.


# Problem 5: Implement shut the box.
def shut_the_box(player, timelimit):
    # play a game of shut the box with player and time limit
    """Play a single game of shut the box."""

    # initialize times and numbers available
    start_time = time.time()
    current_time = time.time()
    nums_available = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # loop until a winning or losing condition is met (time or completion of game)
    while True:
        current_time = time.time()
        if current_time - start_time > float(timelimit):
            break
        print(f"\nNumbers left: {nums_available}")
        if sum(nums_available) <= 6:
            die_roll = r.randint(1, 6)
            while not b.isvalid(die_roll, nums_available):
                die_roll = r.randint(1, 6)
        else:
            die_roll = r.randint(1, 6) + r.randint(1, 6)
            while not b.isvalid(die_roll, nums_available):
                die_roll = r.randint(1, 6) + r.randint(1, 6)
        print(f"Roll: {die_roll}")
        print(f"Seconds left: {round(float(timelimit) - (current_time - start_time), 2)}")
        selected_values = input('Numbers to eliminate: ')
        values = b.parse_input(selected_values, nums_available)
        if values == []:
            print("Invalid input")
            continue
        if sum(values) != die_roll:
            print("Invalid input")
            continue
        for value in values:
            nums_available.remove(value)
        if nums_available == []:
            print(f"\nScore for player {player}: {sum(nums_available)} points")
            print(f"Time played: {current_time - start_time}")
            print("Congratulations!! You shut the box!")
            return

    print('Game over!\n')
    print(f"Score for player {player}: {sum(nums_available)} points")
    print(f"Time played: {round((current_time - start_time), 2)}")
    print("Better luck next time >:)")


if __name__ == '__main__':
    if len(sys.argv) == 3:
        shut_the_box(sys.argv[1], sys.argv[2])
    else:
        print("Error, two arguments are required after the python file name. ex: standard_library.py playername time_limit")      
