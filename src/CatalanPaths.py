from functools import cache
from _tabltypes import Table

"""Catalan paths.

[0]   1,
[1]   0,   1,
[2]   1,   0,   1,
[3]   0,   2,   0,   1,
[4]   2,   0,   3,   0,   1,
[5]   0,   5,   0,   4,   0,   1,
[6]   5,   0,   9,   0,   5,   0,   1,
[7]   0,  14,   0,  14,   0,   6,   0,  1,
[8]  14,   0,  28,   0,  20,   0,   7,  0,  1,
[9]   0,  42,   0,  48,   0,  27,   0,  8,  0,  1.
"""


@cache
def catalanpaths(n: int) -> list[int]:
    if n == 0:
        return [1]

    def r(k: int) -> int:
        return catalanpaths(n - 1)[k] if k >= 0 and k < n else 0

    row = catalanpaths(n - 1) + [1]
    for k in range(0, n):
        row[k] = r(k - 1) + r(k + 1)
    return row


CatalanPaths = Table(
    catalanpaths,
    "CatalanPaths",
    ["A053121", "A052173", "A112554", "A322378"],
    "A000000",
    r"is(k = 0)\ ? \ 0 : \frac{k+1}{n+1} \binom{n+1}{(n-k)/2}",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(CatalanPaths)
