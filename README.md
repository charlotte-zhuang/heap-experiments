# Heap Experiments

This is a work in progress to test the performance of different heap structures against each other.

Initial testing suggests that binary heaps are really good. With enough decrease key operations and a large enough heap, pairing and Fibonacci heaps gain parity; however, even on very dense small to mid sized graphs, binary heaps have a slight edge. Run times on my laptop approached one minute before pairing and Fibonacci heaps saw an advantage. Between those two, there doesn't seem to be a great difference in run time.

## Usage

Check out [the wiki](https://github.com/charlotte-zhuang/heap-experiments/wiki).

## Heaps included

1. Binary
2. Fibonacci
3. Pairing

## Tests included

1. Dijkstra's Single Source Shortest Path
2. Sequential heap operations

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
