# markov_chains.py
"""Volume 2: Markov Chains.
<Lane Lindstrom>
<Math 321>
<03/12/2026>
"""

import numpy as np
from scipy import linalg as la


class MarkovChain:
    """A Markov chain with finitely many states.

    Attributes:
        states: a list of labels for the row/columns
        d: a dictionary mapping labels to their respective row/column
        A: The column stochastic matrix for the chain
    """
    # Problem 1
    def __init__(self, A, states=None):
        """Check that A is column stochastic and construct a dictionary
        mapping a state's label to its index (the row / column of A that the
        state corresponds to). Save the transition matrix, the list of state
        labels, and the label-to-index dictionary as attributes.

        Parameters:
        A ((n,n) ndarray): the column-stochastic transition matrix for a
            Markov chain with n states.
        states (list(str)): a list of n labels corresponding to the n states.
            If not provided, the labels are the indices 0, 1, ..., n-1.

        Raises:
            ValueError: if A is not square or is not column stochastic.

        Example:
            >>> MarkovChain(np.array([[.5, .8], [.5, .2]], states=["A", "B"])
        corresponds to the Markov Chain with transition matrix
                                   from A  from B
                            to A [   .5      .8   ]
                            to B [   .5      .2   ]
        and the label-to-index dictionary is {"A":0, "B":1}.
        """
        a, b = A.shape
        self.d = {}
        if not np.allclose(A.sum(axis=0), np.ones(b)) or a != b:
            raise ValueError
        if states is None:
            states = list(range(a))
        for i in range(len(states)):
            self.d[states[i]] = i
        self.m = A
        self.states = states

    def transition(self, state):
        """Transition to a new state by making a random draw from the outgoing
        probabilities of the state with the specified label.

        Parameters:
            state (str): the label for the current state.

        Returns:
            (str): the label of the state to transitioned to.
        """
        index = self.d[state]
        probs = self.m[:, index]
        transition = np.random.multinomial(1, probs)
        new_index = np.argmax(transition)
        return self.states[new_index]

    # Problem 3
    def walk(self, start, N):
        """Starting at the specified state, use the transition() method to
        transition from state to state N-1 times, recording the state label at
        each step.

        Parameters:
            start (str): The starting state label.

        Returns:
            (list(str)): A list of N state labels, including start.
        """
        states = [start]
        current = start

        for _ in range(N - 1):
            current = self.transition(current)
            states.append(current)

        return states

    # Problem 3
    def path(self, start, stop):
        """Beginning at the start state, transition from state to state until
        arriving at the stop state, recording the state label at each step.

        Parameters:
            start (str): The starting state label.
            stop (str): The stopping state label.

        Returns:
            (list(str)): A list of state labels from start to stop.
        """
        states = [start]
        current = start

        while current != stop:
            current = self.transition(current)
            states.append(current)

        return states

    # Problem 4
    def steady_state(self, tol=1e-12, maxiter=1000):
        """Compute the steady state of the transition matrix A.

        Parameters:
            tol (float): The convergence tolerance.
            maxiter (int): The maximum number of iterations to compute.

        Returns:
            ((n,) ndarray): The steady state distribution vector of A.

        Raises:
            ValueError: if there is no convergence within maxiter iterations.
        """
        n = self.m.shape[0]

        x = np.ones(n) / n

        for _ in range(maxiter):
            x_next = self.m @ x

            if la.norm(x_next - x) < tol:
                return x_next

            x = x_next

        raise ValueError("No convergence within maxiter")


class SentenceGenerator(MarkovChain):
    """A Markov-based simulator for natural language.

    Attributes:
        (fill this out)
    """
    # Problem 5
    def __init__(self, filename):
        """Read the specified file and build a transition matrix from its
        contents. You may assume that the file has one complete sentence
        written on each line.
        """
        with open(filename, 'r') as f:
            lines = f.readlines()

        words = set()
        sentences = []

        for line in lines:
            sentence = line.strip().split()
            sentences.append(sentence)
            words.update(sentence)

        words = list(words)
        words = ["$tart"] + words + ["$top"]

        n = len(words)
        word_to_index = {word: i for i, word in enumerate(words)}

        A = np.zeros((n, n))

        for sentence in sentences:
            prev = "$tart"

            for word in sentence:
                i = word_to_index[word]
                j = word_to_index[prev]
                A[i, j] += 1
                prev = word

            # transition to $top
            i = word_to_index["$top"]
            j = word_to_index[prev]
            A[i, j] += 1

        top_index = word_to_index["$top"]
        A[:, top_index] = 0
        A[top_index, top_index] = 1

        for j in range(n):
            col_sum = A[:, j].sum()
            if col_sum != 0:
                A[:, j] /= col_sum

        super().__init__(A, states=words)

    # Problem 6
    def babble(self):
        """Create a random sentence using MarkovChain.path().

        Returns:
            (str): A sentence generated with the transition matrix, not
                including the labels for the $tart and $top states.

        Example:
            >>> yoda = SentenceGenerator("yoda.txt")
            >>> print(yoda.babble())
            The dark side of loss is a path as one with you.
        """
        path = self.path("$tart", "$top")
        words = path[1:-1]
        return " ".join(words)


if __name__ == "__main__":

    filename = "sample_sentences.txt"
    with open(filename, "w") as f:
        f.write("the force is strong\n")
        f.write("the force is with you\n")
        f.write("you are strong\n")

    print("=== Testing SentenceGenerator ===")
    sg = SentenceGenerator("yoda.txt")

    print("\nStates:")
    print(sg.states)

    print("\nTransition Matrix:")
    print(sg.m)

    print("\nGenerated Sentences:")
    for _ in range(5):
        print("-", sg.babble())

    print("\n=== Testing walk() ===")
    walk = sg.walk("$tart", 10)
    print(walk)

    print("\n=== Testing path() ===")
    path = sg.path("$tart", "$top")
    print(path)

    print("\n=== Testing steady_state() ===")
    try:
        steady = sg.steady_state()
        print("Steady state distribution:")
        print(steady)
        print("Sum:", np.sum(steady))
    except ValueError as e:
        print("Steady state failed:", e)
