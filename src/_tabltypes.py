from typing import Callable, TypeAlias, Iterator
from itertools import accumulate, islice
from functools import cache
import operator
from more_itertools import difference
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


"""Type: row"""
trow: TypeAlias = list[int]

"""Type: triangle"""
tabl: TypeAlias = list[list[int]]

"""Type: sequence"""
seq: TypeAlias = Callable[[int], int]

"""Type: row generator"""
rgen: TypeAlias = Callable[[int], trow]

"""Type: triangle generator"""
tgen: TypeAlias = Callable[[int, int], int]


#    We do not document the case gen: tabl below, because in this
#    case it is easy to produce 'index out of range' errors.
#    Still in some test cases it is useful in connection with the
#    above "PseudoGenerator". For internal use only.
def PseudoGenerator(T: tabl, max: int) -> rgen:
    """A generator for an already existing table.

    Args:
        T, table to be wrapped
        max, size of the table

    Returns:
        table generator

    Error:
        If the requested size > size of given table then
        an emtpy list is returned.
    """
    def gen(n: int) -> trow:
        if n >= max:
            return []
        return T[n]
    return gen

# Useful for the LaTeX titels: https://latexeditor.lagrida.com/

class Table:
    """Provides basic methods for manipulating integer triangles."""
    def __init__(
            self,
            gen: rgen,
            id: str,
            sim: list[str] = [''],
            invid: str = '',
            tex: str = ''
        ) -> None:
        """
        Provides basic methods for manipulating integer triangles.

        Args:
            gen:  Function gen(n:int) -> list[int], defined for all n >= 0.
            id:   The name of the triangle.
            sim:  A list of A-numbers of closley related OEIS triangles.
            invQ: is the triangle invertible?
                  Defaults to None meaning 'I do not know'.
            tex: Defining formula as a TeX-string. 
        """

