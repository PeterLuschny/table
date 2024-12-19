from functools import cache
from _tabltypes import Table

"""Stirling set numbers of second order.


[0] 1;
[1] 0, 0;
[2] 0, 1,   0;
[3] 0, 1,   0,    0;
[4] 0, 1,   3,    0,    0;
[5] 0, 1,  10,    0,    0,  0;
[6] 0, 1,  25,   15,    0,  0,  0;
[7] 0, 1,  56,  105,    0,  0,  0,  0;
[8] 0, 1, 119,  490,  105,  0,  0,  0,  0;
[9] 0, 1, 246, 1918, 1260,  0,  0,  0,  0,  0;
"""


@cache
def stirlingset2(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 0]

    rov = stirlingset2(n - 2)
    row = stirlingset2(n - 1) + [0]
    for k in range(1, n // 2 + 1):
        row[k] = (n - 1) * rov[k - 1] + k * row[k]

    return row


StirlingSet2 = Table(
    stirlingset2,
    "StirlingSet2",
    ["A358623", "A008299", "A137375"],
    "",
    r"\sum_{j=0}^{k} (-1)^{k-j} \binom{n}{k-j} {n-k+j \brace j}",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(StirlingSet2)
