from functools import cache
from _tabltypes import Table

"""Stirling set B-type.


[0]     1;
[1]     1,     1;
[2]     3,     4,     1;
[3]    11,    19,     9,     1;
[4]    49,   104,    70,    16,    1;
[5]   257,   641,   550,   190,   25,   1;
[6]  1539,  4380,  4531,  2080,  425,  36,  1;
[7] 10299, 32803, 39515, 22491, 6265, 833, 49, 1;
"""


@cache
def stirlingsetb(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1, 1]

    pow = stirlingsetb(n - 1)
    row = stirlingsetb(n - 1) + [1]

    row[0] += 2 * row[1]

    for k in range(1, n - 1):
        row[k] = 2 * (k + 1) * pow[k + 1] + (2 * k + 1) * pow[k] + pow[k - 1]

    row[n - 1] = (2 * n - 1) * pow[n - 1] + pow[n - 2]
    return row


StirlingSetB = Table(
    stirlingsetb,
    "StirlingSetB",
    ["A154602"],
    "A000000",
    r"\sum_{j=k}^{n} 2^{n-j} \binom{j}{k} {n \brace j}",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(StirlingSetB)
