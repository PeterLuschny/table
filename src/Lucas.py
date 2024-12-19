from functools import cache
from _tabltypes import Table

"""Lucas triangle.
  [0] [2]
  [1] [1, 2]
  [2] [1, 3, 2]
  [3] [1, 4, 5, 2]
  [4] [1, 5, 9, 7, 2]
  [5] [1, 6, 14, 16, 9, 2]
  [6] [1, 7, 20, 30, 25, 11, 2]
  [7] [1, 8, 27, 50, 55, 36, 13, 2]
  [8] [1, 9, 35, 77, 105, 91, 49, 15, 2]
  [9] [1, 10, 44, 112, 182, 196, 140, 64, 17, 2]
"""


@cache
def lucas(n: int) -> list[int]:
    if n == 0: return [2]
    if n == 1: return [1, 2]

    row = lucas(n - 1) + [0]
    for k in range(n, 0, -1):
        row[k] += row[k - 1]
    return row


Lucas = Table(
    lucas, 
    "Lucas", 
    ["A029635", "A029653"], 
    "", 
    r"\binom{n}{k} + \binom{n-1}{k-1}"
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Lucas)
