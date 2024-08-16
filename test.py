from Tables import Tables, Table, View, StirlingSet

View(StirlingSet)

# =======================================

T = [[1], [0, 1], [0, -2, 1], [0, 3, -6, 1], [0, -4, 24, -12, 1], [0, 5, -80, 90, -20, 1]]

Babel = Table(T, "Babel", ["A059297"], True)

View(Babel)

# =======================================

from functools import cache
from math import comb as binomial

@cache
def abel(n: int) -> list[int]:
    if n == 0: return [1]
    return [binomial(n - 1, k - 1) * n ** (n - k) if k > 0 else 0 
            for k in range(n + 1)]

Abel = Table(abel, "Abel", ["A137452", "A061356", "A139526"], True)

View(Abel)

# =======================================

for tabl in Tables: 
    print(tabl.id)
