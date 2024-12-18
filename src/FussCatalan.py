from functools import cache
from itertools import accumulate
from _tabltypes import Table

"""Fuss-Catalan triangle.

[0] [1]
[1] [0, 1]
[2] [0, 1, 2]
[3] [0, 1, 3,  5]
[4] [0, 1, 4,  9, 14]
[5] [0, 1, 5, 14, 28,  42]
[6] [0, 1, 6, 20, 48,  90, 132]
[7] [0, 1, 7, 27, 75, 165, 297, 429]
"""


@cache
def fusscatalan(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]

    row = fusscatalan(n - 1) + [fusscatalan(n - 1)[n - 1]]
    return list(accumulate(row))


FussCatalan = Table(
    fusscatalan,
    "FussCatalan",
    ["A355173", "A030237", "A054445"],
    "",
    r"is(k=0) \, ? \, 0^n : \frac{(n - k + 2) (n + k - 1)!}{(n + 1)! \, (k - 1)!}",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(FussCatalan)
