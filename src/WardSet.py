from functools import cache
from _tabltypes import Table

"""Ward set numbers.


[0] [1]
[1] [0, 1]
[2] [0, 1,   3]
[3] [0, 1,  10,    15]
[4] [0, 1,  25,   105,    105]
[5] [0, 1,  56,   490,   1260,     945]
[6] [0, 1, 119,  1918,   9450,   17325,   10395]
[7] [0, 1, 246,  6825,  56980,  190575,  270270,  135135]
[8] [0, 1, 501, 22935, 302995, 1636635, 4099095, 4729725, 2027025]
"""


@cache
def wardset(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]

    row = wardset(n - 1) + [0]
    for k in range(n, 0, -1):
        row[k] = k * row[k] + (n + k - 1) * row[k - 1]

    return row


WardSet = Table(
    wardset,
    "WardSet",
    ["A269939", "A134991"],
    "",
    r"\sum_{m=0}^{k} (-1)^{m + k} \binom{n+k}{n+m} { n + m \brace m}",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(WardSet)
