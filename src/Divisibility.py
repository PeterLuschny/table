from functools import cache
from _tabltypes import Table

"""
The divisibility matrix, the indicator function for divisibility.

[ 0]  1
[ 1]  0  1
[ 2]  0  1  1
[ 3]  0  1  0  1
[ 4]  0  1  1  0  1
[ 5]  0  1  0  0  0  1
[ 6]  0  1  1  1  0  0  1
[ 7]  0  1  0  0  0  0  0  1
[ 8]  0  1  1  0  1  0  0  0  1
[ 9]  0  1  0  1  0  0  0  0  0  1
[10]  0  1  1  0  0  1  0  0  0  0  1
"""


@cache
def divisibility(n: int) -> list[int]:
    if n == 0:
        return [1]
    L = [0 for _ in range(n + 1)]
    L[1] = L[n] = 1
    i = 1
    div = n

    while i < div:
        div, mod = divmod(n, i)
        if mod == 0:
            L[i] = L[div] = 1
        i += 1
    return L


Divisibility = Table(
    divisibility,
    "Divisibility",
    ["A113704", "A051731"],
    "A000000",
    r"[n=0 \text{ or } k \text{ divides } n]",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Divisibility)
