from functools import cache
from _tabltypes import Table

"""FiboLucas polynomials, m = 2.
  [ 0] [1]
  [ 1] [1, 2]
  [ 2] [1, 2, 1]
  [ 3] [1, 2, 2, 2]
  [ 4] [1, 2, 3, 4, 1]
  [ 5] [1, 2, 4, 6, 3, 2]
  [ 6] [1, 2, 5, 8, 6, 6, 1]
  [ 7] [1, 2, 6, 10, 10, 12, 4, 2]
  [ 8] [1, 2, 7, 12, 15, 20, 10, 8, 1]
  [ 9] [1, 2, 8, 14, 21, 30, 20, 20, 5, 2]
  [10] [1, 2, 9, 16, 28, 42, 35, 40, 15, 10, 1]

# @cache
def T(n: int, k: int) -> int:
    if k > n: return 0
    if k < 2: return k + 1
    return T(n - 1, k) + T(n - 2, k - 2)
"""


@cache
def fibolucas(n: int) -> list[int]:
    if n == 0: return [1]
    if n == 1: return [1, 2]
    if n == 2: return [1, 2, 1]

    rowA = fibolucas(n - 2)
    row  = fibolucas(n - 1) + [1 + n % 2]
    row[2] += 1

    for k in range(3, n):
        row[k] += rowA[k - 2]

    return row


FiboLucas = Table(
    fibolucas,
    "FiboLucas",
    ["A374439"],
    "",
    r"2^{k'} \, \binom{n - k' - (k - k') / 2}{(k - k') / 2} \text{ where } k' = k \text{ mod } 2",
)


if __name__ == "__main__":
    from _tablutils import PreView
    PreView(FiboLucas)
