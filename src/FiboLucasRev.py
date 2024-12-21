from functools import cache
from FiboLucas import fibolucas
from _tabltypes import Table

"""FiboLucasRev polynomials, m = 2.

| [1] |
| [2, 1] |
| [1, 2, 1] |
| [2, 2, 2, 1] |
| [1, 4, 3, 2, 1] |
| [2, 3, 6, 4, 2, 1] |
| [1, 6, 6, 8, 5, 2, 1] |
| [2, 4, 12, 10, 10, 6, 2, 1] |

# @cache
def T(n: int, k: int) -> int:
    if k > n: return 0
    if k < 2: return k + 1
    return T(n - 1, k) + T(n - 2, k - 2)
"""


@cache
def fibolucasrev(n: int) -> list[int]:
    if n == 0:
        return [1]
    return list(reversed(fibolucas(n)))


FiboLucasRev = Table(
    fibolucasrev, 
    "FiboLucasRev", 
    ["A124038"], 
    "A000000", 
    r"%%"
)


if __name__ == "__main__":
    from _tablutils import PreView
    PreView(FiboLucasRev)
