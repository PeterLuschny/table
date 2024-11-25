from functools import cache
from Tables import Table

"""
DoublePochhammer

[0] 1;
[1] 0,      1;
[2] 0,      2,      1;
[3] 0,      8,      6,      1;
[4] 0,     48,     44,     12,      1;
[5] 0,    384,    400,    140,     20,     1;
[6] 0,   3840,   4384,   1800,    340,    30,    1;
[7] 0,  46080,  56448,  25984,   5880,   700,   42,  1;
[8] 0, 645120, 836352, 420224, 108304, 15680, 1288, 56, 1;

"""

@cache
def doublepochhammer(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]

    row = doublepochhammer(n - 1) + [1]
    for k in range(n - 1, 0, -1):
        row[k] = row[k - 1] + 2 * (n - 1) * row[k]
    return row


DoublePochhammer = Table(doublepochhammer, "DoublePochhammer", 
['A039683'], True,
r"[x^k]\, x(x-2)(x-4)...(x-2n+2)")


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(DoublePochhammer)  # type: ignore
