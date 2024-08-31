from functools import cache
from _tabltypes import Table


"""Polya Trees
[0] [0]
[1] [0, 1]
[2] [0, 0, 1]
[3] [0, 0, 1,  2]
[4] [0, 0, 1,  3,  4]
[5] [0, 0, 1,  5,  8,   9]
[6] [0, 0, 1,  7, 15,  19,  20]
[7] [0, 0, 1, 11, 29,  42,  47,  48]
[8] [0, 0, 1, 15, 53,  89, 108, 114, 115]
[9] [0, 0, 1, 22, 98, 191, 252, 278, 285, 286]
"""


@cache
def _polyatree(n: int, k: int) -> int:
    """
    Args:
        n, the number of vertices
        k, level of a vertex, the level of a vertex is 
        the number of vertices in the path from the root 
        to the vertex, the level of the root is 1.

    Returns:
        number of rooted trees with n vertices where the
        level of a vertex is bounded by k.
    """
    if k >  n: return _polyatree(n, n)
    if k <= 0: return 0
    if n == 1: return 0 if k == 0 else 1

    def W(n: int, k: int, u: int, w: int) -> int: 
       q, r = divmod(u, w)
       if r != 0: return 0
       return q * _polyatree(k, n) * _polyatree(q, n - 1)

    return sum(sum(W(k, i, n - i, j) 
           for i in range(1, n)) for j in range(1, n)) // (n - 1)


@cache
def polyatree(n: int) -> list[int]:
    return [_polyatree(n, k) for k in range(n + 1)]


PolyaTree = Table(polyatree, "PolyaTree", ["A375467"])


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(PolyaTree)