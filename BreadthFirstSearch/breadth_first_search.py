# breadth_first_search.py
"""Volume 2: Breadth-First Search.
<Lane Lindstrom>
<Math 321>
<2/26/2026>
"""

import networkx as nx
from numpy import mean
from collections import deque
from matplotlib import pyplot as plt

# Problems 1-3
class Graph:
    """A graph object, stored as an adjacency dictionary. Each node in the
    graph is a key in the dictionary. The value of each key is a set of
    the corresponding node's neighbors.

    Attributes:
        d (dict): the adjacency dictionary of the graph.
    """
    def __init__(self, adjacency={}):
        """Store the adjacency dictionary as a class attribute"""
        self.d = dict(adjacency)

    def __str__(self):
        """String representation: a view of the adjacency dictionary."""
        return str(self.d)

    # Problem 1
    def add_node(self, n):
        """Add n to the graph (with no initial edges) if it is not already
        present.

        Parameters:
            n: the label for the new node.
        """
        if n not in self.d:
            self.d[n] = set()

    # Problem 1
    def add_edge(self, u, v):
        """Add an edge between node u and node v. Also add u and v to the graph
        if they are not already present.

        Parameters:
            u: a node label.
            v: a node label.
        """
        if u not in self.d:
            self.add_node(u)
        if v not in self.d:
            self.add_node(v)
        self.d[v].add(u)
        self.d[u].add(v)

    # Problem 1
    def remove_node(self, n):
        """Remove n from the graph, including all edges adjacent to it.

        Parameters:
            n: the label for the node to remove.

        Raises:
            KeyError: if n is not in the graph.
        """
        if n not in self.d:
            raise KeyError(f"[{n} not in the graph]")
        
        for neighbor in self.d[n]:
            self.d[neighbor].remove(n)
        self.d.pop(n)

    # Problem 1
    def remove_edge(self, u, v):
        """Remove the edge between nodes u and v.

        Parameters:
            u: a node label.
            v: a node label.

        Raises:
            KeyError: if u or v are not in the graph, or if there is no
                edge between u and v.
        """
        if u not in self.d or v not in self.d:
            raise KeyError("either node inputted is not in the dictionary")
        self.d[v].remove(u)
        self.d[u].remove(v)

    # Problem 2
    def traverse(self, source):
        """Traverse the graph with a breadth-first search until all nodes
        have been visited. Return the list of nodes in the order that they
        were visited.

        Parameters:
            source: the node to start the search at.

        Returns:
            (list): the nodes in order of visitation.

        Raises:
            KeyError: if the source node is not in the graph.
        """
        if source not in self.d:
            raise KeyError("given source not in the graph")
        queue = deque()
        visited = set([source])
        visited_order = []
        queue.append(source)
        while queue:
            current = queue.popleft()
            visited_order.append(current)
            for node in self.d[current]:
                if node not in visited:
                    queue.append(node)
                    visited.add(node)
        return visited_order

    # Problem 3
    def shortest_path(self, source, target):
        """Begin a BFS at the source node and proceed until the target is
        found. Return a list containing the nodes in the shortest path from
        the source to the target, including endoints.

        Parameters:
            source: the node to start the search at.
            target: the node to search for.

        Returns:
            A list of nodes along the shortest path from source to target,
                including the endpoints.

        Raises:
            KeyError: if the source or target nodes are not in the graph.
        """
        if source not in self.d or target not in self.d:
            raise KeyError("given source or target not in the graph")
        queue = deque()
        visited = set([source])
        back_path = {}
        queue.append(source)
        if source == target:
            return [source]
        while queue:
            current = queue.popleft()
            if current == target:
                answer = deque()
                while current != source:
                    answer.appendleft(current)
                    current = back_path[current]
                answer.appendleft(source)
                return list(answer)
            else:
                for node in self.d[current]:
                    if node not in visited:
                        visited.add(node)
                        back_path[node] = current
                        queue.append(node)
             
        raise ValueError("target and source in graph, but no edges connect them")

# Problems 4-6
class MovieGraph:
    """Class for solving the Kevin Bacon problem with movie data from IMDb."""

    # Problem 4
    def __init__(self, filename="movie_data.txt"):
        """Initialize a set for movie titles, a set for actor names, and an
        empty NetworkX Graph, and store them as attributes. Read the speficied
        file line by line, adding the title to the set of movies and the cast
        members to the set of actors. Add an edge to the graph between the
        movie and each cast member.

        Each line of the file represents one movie: the title is listed first,
        then the cast members, with entries separated by a '/' character.
        For example, the line for 'The Dark Knight (2008)' starts with

        The Dark Knight (2008)/Christian Bale/Heath Ledger/Aaron Eckhart/...

        Any '/' characters in movie titles have been replaced with the
        vertical pipe character | (for example, Frost|Nixon (2008)).
        """
        self.movies = set()
        self.actors = set()
        self.graph = nx.Graph()
        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                entries = line.strip().split('/')
                self.movies.add(entries[0])
                for actor in entries[1:]:
                    self.actors.add(actor)
                    self.graph.add_edge(entries[0], actor)

    # Problem 5
    def path_to_actor(self, source, target):
        """Compute the shortest path from source to target and the degrees of
        separation between source and target.

        Returns:
            (list): a shortest path from source to target, including endpoints and movies.
            (int): the number of steps from source to target, excluding movies.
        """
        if target not in self.graph or source not in self.graph:
            raise ValueError("Target or source not in graph")
        else:
            path = nx.shortest_path(self.graph, source, target)
            return path, len(path)//2

    # Problem 6
    def average_number(self, target):
        """Calculate the shortest path lengths of every actor to the target
        (not including movies). Plot the distribution of path lengths and
        return the average path length.

        Returns:
            (float): the average path length from actor to target.
        """
        if target not in self.graph:
            raise KeyError("Actor not in graph")
        lengths = nx.single_source_shortest_path_length(self.graph, target)
        actor_lengths = [dist//2 for actor, dist in lengths.items() if actor in self.actors]
        plt.hist(actor_lengths, bins=[i-.5 for i in range(8)])
        plt.xlabel("Degrees of Separation")
        plt.ylabel("Number of Actors")
        plt.title("Degrees of Separation")
        plt.savefig("DegreesofBacon")
        return mean(actor_lengths)


if __name__ == "__main__":
    pass
