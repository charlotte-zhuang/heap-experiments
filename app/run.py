#!/usr/bin/env python3.9

"""Conduct runtime tests on heaps."""

import sys
from pathlib import Path
from timeit import default_timer
from heapq import heappop, heappush

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from util import pairingheap, fibonacciheap, graph


def pairing_time(testdata: Path) -> float:
    """Executes a heap test using a pairing heap.

    Args:
        test_data (Path): The test data.

    Raises:
        Exception: If the data could not be read.

    Returns:
        float: Execution time in seconds.
    """

    ops = read_operations(testdata)
    start = default_timer()
    heap = pairingheap.Heap()
    nodes = []
    for o in ops:
        if o[0] == "d":
            heap.decreasekey(nodes[o[1]], o[2])
        elif o[0] == "a":
            nodes.append(heap.add(o[1]))
        else:
            heap.pop()
    stop = default_timer()
    return stop - start


def fibonacci_time(testdata: Path) -> float:
    """Executes a heap test using a Fibonacci heap.

    Args:
        test_data (Path): The test data.

    Raises:
        Exception: If the data could not be read.

    Returns:
        float: Execution time in seconds.
    """

    ops = read_operations(testdata)
    start = default_timer()
    heap = fibonacciheap.Heap()
    nodes = []
    for o in ops:
        if o[0] == "d":
            heap.decreasekey(nodes[o[1]], o[2])
        elif o[0] == "a":
            nodes.append(heap.add(o[1]))
        else:
            heap.pop()
    stop = default_timer()
    return stop - start


def binary_time(testdata: Path) -> float:
    """Executes a heap test using a pairing heap.

    Args:
        test_data (Path): The test data.

    Raises:
        Exception: If the test could not be read.

    Returns:
        float: Execution time in seconds.
    """

    ops = read_operations(testdata)
    start = default_timer()
    heap = []
    arr = []
    for o in ops:
        if o[0] == "d":
            arr[o[1]] = o[2]
            heappush(heap, (o[2], o[1]))
            while arr[heap[0][1]] != heap[0][0]:
                heappop(heap)
        elif o[0] == "a":
            heappush(heap, (o[1], len(arr)))
            arr.append(o[1])
        else:
            elem = heappop(heap)
            while arr[elem[1]] != elem[0]:
                elem = heappop(heap)
            arr[elem[1]] = None
    stop = default_timer()
    return stop - start


def noheap_time(testdata: Path) -> float:
    """Executes a heap test without using a heap (linear search).

    Args:
        test_data (Path): The test data.

    Raises:
        Exception: If the test could not be read.

    Returns:
        float: Execution time in seconds.
    """

    ops = read_operations(testdata)
    start = default_timer()
    arr = []
    for o in ops:
        if o[0] == "d":
            arr[o[1]] = o[2]
        elif o[0] == "a":
            arr.append(o[1])
        else:
            i = v = None
            for j, a in enumerate(arr):
                if a and (not v or a < v):
                    i = j
                    v = a
            if i:
                arr[i] = None
    stop = default_timer()
    return stop - start


def dijkstra_pairing_time(graphdata: Path) -> float:
    """Executes Dijkstra's with a pairing heap.

    Args:
        graphdata (Path): The file with the graph.

    Raises:
        Exception: If the test could not be read.

    Returns:
        float: Execution time in seconds.
    """

    adj_list = read_graph(graphdata)
    start = default_timer()
    graph.dijkstra_ssp_pairingheap(adj_list, 0)
    stop = default_timer()
    return stop - start


def dijkstra_fibonacci_time(graphdata: Path) -> float:
    """Executes Dijkstra's with a Fibonacci heap.

    Args:
        graphdata (Path): The file with the graph.

    Raises:
        Exception: If the test could not be read.

    Returns:
        float: Execution time in seconds.
    """

    adj_list = read_graph(graphdata)
    start = default_timer()
    graph.dijkstra_ssp_fibonacciheap(adj_list, 0)
    stop = default_timer()
    return stop - start


def dijkstra_binary_time(graphdata: Path) -> float:
    """Executes Dijkstra's with a binary heap.

    Args:
        graphdata (Path): The file with the graph.

    Raises:
        Exception: If the test could not be read.

    Returns:
        float: Execution time in seconds.
    """

    adj_list = read_graph(graphdata)
    start = default_timer()
    graph.dijkstra_ssp_binaryheap(adj_list, 0)
    stop = default_timer()
    return stop - start


def dijkstra_noheap_time(graphdata: Path) -> float:
    """Executes Dijkstra's without a heap.

    Args:
        graphdata (Path): The file with the graph.

    Raises:
        Exception: If the test could not be read.

    Returns:
        float: Execution time in seconds.
    """

    adj_list = read_graph(graphdata)
    start = default_timer()
    graph.dijkstra_ssp_noheap(adj_list, 0)
    stop = default_timer()
    return stop - start


def read_operations(testdata: Path) -> tuple[int, list[tuple]]:
    """Reads test data from a file.

    Args:
        test_data (Path): The file to write the test to.

    Raises:
        ValueError: If the test data could not be read.

    Returns:
        list[tuple]: A list of all commands in the following form:

            ("d", index, amt) decrease key at the index by an amount
            ("a", key) add key
            ("p") pop minimum
    """

    ops = []
    with testdata.open(mode="r") as dat:
        mode = dat.readline().strip()
        if mode != "heap":
            raise ValueError("This is not a heap test")
        for line in dat:
            line = line.split()
            if line[0] == "d":
                ops.append(("d", int(line[1]), int(line[2])))
            elif line[0] == "a":
                ops.append(("a", int(line[1])))
            else:
                ops.append(("p"))
    return ops


def read_graph(graphdata: Path) -> list[list[tuple[int]]]:
    """Reads a graph from a file.

    Args:
        graphdata (Path): The file to read the graph from.

    Raises:
        ValueError: If the graph could not be read.

    Returns:
        list[list[tuple[int]]]: An adjacency list of the graph.
            list[vertex index] = [(weight, adjacent index)]
    """

    with graphdata.open(mode="r") as dat:
        info = dat.readline().split()
        if info[0] != "graph":
            raise ValueError("This is not a graph")
        n = int(info[1])
        adj_list = [[] for _ in range(n)]
        for u, line in enumerate(dat):
            edges = line.split()
            for e in edges:
                w, v = map(int, e.split(","))
                adj_list[u].append((w, v))
                adj_list[v].append((w, u))
    return adj_list
