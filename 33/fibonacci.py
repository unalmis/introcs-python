# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 fibonacci.py 40
# ------------------------------------------------------------------------------


def fib_0(n: int) -> int:
    # iterative O(n) time, O(1) space
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b  # simultaneous assignment with tuple (un)packing
    return a


def fib_1(n: int, a: int = 0, b: int = 1) -> int:
    # tail recursive O(n) time, O(1) space
    if n <= 0:
        return a
    return fib_1(n - 1, b, a + b)


def fib_2(n: int) -> int:
    # naive implementation, exponential time
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fib_2(n - 1) + fib_2(n - 2)


def main():
    # unit tests
    import sys
    import time

    query = int(sys.argv[1])
    for f in (fib_0, fib_1, fib_2):
        start_time = time.time()
        result = f(query)
        elapsed_time = time.time() - start_time
        print(result, elapsed_time)


if __name__ == "__main__":
    main()
