# See https://github.com/PeterLuschny/table for hints how to install 'Tables'.

from Tables import Table, PreView, Benchmark, StirlingSet
from functools import cache
from math import comb as binomial


@cache
def abel(n: int) -> list[int]:
    if n == 0: return [1]
    return [binomial(n - 1, k - 1) * n ** (n - k) if k > 0 else 0 
            for k in range(n + 1)]

Abel = Table(abel, "Abel", ["A137452", "A061356", "A139526"], True)

PreView(Abel)

# =================================================================

T = [ [1], [0, 1], [0, -2, 1], [0, 3, -6, 1], [0, -4, 24, -12, 1], 
     [0, 5, -80, 90, -20, 1], [0, -6, 240, -540, 240, -30, 1], 
     [0, 7, -672, 2835, -2240, 525, -42, 1], 
     [0, -8, 1792, -13608, 17920, -7000, 1008, -56, 1] ]

Babel = Table(T, "Babel", ["A059297"], True)

PreView(Babel)

# =================================================================

PreView(StirlingSet)

Benchmark(StirlingSet)


# =================================================================    

# Error demonstration:
# Babel.tab(7)
# ValueError('requested size > size of given table')
