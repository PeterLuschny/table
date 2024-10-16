from functools import cache
from _tabltypes import Table

"""Lehmer-Comtet of 2nd kind, unsigned.


[0] 1;
[1] 0,      1;
[2] 0,      1,      1;
[3] 0,      4,      3,      1;
[4] 0,     27,     19,      6,     1;
[5] 0,    256,    175,     55,    10,    1;
[6] 0,   3125,   2101,    660,   125,   15,   1;
[7] 0,  46656,  31031,   9751,  1890,  245,  21,  1;
[8] 0, 823543, 543607, 170898, 33621, 4550, 434, 28, 1;
"""


@cache
def t(n: int, k: int, m: int) -> int:
    if k < 0 or n < 0:
        return 0
    if k == 0:
        return n**k
    return m * t(n, k - 1, m) + t(n - 1, k, m + 1)


@cache
def lehmer(n: int) -> list[int]:
    return [t(k - 1, n - k, n - k) if n != k else 1 for k in range(n + 1)]


Lehmer = Table(lehmer, "Lehmer", ["A354794", "A039621"], True,
r"\(\bbox[yellow, 5px]{\color{DarkGreen} T_{n, k} = is(n = k)\ ? \ 1 : \sum_{j=0}^{k-1} (-1)^{j} (n-j-1)^{n-1} / (j! (k-1-j)!) } \)" )


if __name__ == "__main__":
    from _tablutils import PreView

    # TODO Needs a more efficient implementation.
    PreView(Lehmer)
