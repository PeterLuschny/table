from functools import cache
from _tabltypes import Table

"""Compositions of n with exact k parts.
[0]  1;
[1]  0,  1;
[2]  0,  1,  1;
[3]  0,  1,  2,   1;
[4]  0,  1,  4,   2,   1;
[5]  0,  1,  7,   5,   2,  1;
[6]  0,  1, 12,  11,   5,  2,  1;
[7]  0,  1, 20,  23,  12,  5,  2,  1;
[8]  0,  1, 33,  47,  27, 12,  5,  2, 1;
[9]  0,  1, 54,  94,  59, 28, 12,  5, 2, 1;
"""


@cache
def _composition(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    return (
        2 * _composition(n - 1, k)
        + _composition(n - 1, k - 1)
        - 2 * _composition(n - 2, k - 1)
        + _composition(n - k - 1, k - 1)
        - _composition(n - k - 2, k)
    )


@cache
def composition(n: int) -> list[int]:
    return [_composition(n - 1, k - 1) for k in range(n + 1)]


Composition = Table(composition, "Composition", ["A048004"], True)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Composition)
