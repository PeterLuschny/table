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

# The implementation goes back to:
# https://codegolf.stackexchange.com/questions/275413/
# and relies on work of 
# Jonathan Allan, https://codegolf.stackexchange.com/a/275420
# and user gsitcia.


@cache
def divisors(n: int) -> list[int]:
    return [d for d in range(n, 0, -1) if n % d == 0]


@cache
def _polyatree_vh(vertices: int, height: int) -> int:
    return sum(d * _polyatree_vl(d, height) for d in divisors(vertices))


@cache
def _polyatree_vl(vertices: int, max_level: int) -> int:
    """
    Args:
        nodes, the number of vertices.
        Max level of a vertex. The level of a vertex is 
        the number of vertices in the path from the root 
        to the vertex, the level of the root is 1.

    Returns:
        number of rooted trees with n vertices where the
        level of a vertex is bounded by max_level.
    """
    if vertices == 1:
        return int(max_level > 0)
    if max_level == 0:
        return 0

    height = max_level - 1
    return sum(
        _polyatree_vl(i, max_level) * _polyatree_vh(vertices - i, height)
        for i in range(1, vertices)
    ) // (vertices - 1)


@cache
def polyatreeacc(n: int) -> list[int]:
    return [_polyatree_vl(n, k) for k in range(n + 1)]


PolyaTreeAcc = Table(polyatreeacc, "PolyaTreeAcc", ["A375467"])


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(PolyaTreeAcc)