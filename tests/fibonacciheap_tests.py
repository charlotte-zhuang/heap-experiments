import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from random import randrange, choice
from heapq import heappush, heappop
from util import fibonacciheap

MIN_VAL = int(-1e9)
MAX_VAL = int(1e9)


def remove_test(
    size: int = 10000, rep: int = 1000, minval: int = MIN_VAL, maxval: int = MAX_VAL
) -> bool:
    """Tests the remove operation.

    Args:
        size (int): The size of the test heap.
        rep (int): The repetitions of remove operations.
        minval (int): The minimum value to be added.
        maxval (int): The maximum value to be added.

    Raises:
        AssertionError: Test failed.
    """

    binary_heap = []
    fibonacci_heap = fibonacciheap.Heap()
    nodes = set()
    removed = set()
    for i in range(size):
        num = randrange(minval, maxval + 1)
        heappush(binary_heap, (num, i))
        nodes.add((fibonacci_heap.add(num), i))
    for i in range(rep):
        rem = choice(tuple(nodes))
        nodes.remove(rem)
        fibonacci_heap.remove(rem[0])
        removed.add(rem[1])
        assert fibonacci_heap.size == size - i - 1, "Failed remove node: size mismatch"
    while binary_heap:
        exp = heappop(binary_heap)
        while binary_heap and exp[1] in removed:
            exp = heappop(binary_heap)
        if not exp[1] in removed:
            act = fibonacci_heap.pop()
            assert exp[0] == act.key, "Failed removal test: value mismatch"
    assert fibonacci_heap.minroot == None, "Failed removal test: heap not empty"


def decrease_test(
    size: int = 1000, rep: int = 10000, minval: int = MIN_VAL, maxval: int = MAX_VAL
) -> None:
    """Tests the decrease key operation.

    Args:
        size (int): The size of the test heap. Must be greater than 0.
        rep (int): The repetitions of decrease key operations.
        minval (int): The minimum value to be added.
        maxval (int): The maximum value to be added.

    Raises:
        AssertionError: Test failed.
    """

    binary_heap = []
    fibonacci_heap = fibonacciheap.Heap()
    nodes = []
    arr = []
    for i in range(size):
        num = randrange(minval, maxval + 1)
        heappush(binary_heap, (num, i))
        nodes.append(fibonacci_heap.add(num))
        arr.append(num)
    for _ in range(rep):
        i = randrange(size)
        node = nodes[i]
        key = randrange(minval, node.key + 1)
        fibonacci_heap.decreasekey(node, key)
        heappush(binary_heap, (key, i))
        arr[i] = key
    while binary_heap:
        exp = heappop(binary_heap)
        while binary_heap and arr[exp[1]] != exp[0]:
            exp = heappop(binary_heap)
        if arr[exp[1]] == exp[0]:
            arr[exp[1]] = -1
            act = fibonacci_heap.pop()
            assert exp[0] == act.key, "Failed decrease key test: value mismatch"
    assert fibonacci_heap.minroot == None, "Failed decrease key test: heap not empty"


def heap_test(
    rep: int = 10000,
    addfreq: int = 1,
    popfreq: int = 1,
    minval: int = MIN_VAL,
    maxval: int = MAX_VAL,
) -> None:
    """Tests add and pop operations.

    Args:
        rep (int): The repetitions of add/pop operations.
        addfreq (int): The weighted frequency of add operations.
        popfreq (int): The weighted frequency of pop operations.
        minval (int): The minimum value to be added.
        maxval (int): The maximum value to be added.

    Raises:
        AssertionError: Test failed.
    """

    totalfreq = addfreq + popfreq
    binary_heap = []
    fibonacci_heap = fibonacciheap.Heap()
    for _ in range(rep):
        add = randrange(totalfreq) < addfreq
        if add or len(binary_heap) == 0:
            num = randrange(minval, maxval + 1)
            heappush(binary_heap, num)
            fibonacci_heap.add(num)
            assert (
                binary_heap[0] == fibonacci_heap.minroot.key
            ), "Failed add operation: min value mismatch"
        else:
            a = heappop(binary_heap)
            b = fibonacci_heap.pop().key
            assert a == b, "Failed pop operation: value mismatch"
            if binary_heap:
                assert (
                    binary_heap[0] == fibonacci_heap.minroot.key
                ), "Failed pop operation: new min value mismatch"
            else:
                assert (
                    fibonacci_heap.minroot == None
                ), "Failed pop operation: heap not empty"
        assert (
            len(binary_heap) == fibonacci_heap.size
        ), "Failed add or pop operation: heap size mismatch"


if __name__ == "__main__":
    heap_test()
    decrease_test()
    remove_test()
    remove_test(size=1000, rep=1000)
    print("Fibonacci heap passed all tests")
