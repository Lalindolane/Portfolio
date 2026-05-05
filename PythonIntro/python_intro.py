# python_intro.py
"""Python Essentials: Introduction to Python.
<Lane Lindstrom>
<Math 321>
<01/8/2026>
"""


# Problem 2
def sphere_volume(r):
    """ Returns the volume of a sphere of radius r, using 3.14159 as pi
    """
    pi = 3.14159
    return (4/3)*pi*r**3


# Problem 3
def isolate(a, b, c, d, e):
    """ Print the first three arguments separated by 5 spaces and then print
    the last two arguments with a single space separating the last three arguments

    Example:
    >>> isolate(1, 2, 3, 4, 5)
    1     2     3 4 5
    """
    print(f'{a}     {b}     {c} {d} {e}')


# Problem 4
def first_half(my_string):
    """ Return the first half of the given string. If the length
    of the string is odd, the middle character is not included.

    Examples:
        >>> first_half("python")
        'pyt'
        >>> first_half("ipython")
        'ipy'
    """
    new_string = my_string[:len(my_string)//2]
    return new_string


def backward(my_string):
    """ Return the reverse of the given string.

    Examples:
        >>> backward("python")
        'nohtyp'
        >>> backward("ipython")
        'nohtypi'
    """
    new_string = my_string[-1::-1]
    return new_string


# Problem 5
def list_ops():
    """ Define a list with the entries "bear", "ant", "cat", and "dog" (in this order).
    Performs the following operations on the list:
        - Append "eagle".
        - Replace the entry at index 2 with "fox".
        - Remove (or pop) the entry at index 1.
        - Sort the list in reverse alphabetical order.
        - Replace "eagle" with "hawk".
        - Add the string "hunter" to the last entry in the list.
    Return the resulting list.

    Examples:
        >>> list_ops()
        ['fox', 'hawk', 'dog', 'bearhunter']
    """
    lis = ['bear', 'ant', 'cat', 'dog']
    lis.append('eagle')
    lis.pop(2)
    lis.insert(2, 'fox')
    lis.pop(1)
    lis.sort(reverse=True)
    i = lis.index('eagle')
    lis.pop(i)
    lis.insert(i, 'hawk')
    lis[-1] = lis[-1] + 'hunter'
    return lis


# Problem 6
def pig_latin(word):
    """ Translate the string 'word' into Pig Latin, and return the new word.
    rules are if word starts with a vowel, add 'hay' to the end. if the
    word starts with a consonant, remove the first letter and add it to the
    end along with 'ay'

    Examples:
        >>> pig_latin("apple")
        'applehay'
        >>> pig_latin("banana")
        'ananabay'
    """
    new_string = ''
    vowels = {'a', 'e', 'i', 'o', 'u'}
    if word[0] in vowels:
        new_string = word + 'hay'
    else:
        new_string = word[1:] + word[0] + 'ay'
    return new_string


# Problem 7
def palindrome():
    """ Find and retun the largest panindromic number made from the product
    of two 3-digit numbers.
    """
    candidates = []
    for i in range(100, 1000):
        for j in range(100, 1000):
            n = str(i*j)
            first = first_half(n)
            if len(n) % 2 == 0:
                second_half = n[int(len(n)/2):]
                if first == backward(second_half):
                    candidates.append(int(n))
            else:
                second_half = n[int(len(n)//2+1):]
                if first == backward(second_half):
                    candidates.append(int(n))
    return max(candidates)


# Problem 8
def alt_harmonic(n):
    """ Return the partial sum of the first n terms of the alternating
    harmonic series, which approximates ln(2).
    """
    return sum((-1)**(i+1)/i for i in range(1, n+1))


if __name__ == "__main__":
    print('Hello, world!')