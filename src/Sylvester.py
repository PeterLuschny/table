from functools import cache
from Binomial import Binomial
from StirlingCycle import StirlingCycle
from _tabltypes import Table

"""Sylvester polynomials.

[0] 1;
[1] 0,   2;
[2] 0,   1,    4;
[3] 0,   2,    6,    8;
[4] 0,   6,   19,   24,   16;
[5] 0,  24,   80,  110,   80,   32;
[6] 0, 120,  418,  615,  500,  240,  64;
[7] 0, 720, 2604, 4046, 3570, 1960, 672, 128;
"""


@cache
def sylvester(n: int) -> list[int]:
    def s(n: int, k: int) -> int:
        return sum(Binomial.val(n, k - j) * StirlingCycle.val(n - k + j, j) 
               for j in range(k + 1) )
    return [s(n, k) for k in range(n + 1)]


Sylvester = Table(sylvester, "Sylvester", ["A341101"], False)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Sylvester)
