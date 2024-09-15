from functools import cache
from _tabltypes import Table

"""Polya Trees accumulated
[0] [1]
[1] [0, 1]
[2] [0, 1,  2]
[3] [0, 1,  3,  4]
[4] [0, 1,  5,  8,   9]
[5] [0, 1,  7, 15,  19,  20]
[6] [0, 1, 11, 29,  42,  47,  48]
[7] [0, 1, 15, 53,  89, 108, 114, 115]
[8] [0, 1, 22, 98, 191, 252, 278, 285, 286]
"""

@cache
def divisors(n: int) -> list[int]:
    return [d for d in range(n, 0, -1) if n % d == 0]


@cache
def h(n: int, k: int) -> int:
    return sum(d * T(d, k) for d in divisors(n))


# A244925  (which is (1, 0)-based)
@cache
def H(n: int, k: int) -> int:
    return sum(d * T(d, k) for d in divisors(n) if k <= d)

# A113704
@cache
def e(n: int, k: int) -> int:
    return sum(d * T(d, k) for d in divisors(n) if k == d)

# Call the function h, H, or e according to your use case. 
@cache
def T(n: int, k: int) -> int:
    if n == 1: return int(k > 0)

    return sum(T(i, k) * h(n - i, k - 1) for i in range(1, n)
           ) // (n - 1)


# T(n, k) will add a (0,0,0...) column on the left.
# Interpretations exist for both cases, it is mainly 
# a matter of terminology. The form T(n + 1, k + 1) is
# to be prefered as it covers A113704 in the case k = d,
# which is our Divisibility triangle.
@cache
def polyatreeacc(n: int) -> list[int]:
    return [T(n + 1, k + 1) for k in range(n + 1)]


PolyaTreeAcc = Table(polyatreeacc, "PolyaTreeAcc", ["A375467"])


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(PolyaTreeAcc)

    for n in range(9):
        print([h(n, k) for k in range(n + 1)])

    for n in range(9):
        print([H(n, k) for k in range(n + 1)])
