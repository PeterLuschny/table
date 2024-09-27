from functools import cache
from _tabltypes import Table

"""
    The Eytzinger order arranges elements of an array
    so that a binary search can be performed starting with
    index k = 1 and at a given k step to 2*k or 2*k + 1,
    depending on whether the target is smaller or larger
    than the element at k.

    Args: n, length of array
    Returns: The given array in Eytzinger order.

    Variant 1, A375825, mostly used when (1, 1)-based.
    [0] [0]
    [1] [0, 1]
    [2] [0, 2, 1]
    [3] [0, 2, 1, 3]
    [4] [0, 3, 2, 4, 1]
    [5] [0, 4, 2, 5, 1, 3]
    [6] [0, 4, 2, 6, 1, 3, 5]
    [7] [0, 4, 2, 6, 1, 3, 5, 7]
    [8] [0, 5, 3, 7, 2, 4, 6, 8, 1]
    [9] [0, 6, 4, 8, 2, 5, 7, 9, 1, 3]

    Variant 2, we use this one:
    [0] [0]
    [1] [1, 0]
    [2] [1, 0, 2]
    [3] [2, 1, 3, 0]
    [4] [3, 1, 4, 0, 2]
    [5] [3, 1, 5, 0, 2, 4]
    [6] [3, 1, 5, 0, 2, 4, 6]
    [7] [4, 2, 6, 1, 3, 5, 7, 0]
    [8] [5, 3, 7, 1, 4, 6, 8, 0, 2]
    [9] [6, 3, 8, 1, 5, 7, 9, 0, 2, 4]
"""


# $cache  #  Variant 1, not used here!
def Xeytzingerorder(n: int) -> list[int]:
    row = [0] * (n + 1)

    def e_rec(k: int, i: int) -> int:
        if k <= n:
            i = e_rec(2 * k, i)
            row[k] = i
            i = e_rec(2 * k + 1, i + 1)
        return i
    e_rec(1, 1)
    return row


@cache
def eytzingerorder(n: int) -> list[int]:
    row = [0] * (n + 1)
    def e_rec(k: int, i: int) -> int:
        if k <= n + 1:
            i = e_rec(2 * k, i)
            row[k - 1] = i
            i = e_rec(2 * k + 1, i + 1)
        return i
    e_rec(1, 0)
    return row


EytzingerOrder = Table(eytzingerorder, "EytzingerOrder", ["A375825"])


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(EytzingerOrder)
