from functools import cache
from Binomial import binomial
from _tabltypes import Table


"""Parades triangle.
  [0] 1;
  [1] 0, 0;
  [2] 0, 1,  0;
  [3] 0, 1,  1,   0;
  [4] 0, 1,  5,   1,   0;
  [5] 0, 1, 13,  13,   1,  0;
  [6] 0, 1, 29,  73,  29,  1, 0;
  [7] 0, 1, 61, 301, 301, 61, 1, 0;
"""


@cache
def A(n: int, k: int) -> int:
    if n == 0:
        return int(k == 0)
    if k > n:
        n, k = k, n

    b = binomial(k + 1)
    return k * A(n - 1, k) + sum(b[j + 1] * A(n - 1, k - j)
                             for j in range(1, k + 1))


@cache
def parades(n: int) -> list[int]:
    return [A(n - k, k) for k in range(n + 1)]


Parades = Table(parades, "Parades", 
["A371761", "A272644"], False,
r"")


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Parades)
