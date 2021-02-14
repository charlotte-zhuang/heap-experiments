# Heaps

This is a work in progress to test the performance of different heap structures against each other.

Initial testing suggests that binary heaps are really good. With enough decrease key operations, pairing and Fibonacci heaps gain parity; however even on very dense graphs, binary heaps outperform. Pairing heaps are consistently better than Fibonacci heaps.

## Heaps included

1. Binary
2. Fibonacci
3. Pairing

## Usage

1. Requires Python 3.9, [website](https://www.python.org)
2. Run `heap/app/main.py`

Linux/Mac

```zsh
cd ./heap
chmod 755 ./app/start.py  # give permission for the script to run
./app/start.py
```

I'm not sure how to do this on Windows. Older versions of Python 3 do not support some of the type hinting used.

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

## Documentation

The Python scripts have a lot of comments that hopefully explain what's going on. Here's the project structure and some notable files to get started (it's a mess, can someone show me how to make a Python app?).

- `app/` Contains the heap CLI runtime tester
  - `start.py` Starts the CLI app
- `config/` Contains config files used to generate tests
  - `graph-example.txt` An example config file for making a test graph.
  - `heap-example.txt` An example config file for heap operation tests.
- `data/` Contains generated test data
- `util/` Contains code for the heaps, graph generators, and algorithms
- `tests/` Contains some automated tests for functionality

## Future

1. Redo these tests in C++
2. Test more algorithms and graph classes
3. Test more heaps/priority queues