#if isinstance(gen, tabl): # type: ignore
#    self.gen = PseudoGenerator(gen, len(gen))
#else:
        self.gen = gen
        self.id = id
        self.sim = sim
        self.invid = invid
        self.tex = tex
        self.invQ = invid != ''
        self.impact = 0

    def __getitem__(self, n: int) -> list[int]:
        return self.gen(n)

    def set_impact(self, imp: int) -> None:
        self.impact = imp

    def get_impact(self) -> int:
        return self.impact

    def itr(self, size: int) -> Iterator[list[int]]:
        return islice(iter(self.tab(size)), size)

    def tab(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            table generated
        """
        return [list(self.gen(n))
                for n in range(size)]

    def mat(self, size: int) -> tabl:
        """
        Args:
            size, number of rows and columns

        Returns:
            matrix with generated table as lower triangle
        """
        return [[self.gen(n)[k] if k <= n else 0
                for k in range(size)]
                for n in range(size)]

    def val(self, n: int, k: int) -> int:
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

    def rev(self, row: int) -> trow:
        """
        Args:
            row number to be reversed

        Returns:
            reversed row
        """
        return list(reversed(self.gen(row)))

    def antidiag(self, n: int) -> list[int]:
        """
        Args:
            start index of the antidiagonal

        Returns:
            n-th antidiagonal
        """
        return [self.gen(n - k)[k]
                 for k in range((n + 2) // 2)]

    def alt(self, n: int) -> trow:
        return [(-1) ** k * term 
                for k, term in enumerate(self.gen(n))]

    def acc(self, row: int) -> trow:
        """
        Args:
            index of row to be accumulated

        Returns:
            accumulated row
        """
        return list(accumulate(self.gen(row)))

    def diff(self, n: int) -> trow:
        """
        Args:
            index of row the first differences is searched

        Returns:
            first differences of row
        """
        return list(difference(self.gen(n)))
    
    def der(self, n: int) -> trow:
        """
        Args:
            index of row-polynomial the derivative is searched

        Returns:
            derivative of row-polynomial
        """
        powers = range(n + 3)
        coeffs = self.gen(n + 1)
        return list(map(operator.mul, coeffs, powers))[1:]

    def diag(self, n: int, size: int) -> list[int]:
        """
        Args:
            n is index of start of the diagonal
            size, length of diagonal

        Returns:
            n-th diagonal starting at the left side
        """
        return [self.gen(n + k)[k]
                for k in range(size)]

    def col(self, k: int, size: int) -> list[int]:
        """
        Args:
            k, start at column k
            size, length of column

        Returns:
            k-th column starting at the main diagonal
        """
        return [self.gen(k + n)[k]
                for n in range(size)]

    def sum(self, row: int) -> int:
        """
        Args:
            row number to be summed

        Returns:
            row sum
        """
        return sum(self.gen(row))

    def flat(self, size: int) -> list[int]:
        """
        Args:
            size, number of rows

        Returns:
            generated table read by rows, flattened
        """
        return [self.gen(n)[k]
                for n in range(size)
                for k in range(n + 1)]

    def inv(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            inverse table
        """
        if not self.invQ:
            return []

#   self.tab(size) = [list(self.gen(n)) for n in range(size)]
        M = [[self.gen(n)[k]
             for k in range(n + 1)]
             for n in range(size)]

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

        return [[V[n][n - k]
                 for k in range(n + 1)]
                 for n in range(size)]

    def invrev(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            inverse table of reversed rows of generated table
        """
        M = [list(reversed(self.gen(n)))
             for n in range(size)]

        return InvertMatrix(M)

    def off(self, N: int, K: int) -> rgen:
        """
        Subtriangle based in (N, K).
        Args:
            N, shifts row-offset by N
            K, shifts column-offset by K

        Returns:
            row generator of shifted table
        """
        def subgen(n: int) -> trow:
            return self.gen(n + N)[K: N + n + 1]

        return subgen

    def rev11(self, n: int) -> trow:
        """
        Args:
            size, number of rows

        Returns:
            sub-table with offset (1,1) and reversed rows
        """

        return list(reversed(self.off(1, 1)(n)))

    def inv11(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            inverse of the sub-table with offset (1,1)
        """
        M = [list(self.off(1, 1)(n))
             for n in range(size)]

        return InvertMatrix(M)
    
    def revinv11(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            reversed rows of the inverse sub-table with offset (1,1)
        """
        M = self.inv11(size)
        return [list(reversed(row)) for row in M]

    def invrev11(self, size: int) -> tabl:
        """
        Args:
            size, number of rows

        Returns:
            sub-table with offset (1,1), reversed rows and inverted
        """
        M = [list(reversed(self.off(1, 1)(n)))
             for n in range(size)]

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
        return sum(c * (x ** j) for (j, c) in enumerate(self.gen(n)))

    # Also called sumprod.
    def trans(self, s: seq, size: int) -> list[int]:
        """[sum(T(n, k) * s(k) for 0 <= k <= n) for 0 <= n < size]
           For example, if T is the binomial then this is the
           'binomial transform'.

        Args:
            s, sequence. Recommended to be cached function.
            size, length of the returned list

        Returns:
            Initial segment of length size of s transformed.
        """
        return [sum(self.gen(n)[k] * s(k) for k in range(n + 1))
               for n in range(size)]

    def invtrans(self, s: seq, size: int) -> list[int]:
        """[sum((-1)^(n-k) * T(n, k) * s(k) for 0 <= k <= n)
            for 0 <= n < size]
            For example, if T is the binomial then this is the
            'inverse binomial transform'.

        Args:
            s, sequence. Recommended to be cached function.
            size, length of the returned list

        Returns:
            Initial segment of length size of s transformed.
        """
        return [sum((-1)**(n-k) * self.gen(n)[k] * s(k) for k in range(n + 1))
               for n in range(size)]

    def show(self, size: int) -> None:
        """Prints the first 'size' rows with row-number.

        Args:
            size, number of rows
        """
        for n in range(size):
            print([n], self.gen(n))
 

def RevTable(T: Table) -> Table:
    """ """
    @cache
    def revgen(n: int) -> trow:
        return T.rev(n)
    return Table(revgen, T.id + ":Rev")

def AltTable(T: Table) -> Table:
    """ """
    @cache
    def altgen(n: int) -> trow:
        return T.alt(n)
    return Table(altgen, T.id + ":Alt")


def SubTriangle(T: Table, N: int, K: int) -> Table:
    """
    Generates a sub-triangle of a given size from a given triangle.

    Args:
        T (Table) 
        N (int): The starting row index of the sub-triangle.
        K (int): The starting column index of the sub-triangle.
        size (int): The size of the sub-triangle.

    Returns:
        tabl: The generated sub-triangle.

    """
    return Table(T.off(N, K), T.id + ":Off")


"""Type: trait"""
trait: TypeAlias = Callable[[Table, int], list[int]]


if __name__ == "__main__":

    from functools import cache
    from math import comb as binomial
    from _tablutils import PreView
    from more_itertools import flatten
    from StirlingSet import StirlingSet

    PreView(StirlingSet)

    @cache
    def abel(n: int) -> list[int]:
        if n == 0:
            return [1]
        return [binomial(n - 1, k - 1) * n ** (n - k) if k > 0 else 0
                for k in range(n + 1)]

    Abel = Table(
    abel, 
    "Abel", 
    ["A137452", "A061356", "A139526"], 
    "A059297",
    r"is(k = 0)\ ? \ 0^n : \binom{n-1}{k-1} (-n)^{n - k}" 
)

    PreView(Abel)

    print()
    print("Different ways to display a Table:")
    print()

    Abel.show(7)

    print()
    print(Abel.tab(7))

    print()
    print(list(flatten(Abel.itr(7))))

    print()

    # Use the Table as an iterable:
    rows = StirlingSet.itr(7)
    for r in rows:
        print(r, sum(r))

    print()
