from functools import cache
from _tabltypes import Table

"""Stirling cycle B-type.

[0]      1;
[1]      1,      1;
[2]      3,      4,      1;
[3]     15,     23,      9,     1;
[4]    105,    176,     86,    16,     1;
[5]    945,   1689,    950,   230,    25,   1;
[6]  10395,  19524,  12139,  3480,   505,  36,  1;
[7] 135135, 264207, 177331, 57379, 10045, 973, 49, 1;
"""


@cache
def stirlingcycleb(n: int) -> list[int]:
    if n == 0:
        return [1]

    row = stirlingcycleb(n - 1) + [1]

    m = 2 * n - 1
    for k in range(n - 1, 0, -1):
        row[k] = m * row[k] + row[k - 1]
    row[0] *= m

    return row


StirlingCycleB = Table(
    stirlingcycleb,
    "StirlingCycB",
    ["A028338", "A039757", "A039758", "A109692"],
    "A000000",
    r"\sum_{i=k}^{n} (-2)^{n-i} \binom{i}{k} {n \brack i}",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(StirlingCycleB)
