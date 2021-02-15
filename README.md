# Heap Experiments

This is a work in progress to test the performance of different heap structures against each other.

Initial testing suggests that binary heaps are really good. With enough decrease key operations and a large enough heap, pairing and Fibonacci heaps gain parity; however, even on very dense small to mid sized graphs, binary heaps have a slight edge and linear search outperforms all heap structures. Pairing heaps are consistently better than Fibonacci heaps.

## Heaps included

1. Binary
2. Fibonacci
3. Pairing

## Tests included

1. Dijkstra's Single Source Shortest Path
2. Sequential heap operations

## Usage

1. Requires Python 3.9, [website](https://www.python.org)
2. Run `heap-experiments/app/main.py`

Linux/Mac

```zsh
cd ./heap-experiments
chmod 755 ./app/main.py  # give permission for the script to run
./app/main.py
```

Older versions of Python 3 do not support some of the type hinting used; removing type hinting should make the code compatible with all versions of Python 3.

Check out the wiki to see all commands.

## About

### Binary Heap

The binary heap used is an implicit binary heap from Python's [heap queue module](https://docs.python.org/3/library/heapq.html).

### Pairing Heap

The following sources were very helpful to make my pairing heap.

1. [The Pairing Heap: A New Form of Self-Adjusting Heap](http://www.cs.cmu.edu/afs/cs.cmu.edu/user/sleator/www/papers/pairing-heaps.pdf)
2. [COS 423 Lecture 6, Robert E. Tarjan](https://www.cs.princeton.edu/courses/archive/spr11/cos423/Lectures/Heaps.pdf)

### Fibonacci Heap

Largely copied from _Introduction to Algorithms_ by Cormen et al., 2009.

## Future

1. Redo these tests in C++
2. Test more algorithms and graph classes
3. Test more heaps/priority queues
