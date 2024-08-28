from functools import cache
from _tabltypes import Table

"""Leibniz's Scheme, multiplication table read by antidiagonals.

[0]  0
[1]  0   1
[2]  0   2    2
[3]  0   3    4   3
[4]  0   4    6   6    4
[5]  0   5    8   9    8    5
[6]  0   6   10  12   12   10    6
[7]  0   7   12  15   16   15   12    7
[8]  0   8   14  18   20   20   18   14   8
[9]  0   9   16  21   24   25   24   21  16  9
"""


@cache
def leibnizscheme(n: int) -> list[int]:
    if n == 0: return [0]
    L = leibnizscheme(n - 1)
    return [L[k] + k for k in range(n)] + [n]

LeibnizScheme = Table(leibnizscheme, "LeibnizScheme", ["A003991"]) 


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(LeibnizScheme)
