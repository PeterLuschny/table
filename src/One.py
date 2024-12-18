from functools import cache
from _tabltypes import Table

"""Uno, the all 1's triangle.

[0]  1
[1]  1,  1
[2]  1,  1,  1
[3]  1,  1,  1,  1
[4]  1,  1,  1,  1,  1
[5]  1,  1,  1,  1,  1,  1
[6]  1,  1,  1,  1,  1,  1,  1
[7]  1,  1,  1,  1,  1,  1,  1,  1
[8]  1,  1,  1,  1,  1,  1,  1,  1,  1
"""


@cache
def one(n: int) -> list[int]:
    if n == 0:
        return [1]
    return one(n - 1) + [1]


One = Table(
    one, 
    "One", 
    ["A000012", "A008836", "A014077"], 
    "A000000",
    r"1"
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(One)
