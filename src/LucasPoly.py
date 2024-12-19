from functools import cache
from _tabltypes import Table

"""Lucas polynomials (unsigned coefficients).
  [ 0]  1;
  [ 1]  1,  0;
  [ 2]  1,  1,  1;
  [ 3]  1,  2,  1,  0;
  [ 4]  1,  3,  1,  1,  1;
  [ 5]  1,  4,  1,  3,  2,  0;
  [ 6]  1,  5,  1,  6,  3,  1,  1;
  [ 7]  1,  6,  1, 10,  4,  4,  3,  0;
  [ 8]  1,  7,  1, 15,  5, 10,  6,  1,  1;
  [ 9]  1,  8,  1, 21,  6, 20, 10,  5,  4,  0;
  [10]  1,  9,  1, 28,  7, 35, 15, 15, 10,  1, 1;
"""


@cache
def lucaspoly(n: int) -> list[int]:
    if n == 0: return [1]
    if n == 1: return [1, 0]
    if n == 2: return [1, 1, 1]

    rowA = lucaspoly(n - 2)
    row  = lucaspoly(n - 1) + [(n + 1) % 2]
    row[1] += 1

    for k in range(3, n):
        row[k] += rowA[k - 2]

    return row


LucasPoly = Table(
    lucaspoly, 
    "LucasPoly", 
    ["A374440"], 
    "", 
    r"T_{n - 1, k} + T_{n - 2, k - 2}"
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(LucasPoly)
