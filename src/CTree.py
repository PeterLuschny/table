from functools import cache
from _tabltypes import Table

"""Christmas tree, binomial(n mod 2, k mod 2).

[0]                           1
[1]                          1, 1
[2]                        1, 0, 1
[3]                       1, 1, 1, 1
[4]                     1, 0, 1, 0, 1
[5]                    1, 1, 1, 1, 1, 1
[6]                  1, 0, 1, 0, 1, 0, 1
[7]                 1, 1, 1, 1, 1, 1, 1, 1
[8]               1, 0, 1, 0, 1, 0, 1, 0, 1
[9]              1, 1, 1, 1, 1, 1, 1, 1, 1, 1
"""


@cache
def ctree(n: int) -> list[int]:
    if n % 2 == 1:
        return [1] * (n + 1)

    return [1, 0] * (n // 2) + [1]


CTree = Table(
    ctree, 
    "CTree", 
    ["A106465", "A106470"], 
    "A00000",
    r"is(n \text{ odd})\ ? \ 1 : (k + 1) \text{ mod } 2"
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(CTree)
