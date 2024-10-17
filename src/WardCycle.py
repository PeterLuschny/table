from functools import cache
from _tabltypes import Table

"""Ward cycle numbers.


[1]
[0,    1]
[0,    2,     3]
[0,    6,    20,     15]
[0,   24,   130,    210,    105]
[0,  120,   924,   2380,   2520,    945]
[0,  720,  7308,  26432,  44100,  34650,  10395]
[0, 5040, 64224, 303660, 705320, 866250, 540540, 135135]
"""


@cache
def wardcycle(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]

    row = wardcycle(n - 1) + [0]
    for k in range(n, 0, -1):
        row[k] = (n + k - 1) * (row[k - 1] + row[k])

    return row


WardCycle = Table(wardcycle, "WardCycle", 
["A269940", "A111999", "A259456"], False, 
r"\sum_{m=0}^{k} (-1)^{m+k} \binom{n+k}{n+m} { n + m \brack m}")


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(WardCycle)
