#!/usr/bin/env python3.9

"""Graph algorithms

Attributes:
    MAX_VAL (int): A default maximum weight value.
"""

from random import randrange
from heapq import heappop, heappush
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from util import pairingheap, fibonacciheap

MAX_VAL = int(1e9)


def dijkstra_ssp_pairingheap(
    adj_list: list[list[tuple[int]]], src: int
) -> list[tuple[int]]:
    """Dijkstra's single source shortest path algorithm. Finds the minimum
        weight path to reach all vertices from a source. Uses a pairing heap.

    Args:
        adj_list (list[list[tuple[int]]]): The graph in adjacency list format.
            Weights must be positive.
            adj_list[vertex index] = [(weight, adjacent index)]
        src (int): The source index.

    Returns:
        list[HeapNode]: HeapNodes with minimum distances and the
            second-to-last vertex on a path from the source to the vertex.
            HeapNode.key (int): minimum distance
            HeapNode.pred (HeapNode): the predecessor
    """

    nodes = [None] * len(adj_list)
    q = pairingheap.Heap()
    nodes[src] = q.add(0)
    nodes[src].index = src
    nodes[src].pred = nodes[src]
    while q.size != 0:
        u = q.pop()
        # relax al edges out of u
        for w, v in adj_list[u.index]:
            if nodes[v]:
                v = nodes[v]
                if v.key > u.key + w:
                    q.decreasekey(v, u.key + w)
                    v.pred = u
            else:
                nodes[v] = q.add(u.key + w)
                nodes[v].index = v
                nodes[v].pred = u
    return nodes


def dijkstra_ssp_fibonacciheap(
    adj_list: list[list[tuple[int]]], src: int
) -> list[tuple[int]]:
    """Dijkstra's single source shortest path algorithm. Finds the minimum
        weight path to reach all vertices from a source. Uses a Fibonacci
        heap. The path is not stored, but it could be.

    Args:
        adj_list (list[list[tuple[int]]]): The graph in adjacency list format.
            Weights must be positive.
            adj_list[vertex index] = [(weight, adjacent index)]
        src (int): The source index.

    Returns:
        list[HeapNode]: HeapNodes with minimum distances and the
            second-to-last vertex on a path from the source to the vertex.
            HeapNode.key (int): minimum distance
            HeapNodes.pred (HeapNode): the predecessor
    """

    nodes = [None] * len(adj_list)
    q = fibonacciheap.Heap()
    nodes[src] = q.add(0)
    nodes[src].index = src
    nodes[src].pred = nodes[src]
    while q.size != 0:
        u = q.pop()
        # relax all edges out of u
        for w, v in adj_list[u.index]:
            if nodes[v]:
                v = nodes[v]
                if v.key > u.key + w:
                    q.decreasekey(v, u.key + w)
                    v.pred = u
            else:
                nodes[v] = q.add(u.key + w)
                nodes[v].index = v
                nodes[v].pred = u
    return nodes


def dijkstra_ssp_binaryheap(
    adj_list: list[list[tuple[int]]], src: int
) -> list[tuple[int]]:
    """Dijkstra's single source shortest path algorithm. Finds the minimum
        weight path to reach all vertices from a source. Uses a binary
        heap.

    Args:
        adj_list (list[list[tuple[int]]]): The graph in adjacency list format.
            Weights must be positive.
            adj_list[vertex index] = [(weight, adjacent index)]
        src (int): The source index.

    Returns:
        list[tuple[int]]: (minimum distance, predecessor)
    """

    dis = [None] * len(adj_list)
    q = [(0, src)]
    dis[src] = (0, src)
    while q:
        u = heappop(q)
        while q and dis[u[1]][0] != u[0]:
            u = heappop(q)
        if dis[u[1]][0] != u[0]:
            # q is empty
            return dis
        # relax all edges out of u
        for w, v in adj_list[u[1]]:
            if dis[v]:
                if dis[v][0] > u[0] + w:
                    heappush(q, (u[0] + w, v))
                    dis[v] = (u[0] + w, u[1])
            else:
                heappush(q, (u[0] + w, v))
                dis[v] = (u[0] + w, u[1])
    return dis


