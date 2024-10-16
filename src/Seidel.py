from _tabltypes import Table
from Entringer import entringer


"""Seidel boustrophedon:

[0] [ 1]
[1] [ 0,  1]
[2] [ 1,  1,   0]
[3] [ 0,  1,   2,   2]
[4] [ 5,  5,   4,   2,   0]
[5] [ 0,  5,  10,  14,  16,  16]
[6] [61, 61,  56,  46,  32,  16,   0]
[7] [ 0, 61, 122, 178, 224, 256, 272, 272]
"""

# #@


def seidel(n: int) -> list[int]:
    return entringer(n) if n % 2 else entringer(n)[::-1]


Seidel = Table(
    seidel, "Seidel", ["A008280", "A108040", "A236935", "A239005"], False
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Seidel)