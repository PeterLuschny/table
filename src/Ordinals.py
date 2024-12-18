from functools import cache
from _tabltypes import Table

"""von Neumann ordinals (kind of).

[0] [0]
[1] [0,  1]
[2] [0,  1,  2]
[3] [0,  1,  2,  3]
[4] [0,  1,  2,  3,  4]
[5] [0,  1,  2,  3,  4,  5]
[6] [0,  1,  2,  3,  4,  5,  6]
[7] [0,  1,  2,  3,  4,  5,  6,  7]
"""


@cache
def ordinals(n: int) -> list[int]:
    if n == 0:
        return [0]
    return ordinals(n - 1) + [n]


Ordinals = Table(
    ordinals, 
    "Ordinals", 
    ["A002262", "A002260", "A004736", "A025581"], 
    "", 
    r"T(n,k) = k"
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Ordinals)
