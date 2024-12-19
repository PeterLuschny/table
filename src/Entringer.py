from functools import cache
from _tabltypes import Table

"""Euler-Bernoulli triangle.

[0] [1]
[1] [0,   1]
[2] [0,   1,   1]
[3] [0,   1,   2,   2]
[4] [0,   2,   4,   5,    5]
[5] [0,   5,  10,  14,   16,   16]
[6] [0,  16,  32,  46,   56,   61,   61]
[7] [0,  61, 122, 178,  224,  256,  272,  272]
"""


@cache
def entringer(n: int) -> list[int]:
    if n == 0:
        return [1]

    rowA = entringer(n - 1)
    row = [0] + entringer(n - 1)
    row[1] = row[n]
    for k in range(2, n + 1):
        row[k] = row[k - 1] + rowA[n - k]
    return row


Entringer = Table(
    entringer,
    "Entringer",
    ["A008281", "A008282", "A010094"],
    "A000000",
    r"is(k=0) \ ? \ 0^n : T(n, k-1) + T(n-1, n-k)",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Entringer)