def dijkstra_ssp_noheap(adj_list: list[list[tuple[int]]], src: int) -> list[tuple[int]]:
    """Dijkstra's single source shortest path algorithm. Finds the minimum
        weight path to reach all vertices from a source. Does not use a
        priority queue.

    Args:
        adj_list (list[list[tuple[int]]]): The graph in adjacency list format.
            Weights must be positive.
            adj_list[vertex index] = [(weight, adjacent index)]
        src (int): The source index.

    Returns:
        list[tuple[int]]: (minimum distance, predecessor)
    """

    dis = [None] * len(adj_list)
    dis[src] = (0, src, False)
    while True:
        # find the minimum value in dis
        u = ui = None
        for i, e in enumerate(dis):
            if e and not e[2] and (not u or e[0] < u[0]):
                u = e
                ui = i
        if not u:
            # all vertices are done
            return dis
        # vertex u is done
        dis[ui] = (u[0], u[1], True)
        # relax all edges out of u
        for w, v in adj_list[ui]:
            if dis[v]:
                if dis[v][0] > u[0] + w:
                    dis[v] = (u[0] + w, ui, False)
            else:
                dis[v] = (u[0] + w, ui, False)


def rand_graph(vertices: int, edges: int) -> list[list[int]]:
    """Generates a random connected undirected graph.

    Args:
        vertices (int): The number of vertices
        edges (int): The number of edges.
            vertices - 1 <= edges <= vertices (vertices - 1) / 2

    Raises:
        ValueError: If edges is outside the appropriate range.

    Returns:
        list[list[int]]: The graph in adjacency list format:
            list[vertex index] = [adjacent index]
    """

    if edges + 1 < vertices:
        raise ValueError("Too few edges")
    if edges * 4 > vertices * (vertices - 1):
        # graph is more than 50% complete: start from a complete graph and
        # remove edges
        remove_edges = (vertices * (vertices - 1) // 2) - edges
        if remove_edges < 0:
            raise ValueError("Too many edges")
        adj_list = [set() for _ in range(vertices)]
        for v, adj in enumerate(adj_list):
            for u in range(vertices):
                if u != v:
                    adj.add(u)
        # remove edges
        for _ in range(remove_edges):
            u = v = 0
            while (
                u == v
                or len(adj_list[v]) == 0
                or len(adj_list[u]) == 0
                or u not in adj_list[v]
            ):
                u = randrange(vertices)
                v = randrange(vertices)
            adj_list[v].remove(u)
            adj_list[u].remove(v)
        # convert sets to lists
        for i in range(vertices):
            adj_list[i] = list(adj_list[i])
        return adj_list
    # graph is at most 50% complete: start from tree and add edges
    adj_list = rand_tree(vertices)
    for _ in range(edges - vertices + 1):
        u = v = 0
        while u == v or u in adj_list[v]:
            u = randrange(vertices)
            v = randrange(vertices)
        adj_list[u].append(v)
        adj_list[v].append(u)
    return adj_list


def assign_random_weights(
    adj_list: list[list[int]], minweight: int = 0, maxweight: int = MAX_VAL
) -> list[list[tuple[int]]]:
    """Assigns random weights to an undirected graph.

    Args:
        adj_list (list[list[int]]): A graph as an adjacency list.
        minweight (int, optional): The minimum weight for an edge. Defaults to 0.
        maxweight (int, optional): The maximum weight for an edge. Defaults to MAX_VAL.

    Returns:
        list[list[tuple[int]]]: The original adjacency list:
            list[vertex index] = [(weight, adjacent index)]
    """

    for edges in adj_list:
        for i in range(len(edges)):
            edges[i] = (randrange(minweight, maxweight + 1), edges[i])
    return adj_list


def rand_tree(size: int) -> list[list[int]]:
    """Generates a random tree (undirected).

    Args:
        size (int): The number of vertices in the tree.

    Returns:
        list[list[int]]: The tree in adjacency list format:
            list[vertex index] = [adjacent index]
    """

    prufer = rand_prufer_seq(size)
    adj_list = [[] for _ in range(size)]
    degree = [1] * size
    # calculate degrees
    for u in prufer:
        degree[u] += 1
    # make edges
    for u in prufer:
        v = degree.index(1)
        adj_list[u].append(v)
        adj_list[v].append(u)
        degree[u] -= 1
        degree[v] -= 1
    # make last edge
    u = degree.index(1)
    v = degree.index(1, u + 1)
    adj_list[u].append(v)
    adj_list[v].append(u)
    return adj_list


def rand_prufer_seq(size: int) -> list[int]:
    """Generates a random Prufer sequence.

    Args:
        size (int): The number of vertices in the tree.

    Returns:
        list[int]: The Prufer sequence of length size - 2.
    """

    return [randrange(0, size) for _ in range(size - 2)]
