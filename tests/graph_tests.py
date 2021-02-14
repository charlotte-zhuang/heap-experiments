import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from util import graph


def dijkstra_ssp_pairingheap_test() -> None:
    """A simple test for Dijkstra's using a paring heap."""

    adj_list = [
        [(0, 1), (6, 4)],
        [(10, 2), (1, 4)],
        [(5, 0), (2, 3)],
        [(3, 2)],
        [(1, 3)],
    ]
    ans = graph.dijkstra_ssp_pairingheap(adj_list, 0)
    assert ans[0].key == 0, "Dijkstra pairing heap distance mismatch"
    assert ans[1].key == 0, "Dijkstra pairing heap distance mismatch"
    assert ans[2].key == 5, "Dijkstra pairing heap distance mismatch"
    assert ans[3].key == 2, "Dijkstra pairing heap distance mismatch"
    assert ans[4].key == 1, "Dijkstra pairing heap distance mismatch"
    assert ans[0].pred == ans[0], "Dijkstra pairing heap predecessor mismatch"
    assert ans[1].pred == ans[0], "Dijkstra pairing heap predecessor mismatch"
    assert ans[2].pred == ans[3], "Dijkstra pairing heap predecessor mismatch"
    assert ans[3].pred == ans[4], "Dijkstra pairing heap predecessor mismatch"
    assert ans[4].pred == ans[1], "Dijkstra pairing heap predecessor mismatch"


def dijkstra_ssp_fibonacciheap_test() -> None:
    """A simple test for Dijkstra's using a fibonacci heap."""

    adj_list = [
        [(0, 1), (6, 4)],
        [(10, 2), (1, 4)],
        [(5, 0), (2, 3)],
        [(3, 2)],
        [(1, 3)],
    ]
    ans = graph.dijkstra_ssp_fibonacciheap(adj_list, 0)
    assert ans[0].key == 0, "Dijkstra Fibonacci heap distance mismatch"
    assert ans[1].key == 0, "Dijkstra Fibonacci heap distance mismatch"
    assert ans[2].key == 5, "Dijkstra Fibonacci heap distance mismatch"
    assert ans[3].key == 2, "Dijkstra Fibonacci heap distance mismatch"
    assert ans[4].key == 1, "Dijkstra Fibonacci heap distance mismatch"
    assert ans[0].pred == ans[0], "Dijkstra Fibonacci heap predecessor mismatch"
    assert ans[1].pred == ans[0], "Dijkstra Fibonacci heap predecessor mismatch"
    assert ans[2].pred == ans[3], "Dijkstra Fibonacci heap predecessor mismatch"
    assert ans[3].pred == ans[4], "Dijkstra Fibonacci heap predecessor mismatch"
    assert ans[4].pred == ans[1], "Dijkstra Fibonacci heap predecessor mismatch"


def dijkstra_ssp_binaryheap_test() -> None:
    """A simple test for Dijkstra's using a binary heap."""

    adj_list = [
        [(0, 1), (6, 4)],
        [(10, 2), (1, 4)],
        [(5, 0), (2, 3)],
        [(3, 2)],
        [(1, 3)],
    ]
    ans = graph.dijkstra_ssp_binaryheap(adj_list, 0)
    assert ans[0][0] == 0, "Dijkstra binary heap distance mismatch"
    assert ans[1][0] == 0, "Dijkstra binary heap distance mismatch"
    assert ans[2][0] == 5, "Dijkstra binary heap distance mismatch"
    assert ans[3][0] == 2, "Dijkstra binary heap distance mismatch"
    assert ans[4][0] == 1, "Dijkstra binary heap distance mismatch"
    assert ans[0][1] == 0, "Dijkstra binary heap predecessor mismatch"
    assert ans[1][1] == 0, "Dijkstra binary heap predecessor mismatch"
    assert ans[2][1] == 3, "Dijkstra binary heap predecessor mismatch"
    assert ans[3][1] == 4, "Dijkstra binary heap predecessor mismatch"
    assert ans[4][1] == 1, "Dijkstra binary heap predecessor mismatch"

def dijkstra_ssp_noheap_test() -> None:
    """A simple test for Dijkstra's without using a heap."""

    adj_list = [
        [(0, 1), (6, 4)],
        [(10, 2), (1, 4)],
        [(5, 0), (2, 3)],
        [(3, 2)],
        [(1, 3)],
    ]
    ans = graph.dijkstra_ssp_noheap(adj_list, 0)
    assert ans[0][0] == 0, "Dijkstra no heap distance mismatch"
    assert ans[1][0] == 0, "Dijkstra no heap distance mismatch"
    assert ans[2][0] == 5, "Dijkstra no heap distance mismatch"
    assert ans[3][0] == 2, "Dijkstra no heap distance mismatch"
    assert ans[4][0] == 1, "Dijkstra no heap distance mismatch"
    assert ans[0][1] == 0, "Dijkstra no heap predecessor mismatch"
    assert ans[1][1] == 0, "Dijkstra no heap predecessor mismatch"
    assert ans[2][1] == 3, "Dijkstra no heap predecessor mismatch"
    assert ans[3][1] == 4, "Dijkstra no heap predecessor mismatch"
    assert ans[4][1] == 1, "Dijkstra no heap predecessor mismatch"


def see_random_weights(size: int):
    adj_list = graph.rand_tree(size)
    graph.assign_random_weights(adj_list)
    print("Weighted tree")
    for u, edges in enumerate(adj_list):
        print(f"{u}: ", end="")
        print(*edges, sep=",")


def see_graph(vertices: int, edges: int) -> None:
    """Prints a random graph.

    Args:
        vertices (int): The number of vertices in the graph.
        edges (int): The number of edges in the graph.
    """

    adj_list = graph.rand_graph(vertices, edges)
    print("Graph")
    for u, edges in enumerate(adj_list):
        print(f"{u}: ", end="")
        print(*edges, sep=",")


def see_tree(size: int) -> None:
    """Prints a random tree.

    Args:
        size (int): The size of the tree.
    """

    adj_list = graph.rand_tree(size)
    print("Tree")
    for u, edges in enumerate(adj_list):
        print(f"{u}: ", end="")
        print(*edges, sep=",")


if __name__ == "__main__":
    dijkstra_ssp_pairingheap_test()
    dijkstra_ssp_fibonacciheap_test()
    dijkstra_ssp_binaryheap_test()
    dijkstra_ssp_noheap_test
    print("All graph tests passed")
