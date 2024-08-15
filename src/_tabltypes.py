from typing import Callable, TypeAlias
from itertools import accumulate
from _tablinverse import InvertTriangle, InvertMatrix

# #@

# T ENUMERATED AS A TRIANGLE
#
# T(0,0)
# T(1,0)  T(1,1)
# T(2,0)  T(2,1)  T(2,2)
# T(3,0)  T(3,1)  T(3,2)  T(3,3)
# T(4,0)  T(4,1)  T(4,2)  T(4,3)  T(4,4)
# T(5,0)  T(5,1)  T(5,2)  T(5,3)  T(5,4)  T(5,5)
#
# A subtriangle of the standard triangle T as indexed above
# is given by a new root node [N, K].
# For some dimension size > 0 it is defined as
# T[N, K, size] = [[T(n, k) for k in range(K, N + n + 1)] 
#                           for n in range(N, N + size)]


"""Type: table row"""
trow: TypeAlias = list[int]

"""Type: triangle (resp. table)"""
tabl: TypeAlias = list[list[int]]

"""Type: sequence generator"""
seq: TypeAlias = Callable[[int], int]

"""Type: row generator"""
rgen: TypeAlias = Callable[[int], trow]

"""Type: triangle (resp. table) generator"""
tgen: TypeAlias = Callable[[int, int], int]


def PseudoGenerator(T: tabl) -> rgen:
    def gen(n: int) -> list[int]:
        return [T[n][k] for k in range(n + 1)]
    return gen


class Table:
    def __init__(
            self, 
            gen: rgen | tabl, 
            id: str, 
            sim: list[str] = [''], 
            invabl: bool | None = None
            ) -> None:
        
        if isinstance(gen, list):
            self.gen = PseudoGenerator(gen)
        else:
            self.gen = gen

        self.id = id
        self.sim = sim
        self.invabl = invabl


    def val(self, n:int, k:int) -> int:
        return self.gen(n)[k]

    def row(self, n: int) -> trow:
        return self.gen(n)

    def tab(self, size: int) -> tabl:
        return [list(self.gen(n)) for n in range(size)]

    def rev(self, size: int) -> tabl:
        return [list(reversed(self.gen(n))) for n in range(size)]

    def diag(self, size: int) -> tabl:
        """Return the table of (upward) anti-diagonals."""
        return [[self.gen(n - k - 1)[k] 
                 for k in range((n + 1) // 2)] for n in range(1, size + 1)]

    def acc(self, size: int) -> tabl:
        return [list(accumulate(self.gen(n))) for n in range(size)]

    def mat(self, size: int) -> tabl:
        return [[self.gen(n)[k] if k <= n else 0 for k in range(size)] for n in range(size)]

    def flat(self, size: int) -> trow:
        return [self.gen(n)[k] for n in range(size) for k in range(n + 1)]

    def inv(self, size: int) -> tabl:
        if self.invabl == False:
            return []
        V = InvertTriangle(self.gen, size)
        if V == []:
            self.invabl = False
            return []
        return V

    def revinv(self, size: int) -> tabl:
        V = self.inv(size)
        if V == []:
            return []
        return [[V[n][n - k] for k in range(n + 1)] for n in range(size)]

    def invrev(self, size: int) -> tabl:
        R = [list(reversed(self.gen(n))) for n in range(size)]
        M = [[R[n][k] if k <= n else 0 for k in range(size)] for n in range(size)]
        return InvertMatrix(M)

    def off(self, N: int, K: int) -> rgen:
        def subgen(n: int) -> trow:
            return self.gen(n + N)[K : N + n + 1] 
        return subgen

    def invrev11(self, size: int) -> tabl:
        R = [list(reversed(self.off(1,1)(n))) for n in range(size)]
        M = [[R[n][k] if k <= n else 0 for k in range(size)] for n in range(size)]
        return InvertMatrix(M)


def View(T:Table, size: int = 6) -> None:
    print("name       ", T.id)
    print("similars   ", T.sim)
    print("invertible ", T.invabl)
    print("table      ", T.tab(size))
    print("anti-diag  ", T.diag(size))
    print("accumulated", T.acc(size))
    print("inverted   ", T.inv(size))
    print("rev of inv ", T.revinv(size))
    print("reverted   ", T.rev(size))
    print("inv of rev ", T.invrev(size))
    print("matrix     ", T.mat(size))
    print("flatt seq  ", T.flat(size))
    print("inv rev 11 ", T.invrev11(size-1))
    T11 = Table(T.off(1, 1), "Toffset11")
    print("1-1-based  ", T11.tab(size-1))
    print("some row   ", T.row(size-1))
    print("some value ", T.val(size-1, (size-1)//2))


if __name__ == "__main__":

    from functools import cache
    from math import comb as binomial

    @cache
    def abel(n: int) -> list[int]:
        if n == 0: return [1]
        return [binomial(n - 1, k - 1) * n ** (n - k) if k > 0 else 0 
                for k in range(n + 1)]

    Abel = Table(abel, "Abel", ["A137452", "A061356", "A139526"], True)

    View(Abel)

# =================================================================

    T = [[1], [0, 1], [0, -2, 1], [0, 3, -6, 1], [0, -4, 24, -12, 1], [0, 5, -80, 90, -20, 1]]

    Babel = Table(T, "Babel", ["A059297"], True)

    View(Babel)
