from functools import cache
from _tabltypes import Table

"""Falling factorial, number of permutations of n things k at a time.

[0]  1
[1]  1,  1
[2]  1,  2,  2
[3]  1,  3,  6,   6
[4]  1,  4, 12,  24,   24
[5]  1,  5, 20,  60,  120,  120
[6]  1,  6, 30, 120,  360,  720,  720
"""


@cache
def fallingfactorial(n: int) -> list[int]:
    if n == 0:
        return [1]

    r = fallingfactorial(n - 1)
    row = [n * r[k] for k in range(-1, n)]
    row[0] = 1
    return row


FallingFactorial = Table(fallingfactorial, "FallingFact",
["A008279", "A068424", "A094587", "A173333", "A181511"], False,
r"n! / (n - k)!" )


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(FallingFactorial)
