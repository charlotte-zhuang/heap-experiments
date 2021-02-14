#!/usr/bin/env python3.9

"""Generate heap runtime tests.

Attributes:
    MIN_VAL (int): A default minimum key value.
    MAX_VAL (int): A default maximum key value.
"""

import sys
from pathlib import Path
from random import randrange, choice
from heapq import heappop, heappush

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from util import graph

MIN_VAL = int(-1e9)
MAX_VAL = int(1e9)


def random_graph(
    test_data: Path,
    vertices: int = 100000,
    edges: int = 1000000,
    minweight: int = 0,
    maxweight: int = MAX_VAL,
) -> None:
    """Generates a random connected undirected graph.

    Args:
        test_data (Path): The file to write the graph to.
        vertices (int, optional): The number of vertices. Defaults to 100000.
        edges (int, optional): The number of edges. Defaults to 1000000.
        minweight (int, optional): The minimum weight. Defaults to 0.
        maxweight (int, optional): The maximum weight. Defaults to MAX_VAL.

    Returns:
        tuple[int]: (vertices, edges)
    """

    vertices = max(vertices, 1)
    if edges < vertices - 1:
        edges = vertices - 1
    elif edges * 2 > vertices * (vertices - 1):
        edges = vertices * (vertices - 1) // 2
    adj_list = graph.rand_graph(vertices, edges)
    graph.assign_random_weights(adj_list, minweight, maxweight)
    with test_data.open(mode="w") as dat:
        dat.write(f"graph {vertices}\n")
        for adj in adj_list:
            for w, v in adj:
                dat.write(f"{w},{v} ")
            dat.write("\n")
    return vertices, edges


def random_test(
    test_data: Path,
    size: int = 0,
    op: int = 1000000,
    addfreq: int = 1,
    decfreq: int = 1,
    popfreq: int = 1,
    minval: int = MIN_VAL,
    maxval: int = MAX_VAL,
) -> tuple[int]:
    """Generates random commands for a heap to execute.

    Args:
        test_data (Path): The file to write the test to.
        size (int, optional): The initial heap size. Defaults to 0.
        op (int, optional): The number of operations. Defaults to 1000000.
        addfreq (int, optional): The weighted frequency of add operations. Defaults to 1.
        decfreq (int, optional): The weighted frequency of decrease key operations. Defaults to 1.
        popfreq (int, optional): The weighted frequency of pop min operations. Defaults to 1.
        minval (int, optional): The minimum value to add to the heap. Defaults to MIN_VAL.
        maxval (int, optional): The maximum value to add to the heap. Defaults to MAX_VAL.

    Returns:
        tuple[int]: (total operations, add operations, decrease key
            operations, pop minimum operations, minval, maxval)
    """

    size = max(size, 0)
    op = max(op, 0)
    addfreq = max(addfreq, 0)
    decfreq = max(decfreq, 0)
    popfreq = max(popfreq, 0)
    minval = min(minval, maxval)
    if size + op == 0:
        op = 1
    if addfreq + decfreq + popfreq == 0:
        addfreq = 1
        decfreq = 1
        popfreq = 1
    totalfreq = addfreq + decfreq + popfreq
    arr = []
    heap = []
    add = dec = pop = 0

    if popfreq < decfreq:

        def rand_dec_choice():
            i = randrange(len(arr))
            return arr[i], i

    else:

        def rand_dec_choice():
            return choice(heap)

    with test_data.open(mode="w") as dat:
        dat.write("heap\n")
        for _ in range(size):
            num = randrange(minval, maxval + 1)
            heappush(heap, (num, len(arr)))
            arr.append(num)
            dat.write(f"a {num}\n")
            add += 1
        heapsize = size
        for _ in range(op):
            action = randrange(totalfreq)
            if action < decfreq and heapsize != 0:
                # decrease key
                key, i = rand_dec_choice()
                while not (arr[i] and arr[i] == key):
                    key, i = rand_dec_choice()
                nk = randrange(minval, key + 1)
                heappush(heap, (nk, i))
                arr[i] = nk
                dat.write(f"d {i} {nk}\n")
                dec += 1
            elif action < decfreq + popfreq and heapsize != 0:
                # pop
                elem = heappop(heap)
                while arr[elem[1]] != elem[0]:
                    elem = heappop(heap)
                arr[elem[1]] = None
                heapsize -= 1
                dat.write("p\n")
                pop += 1
            else:
                # add
                num = randrange(minval, maxval + 1)
                heappush(heap, (num, len(arr)))
                arr.append(num)
                heapsize += 1
                dat.write(f"a {num}\n")
                add += 1
    total = size + op
    return total, add, dec, pop, minval, maxval
