from functools import cache
from _tabltypes import Table

"""FiboLucasInv polynomials.

    [0] [  1]
    [1] [ -2,   1]
    [2] [  3,  -2,   1]
    [3] [ -4,   2,  -2,   1]
    [4] [  6,  -2,   1,  -2,   1]
    [5] [-10,   5,   0,   0,  -2,  1]
    [6] [ 15, -10,   5,   2,  -1, -2,  1]
    [7] [-20,  10, -12,   6,   4, -2, -2,  1]
    [8] [ 30,  -8,   4, -16,   8,  6, -3, -2,  1]
    [9] [-52,  26,   8,  -4, -22, 11,  8, -4, -2, 1]

"""


@cache
def fibolucasinv(n: int) -> list[int]:
    if n == 0: return [1]
    if n == 1: return [-2, 1]
    fli = fibolucasinv(n - 1)
    row = [1] * (n + 1)
    row[n - 1] = -2
    for k in range(n - 2, 0, -1):
        row[k] = fli[k - 1] - fli[k + 1]
    row[0] = -2 * fli[0] - fli[1]
    return row


FiboLucasInv = Table(
    fibolucasinv, 
    "FiboLucasInv", 
    ["A375025"], 
    "A000000", 
    r"%%"
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(FiboLucasInv)
