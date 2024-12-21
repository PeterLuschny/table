from functools import cache
from _tabltypes import Table

"""Binomial Diff Pell triangle


[0]    1;
[1]    1,    1;
[2]    3,    2,    1;
[3]    7,    9,    3,    1;
[4]   17,   28,   18,    4,    1;
[5]   41,   85,   70,   30,    5,    1;
[6]   99,  246,  255,  140,   45,    6,   1;
[7]  239,  693,  861,  595,  245,   63,   7,   1;
[8]  577, 1912, 2772, 2296, 1190,  392,  84,   8, 1;
[9] 1393, 5193, 8604, 8316, 5166, 2142, 588, 108, 9, 1;
"""


@cache
def binomialdiffpell(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1, 1]

    arow = binomialdiffpell(n - 1)
    row = arow + [1]
    for k in range(1, n):
        row[k] = (arow[k - 1] * n) // k
    row[0] = 2 * arow[0] + binomialdiffpell(n - 2)[0]

    return row


BinomialDiffPell = Table(
    binomialdiffpell,
    "BinomialDiffPell",
    ["A367564"],
    "A000000",
    r"\frac{1}{2} \binom{n}{k} ((1-\sqrt{2})^{n-k} + (1+\sqrt{2})^{n-k})"
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(BinomialDiffPell)
