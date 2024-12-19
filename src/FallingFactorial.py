from functools import cache
from _tabltypes import Table

"""Falling factorial, number of permutations of n things k at a time.

[0]  1
[1]  1,  1
[2]  1,  2,  2
[3]  1,  3,  6,   6
[4]  1,  4, 12,  24,   24
[5]  1,  5, 20,  60,  120,  120
[6]  1,  6, 30, 120,  360,  720,     720
[7]  1,  7, 42, 210,  840,  2520,   5040,   5040;
[8]  1,  8, 56, 336, 1680,  6720,  20160,  40320,   40320;
[9]  1,  9, 72, 504, 3024, 15120,  60480, 181440,  362880,  362880;
"""


@cache
def fallingfactorial(n: int) -> list[int]:
    if n == 0:
        return [1]

    r = fallingfactorial(n - 1)
    row = [n * r[k] for k in range(-1, n)]
    row[0] = 1
    return row


FallingFactorial = Table(
    fallingfactorial,
    "FallingFact",
    ["A008279", "A068424", "A094587", "A173333", "A181511"],
    "",
    r"n! / (n - k)!",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(FallingFactorial)
