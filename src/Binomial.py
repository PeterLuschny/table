from functools import cache
from _tabltypes import Table

"""Pascal triangle, binomial coefficients.


[0]   1;
[1]   1,   1;
[2]   1,   2,   1;
[3]   1,   3,   3,   1;
[4]   1,   4,   6,   4,   1;
[5]   1,   5,  10,  10,   5,   1;
[6]   1,   6,  15,  20,  15,   6,   1;
[7]   1,   7,  21,  35,  35,  21,   7,   1;
[8]   1,   8,  28,  56,  70,  56,  28,   8,   1;
[9]   1,   9,  36,  84, 126, 126,  84,  36,   9,   1;


Inverse binomial triangle:

   1;
  -1,    1;
   1,   -2,    1;
  -1,    3,   -3,    1;
   1,   -4,    6,   -4,    1;
  -1,    5,  -10,   10,   -5,    1;
   1,   -6,   15,  -20,   15,   -6,    1;
  -1,    7,  -21,   35,  -35,   21,   -7,    1;
   1,   -8,   28,  -56,   70,  -56,   28,   -8,    1;
  -1,    9,  -36,   84, -126,  126,  -84,   36,   -9,    1;
  ...
"""


@cache
def binomial(n: int) -> list[int]:
    if n == 0:
        return [1]

    row: list[int] = [1] + binomial(n - 1)
    for k in range(1, n):
        row[k] += row[k + 1]
    return row


def invbinomial(n: int) -> list[int]:
    return [(-1)**(n - k) * binomial(n)[k] for k in range(n + 1)]


Binomial = Table(binomial, "Binomial", 
["A007318", "A074909", "A108086", "A117440",
"A118433", "A130595", "A135278", "A154926" ], True,
r"n! \, / (k! \, (n - k)! )")


InvBinomial = Table(invbinomial, "InvBinomial", ["A130595"], True,
r"(-1)^{n-k} \, n! \, / (k! \, (n - k)! )" )


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Binomial)
    PreView(InvBinomial)
