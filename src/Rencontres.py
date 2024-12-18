from functools import cache
from _tabltypes import Table

"""Rencontres triangle.

[0]       1;
[1]       0,      1;
[2]       1,      0,     1;
[3]       2,      3,     0,     1;
[4]       9,      8,     6,     0,    1;
[5]      44,     45,    20,    10,    0,    1;
[6]     265,    264,   135,    40,   15,    0,   1;
[7]    1854,   1855,   924,   315,   70,   21,   0,  1;
[8]   14833,  14832,  7420,  2464,  630,  112,  28,  0, 1;
[9]  133496, 133497, 66744, 22260, 5544, 1134, 168, 36, 0, 1;
"""


@cache
def rencontres(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]

    row = [
        (n - 1) * (rencontres(n - 1)[0] + rencontres(n - 2)[0])
    ] + rencontres(n - 1)
    for k in range(1, n - 1):
        row[k] = (n * row[k]) // k
    return row


Rencontres = Table(
    rencontres,
    "Rencontres",
    ["A008290", "A098825"],
    "A055137",
    r"\binom{n}{k} derangements(n - k)",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Rencontres)
