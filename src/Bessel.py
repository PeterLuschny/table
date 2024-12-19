from functools import cache
from _tabltypes import Table

"""Bessel triangle.

[0] [1]
[1] [0,      1]
[2] [0,      1,      1]
[3] [0,      3,      3,     1]
[4] [0,     15,     15,     6,     1]
[5] [0,    105,    105,    45,    10,    1]
[6] [0,    945,    945,   420,   105,   15,   1]
[7] [0,  10395,  10395,  4725,  1260,  210,  21,  1]
[8] [0, 135135, 135135, 62370, 17325, 3150, 378, 28, 1]
"""


@cache
def bessel(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]

    row = bessel(n - 1) + [1]
    for k in range(n - 1, 0, -1):
        row[k] = row[k - 1] + (2 * (n - 1) - k) * row[k]
    return row


Bessel = Table(
    bessel, 
    "Bessel", 
    ["A132062", "A001497", "A001498", "A122850"], 
    "A122848",
    r"2^{k - n} \binom{2n - 2k}{n - k} \binom{2n - k - 1}{k - 1} (n - k)!" 
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Bessel)
