from functools import cache
from _tabltypes import Table


"""n XOR k (or Nim-sum of n and k).

[0] 0;
[1] 1,  1;
[2] 2,  0,  2;
[3] 3,  3,  3,  3;
[4] 4,  2,  0,  2,  4;
[5] 5,  5,  1,  1,  5,  5;
[6] 6,  4,  6,  0,  6,  4,  6;
[7] 7,  7,  7,  7,  7,  7,  7,  7;
[8] 8,  6,  4,  6,  0,  6,  4,  6,  8;
[9] 9,  9,  5,  5,  1,  1,  5,  5,  9,  9;
"""


@cache
def nimsum(n: int) -> list[int]:
    return [k ^ (n - k) for k in range(n + 1)]


NimSum = Table(
    nimsum, 
    "NimSum", 
    ["A003987"], 
    "",
    r"%%"
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(NimSum)
