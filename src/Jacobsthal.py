from functools import cache
from _tabltypes import Table


"""Jacobsthal polynomials.

  [0]   1;
  [1]   1,   1;
  [2]   1,   2,    1;
  [3]   3,   5,    3,    1;
  [4]   5,  12,   10,    4,   1;
  [5]  11,  27,   28,   16,   5,   1;
  [6]  21,  62,   75,   52,  23,   6,   1;
  [7]  43, 137,  193,  159,  85,  31,   7,  1;
  [8]  85, 304,  480,  456, 290, 128,  40,  8, 1;
  [9] 171, 663, 1170, 1254, 916, 480, 182, 50, 9, 1;
"""


@cache
def jacobsthal(n: int) -> list[int]:
    if n == 0: return [1]
    if n == 1: return [1, 1]
    if n == 2: return [1, 2, 1]

    Jn1 = jacobsthal(n - 1)
    Jn2 = jacobsthal(n - 2) + [0]
    row = [1] * (n + 1)
    for k in range(1, n):
        row[k] = Jn1[k-1] + Jn1[k] + 2 * Jn2[k]
    row[0] = Jn1[0] + 2 * Jn2[0]
    return row


Jacobsthal = Table(
    jacobsthal,
    "Jacobsthal",
    ["A322942"],
    "A000000",
    r"[x^k]\ ((x+1)\, \mathrm{J}(n-1, x) + 2\, \mathrm{J}(n-2, x))",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Jacobsthal)
