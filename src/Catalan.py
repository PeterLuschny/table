from functools import cache
from _tabltypes import Table

"""Balott Catalan triangle.

[0] 1;
[1] 0,    1;
[2] 0,    2,    1;
[3] 0,    5,    4,    1;
[4] 0,   14,   14,    6,    1;
[5] 0,   42,   48,   27,    8,    1;
[6] 0,  132,  165,  110,   44,   10,   1;
[7] 0,  429,  572,  429,  208,   65,  12,   1;
[8] 0, 1430, 2002, 1638,  910,  350,  90,  14,  1;
[9] 0, 4862, 7072, 6188, 3808, 1700, 544, 119, 16, 1;
"""


@cache
def catalan(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]

    pow = catalan(n - 1) + [0]
    row = pow.copy()
    for k in range(n - 1, 0, -1):
        row[k] = pow[k - 1] + 2 * pow[k] + pow[k + 1]
    row[n] = 1

    return row


Catalan = Table(
    catalan,
    "Catalan",
    ["A128899", "A039598"],
    "A128908",
    r"\sum_{i=1}^{n-k+1} \text{Catalan}(i) T_{k-1, n-i}",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Catalan)
