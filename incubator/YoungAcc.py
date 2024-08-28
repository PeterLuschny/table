from functools import cache
from _tabltypes import Table

""" 
[0]  1
[0]  0,  1
[0]  0,  1,  2
[0]  0,  1,  3,   4
[0]  0,  1,  6,   9,  10
[0]  0,  1, 10,  21,  25,  26
[0]  0,  1, 20,  51,  70,  75,  76
[0]  0,  1, 35, 127, 196, 225, 231, 232
[0]  0,  1, 70, 323, 588, 715, 756, 763, 764
"""

@cache
def youngacc(n: int) -> list[int]:
    return [n] * (n+1)


YoungAcc = Table(
    youngacc,
    "YoungAcc",
    ["A049400", "A182172"],
    True )


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(YoungAcc)
