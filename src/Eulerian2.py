from functools import cache
from _tabltypes import Table

"""Eulerian2 triangle.

[0] 1;
[1] 0, 1;
[2] 0, 1,   2;
[3] 0, 1,   8,     6;
[4] 0, 1,  22,    58,     24;
[5] 0, 1,  52,   328,    444,    120;
[6] 0, 1, 114,  1452,   4400,   3708,    720;
[7] 0, 1, 240,  5610,  32120,  58140,  33984,  5040;
[8] 0, 1, 494, 19950, 195800, 644020, 785304, 341136, 40320;
"""


@cache
def eulerian2(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]

    row = eulerian2(n - 1) + [0]
    for k in range(n, 1, -1):
        row[k] = (2 * n - k) * row[k - 1] + k * row[k]
    return row


Eulerian2 = Table(
    eulerian2,
    "Eulerian2",
    ["A340556", "A201637", "A008517", "A112007", "A163936"],
    "A000000",
    r"%%",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Eulerian2)

# See also http://luschny.de/math/oeis/A340556.html
