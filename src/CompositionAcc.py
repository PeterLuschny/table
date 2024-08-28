from functools import cache
from itertools import accumulate
from _tabltypes import Table
from Composition import composition

"""Compositions of n into at most k parts.

[0] 1;
[1] 0, 1;
[2] 0, 1,  2;
[3] 0, 1,  3,   4;
[4] 0, 1,  5,   7,   8;
[5] 0, 1,  8,  13,  15,  16;
[6] 0, 1, 13,  24,  29,  31,  32;
[7] 0, 1, 21,  44,  56,  61,  63,  64;
[8] 0, 1, 34,  81, 108, 120, 125, 127, 128;
[9] 0, 1, 55, 149, 208, 236, 248, 253, 255, 256;

"""

@cache
def compoacc(n: int) -> list[int]:
    return list(accumulate(composition(n))) 


CompoAcc = Table(compoacc, "CompositionAcc", ["A126198"], False)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(CompoAcc)
