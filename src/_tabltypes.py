from typing import Callable, TypeAlias
from itertools import accumulate
from _tablinverse import InvertMatrix

# #@

# TABLE T ENUMERATED AS A TRIANGLE
# Is always (0,0)-based!
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
#
# Examples for the enumerations:
# row(4)     = [T(4,0), T(4,1), T(4,2), T(4,3), T(4,4)]
# col(2, 5)  = [T(2,2), T(3,2), T(4,2), T(5,2), T(6,2)]
# diag(2, 5) = [T(2,0), T(3,1), T(4,2), T(5,3), T(6,4)]


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


def PseudoGenerator(T: tabl, max: int) -> rgen:
    """A generator for an already existing table.

    Args:
        T, table to be wrapped
        max, size of the table

    Returns:
        table generator

    Error:
        Raises a ValueError if the requested size > size of given table, 
        or returns an emtpy list, dependig on your choice.
    """
    def gen(n: int) -> trow:
        if n >= max:
            #raise ValueError('requested size > size of given table')
            return []
        return T[n]
    return gen

#    We do not document the case gen: tabl below, because
#    in this case all the generatetibility of our approach is lost
#    and it is easy to produce 'index out of range' errors.
#    Still in some test cases it is useful in connection with the
#    above "PseudoGenerator". For internal use only.
class Table:
    """Provides basic methods for manipulating integer triangles."""
    def __init__(
        self, 
        gen: rgen,
        id: str, 
        sim: list[str] = [''],
        invQ: bool | None = None
        ) -> None:
        """
        Provides basic methods for manipulating integer triangles. 

        Args:
            gen, Function gen(n:int) -> list[int], defined for all n >= 0. 
            id, The name of the triangle.
            sim, A list of A-numbers of closley related OEIS triangles.
            invQ, is the triangle invertible? Defaults to None meaning 'I do not know'.
        """

        if isinstance(gen, list):
            self.gen = PseudoGenerator(gen, len(gen))
        else:
            self.gen = gen

        self.id = id
        self.sim = sim
        self.invQ = invQ


    def val(self, n:int, k:int) -> int:
        """Term of table with index (n, k).

        Args:
            n, row index 
            k, column index 

        Returns:
            term of the table
        """
        return self.gen(n)[k]

    def row(self, n: int) -> trow:
        """n-th row of generated table

        Args:
            n, row index

        Returns:
            n-th row 
        """
        return self.gen(n)

    def tab(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            table generated 
        """
        return [list(self.gen(n)) for n in range(size)]

    def rev(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            tabel with reversed rows
        """
        return [list(reversed(self.gen(n))) for n in range(size)]

    def adtab(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            table of (upward) anti-diagonals
        """
        return [[self.gen(n - k - 1)[k] 
                 for k in range((n + 1) // 2)] for n in range(1, size + 1)]

    def diag(self, n: int, size: int) -> list[int]:
        """
        Args:
            n, start at row n 
            size, length of diagonal

        Returns:
            n-th diagonal starting at the left side
        """
        return [self.gen(n + k)[k] for k in range(size)]

    def col(self, k: int, size: int) -> list[int]:
        """
        Args:
            k, start at column k
            size, length of column

        Returns:
            k-th column starting at the main diagonal
        """
        return [self.gen(k + n)[k] for n in range(size)]

    def sum(self, size: int) -> list[int]:
        """
        Args:
            size, number of rows to be summed

        Returns:
            The first 'size' row sums.
        """
        return [sum(self.gen(n)) for n in range(size)]

    def acc(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            table with rows accumulated
        """
        return [list(accumulate(self.gen(n))) for n in range(size)]

    def mat(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            matrix with generated table as lower triangle
        """
        return [[self.gen(n)[k] if k <= n else 0 for k in range(size)] for n in range(size)]

    def flat(self, size: int) -> list[int]:
        """
        Args:
            size, number of rows

        Returns:
            generated table read by rows, flattened
        """
        return [self.gen(n)[k] for n in range(size) for k in range(n + 1)]

    def inv(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            inverse table
        """
        if self.invQ == False:
            return []
        M = [[self.gen(n)[k] for k in range(n + 1)] for n in range(size)]
        V = InvertMatrix(M)
        if V == []:
            self.invQ = False
            return []
        return V

    def revinv(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            table with reversed rows of the inverse table
        """
        V = self.inv(size)
        if V == []:
            return []
        return [[V[n][n - k] for k in range(n + 1)] for n in range(size)]

    def invrev(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            inverse table of reversed rows of generated table
        """
        M = [list(reversed(self.gen(n))) for n in range(size)]
        return InvertMatrix(M)

    def off(self, N: int, K: int) -> rgen:
        """
        Args:
            N, shifts row-offset by N 
            K, shifts column-offset by K

        Returns:
            row generator of shifted table
        """
        def subgen(n: int) -> trow:
            return self.gen(n + N)[K : N + n + 1] 
        return subgen

    def invrev11(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            sub-table with offset (1,1), reversed rows and inverted
        """
        M = [list(reversed(self.off(1, 1)(n))) for n in range(size)]
        return InvertMatrix(M)

    def poly(self, n: int, x: int) -> int:
        """The rows seen as the coefficients of a polynomial in
        ascending order of powers. Evaluats the n-th row at x.

        Args:
            n, index of row
            x, argument of the polynomial

        Returns:
            sum(T(n, k) * x^j for j=0..n)
        """
        row = self.gen(n)
        return sum(c * (x ** j) for (j, c) in enumerate(row))

    def summap(self, s: seq, size: int) -> list[int]:
        """[sum(T(n, k) * s(k) for 0 <= k <= n) for 0 <= n < size]
           For example, if T is the binomial then this is the 
           'binomial transform'.

        Args:
            s, sequence
            size 

        Returns:
            Initial segment of length size of s transformed.
        """
        return [sum(self.gen(n)[k] * s(k) 
                    for k in range(n + 1)) for n in range(size)]

    def invmap(self, s: seq, size: int) -> list[int]:
        """[sum((-1)^(n-k) * T(n, k) * s(k) for 0 <= k <= n) 
            for 0 <= n < size]
            For example, if T is the binomial then this is the 
            'inverse binomial transform'.

        Args:
            s, sequence
            size 

        Returns:
            Initial segment of length size of s transformed.
        """
        return [sum((-1)**(n-k) * self.gen(n)[k] * s(k) 
                    for k in range(n + 1)) for n in range(size)]

    def show(self, size: int) -> None:
        """Prints the first 'size' rows with row-number.

        Args:
            size, number of rows
        """
        for n in range(size):
            print([n], self.gen(n))



if __name__ == "__main__":

    from functools import cache
    from math import comb as binomial
    from _tablutils import PreView
    from StirlingSet import StirlingSet

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
