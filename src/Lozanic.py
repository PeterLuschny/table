from functools import cache
from _tabltypes import Table
from Binomial import binomial

"""Lozanic numbers.


[0]  1;
[1]  1,  1;
[2]  1,  1,  1;
[3]  1,  2,  2,  1;
[4]  1,  2,  4,  2,  1;
[5]  1,  3,  6,  6,  3,  1;
[6]  1,  3,  9, 10,  9,  3,  1;
[7]  1,  4, 12, 19, 19, 12,  4,  1;
[8]  1,  4, 16, 28, 38, 28, 16,  4,  1;
[9]  1,  5, 20, 44, 66, 66, 44, 20,  5,  1;
"""


@cache
def lozanic(n: int) -> list[int]:
    if n == 0:
        return [1]

    row = [1] + lozanic(n - 1)
    for k in range(1, n):
        row[k] += row[k + 1]

    if n % 2 != 0:
        return row

    b = binomial(n // 2 - 1)
    for k in range(1, n, 2):
        row[k] -= b[(k - 1) // 2]

    return row


Lozanic = Table(
    lozanic,
    "Lozanic",
    ["A034851"],
    "A000000",
    r"\frac{1}{2} \left(\binom{n}{k}+\binom{n \text{ mod } 2}{k \text{ mod } 2} \binom{n \text{ div } 2}{k \text{ div } 2} \right)",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Lozanic)
