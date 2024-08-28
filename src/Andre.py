from functools import cache
from Binomial import Binomial
from _tabltypes import Table


"""Andre numbers (version A375555).
  [0]  1;
  [1]  1, 1;
  [2]  1, 1,    1;
  [3]  1, 1,    2,    1;
  [4]  1, 1,    5,    3,   1;
  [5]  1, 1,   16,    9,   4,   1;
  [6]  1, 1,   61,   19,  14,   5,  1;
  [7]  1, 1,  272,   99,  34,  20,  6,  1;
  [8]  1, 1, 1385,  477,  69,  55, 27,  7, 1;
  [9]  1, 1, 7936, 1513, 496, 125, 83, 35, 8, 1;
"""

# TODO Give a row based recurrence for this.
@cache
def _andre(n: int, k: int) -> int:
    if k == 0 or n == 0: return 1 
    return -sum(Binomial.val(k, j) * _andre(n, j) for j in range(0, k, n)) 

@cache
def andre(n: int) -> list[int]:
    return [abs(_andre(k, n)) for k in range(n + 1)]


Andre = Table(andre, "Andre", ["A375555", "A181937"], True)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Andre)
