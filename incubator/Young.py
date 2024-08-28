from functools import cache
from _tabltypes import Table

""" 
[0]  1
[0]  0,  1
[0]  0,  1,  1
[0]  0,  1,  2,   1
[0]  0,  1,  5,   3,   1
[0]  0,  1,  9,  11,   4,   1
[0]  0,  1, 19,  31,  19,   5,  1
[0]  0,  1, 34,  92,  69,  29,  6, 1
[0]  0,  1, 69, 253, 265, 127, 41, 7, 1
"""

@cache
def young(n: int) -> list[int]:
    return [n] * (n+1)


Young = Table(
    young,
    "Young",
    ["A047884"],
    True )


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Young)
