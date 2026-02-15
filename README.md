# 2D Convex Hull Project

This project implements three algorithms to compute the convex hull of various 2D point distributions.

## Algorithms Implemented
1. **Sweeping Algorithm** - $O(n \log n)$
2. **Output-Sensitive Algorithm** - $O(n \log h)$
3. **Gift Wrapping Algorithm** - $O(nh)$

## Prerequisites

You need Python 3 and the following libraries:

```bash
pip install matplotlib numpy
```

## Files Description

* **`main.py`**: Runs a visual demonstration of the algorithms on different datasets.
* **`hull.py`**: Contains the class implementations of the algorithms (`SweepingHull`, `OSHull`, `GiftWrappingHull`).
* **`datasets.py`**: Generates the 4 required point distributions (A, B, C, D).
* **`tests.py`**: Unit tests to verify geometric primitives and hull correctness.
* **`complexity.py`**: Benchmarking script to measure and plot time complexity.

## How to Run

### 1. Visual Demonstration
To see the datasets and the resulting hulls:
```bash
python main.py
```

*Note: You must close the plot window to proceed to the next example.*

### 2. Unit Tests
To verify that the algorithms are working correctly:

```bash
python tests.py
```

*Note: You must close the plot window to proceed to the next example.*

### 2. Unit Tests
To verify that the algorithms are working correctly:

```bash
python tests.py
```

### 3. Complexity Benchmark

To generate the time complexity graph (Time vs. Number of Points):

```bash
python complexity.py
```
