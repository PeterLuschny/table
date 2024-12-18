from functools import cache
from _tabltypes import Table

"""Harmonic polynomials (coefficients).

[0] 1
[1] 0,     1
[2] 0,     2,     1
[3] 0,     6,     4,     1
[4] 0,    24,    18,     7,    1
[5] 0,   120,    96,    46,   11,    1
[6] 0,   720,   600,   326,  101,   16,   1
[7] 0,  5040,  4320,  2556,  932,  197,  22,  1
"""


@cache
def harmonic(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]

    row = harmonic(n - 1) + [1]
    sav = row[1]

    for k in range(n - 1, 0, -1):
        row[k] = (n - 1) * row[k] + row[k - 1]
    row[1] += sav

    return row


Harmonic = Table(
    harmonic,
    "Harmonic",
    ["A358694", "A109822"],
    "A000000",
    r"T_{n - 1, k - 1} + (n - 1) T_{n - 1, k}; \ T_{n, 1} = n!",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Harmonic)
