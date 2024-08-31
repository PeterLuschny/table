# See https://github.com/PeterLuschny/table for hints how to install 'Tables'.

from Tables import Table, PreView, StirlingSet
from functools import cache
from math import comb as binomial


PreView(StirlingSet)


@cache
def abel(n: int) -> list[int]:
    if n == 0: return [1]
    return [binomial(n - 1, k - 1) * n ** (n - k) if k > 0 else 0 
            for k in range(n + 1)]

Abel = Table(abel, "Abel", ["A137452", "A061356", "A139526"], True)

PreView(Abel)


# Error demonstration:
# Babel.tab(7)
# ValueError('requested size > size of given table')
