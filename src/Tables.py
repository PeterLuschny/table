from functools import cache
from itertools import accumulate
from math import factorial, sqrt
from fractions import Fraction
import time
from sys import setrecursionlimit, set_int_max_str_digits
from typing import Callable, TypeAlias
setrecursionlimit(3000)
set_int_max_str_digits(5000)
def InvertMatrix(L: list[list[int]], check: bool = True) -> list[list[int]]:
    """
    Calculates the inverse of a lower triangular matrix.
    Args:
        The lower triangular matrix to be inverted.
        Check whether the inverse exists as an integer matrix, defaults to True.
    Returns:
        The integer inverse of the lower triangular matrix if it exists.
        []: If the inverse does not exist.
    """
    n = len(L)
    inv = [[0 for _ in range(n)] for _ in range(n)]  # Identity matrix
    for i in range(n):
        inv[i][i] = 1
    for k in range(n):
        for j in range(n):
            for i in range(k):
                inv[k][j] -= inv[i][j] * L[k][i]
            if check:
                a = inv[k][j]
                b = L[k][k]
                if b == 0:
                    # print("Warning: Inverse does not exist!")
                    # raise ValueError("Inverse does not exist!")
                    return []
                a, r = divmod(a, b)  # make sure that a is integer
                if r != 0:
                    # print("Warning: Integer terms do not exist!")
                    # raise ValueError("Integer inverse does not exist!")
                    return []
    return [row[0:n + 1] for n, row in enumerate(inv)]
def InvertTriangle(r: Callable[[int], list[int]], dim: int) -> list[list[int]]:
    M = [[r(n)[k] for k in range(n + 1)] for n in range(dim)]
    return InvertMatrix(M, True)
def convtriangle(seq: Callable[[int], int], dim: int = 10) -> list[list[int]]:
    """Sometimes called the partition transform of seq. 
    See A357368 for more information and some examples.
    Args:
        seq, sequence to be convoluted
        dim, the size of the triangle
    Returns:
        The convolution triangle of seq.
    """
    A = [seq(i) for i in range(1, dim)] # Cache the input sequence.
    # print("In:", A)
    C = [[0 for _ in range(m + 1)] for m in range(dim)]
    C[0][0] = 1
    for m in range(1, dim):
        C[m][m] = C[m - 1][m - 1] * A[0]
        for k in range(m - 1, 0, -1):
            C[m][k] = sum(A[i] * C[m - i - 1][k - 1] for i in range(m - k + 1))
    return C
def ConvTriangle(
        T: Callable[[int, int], int], 
        seq: Callable[[int], int], 
        dim: int = 10
    ) -> list[list[int]]:
    A = [seq(i) for i in range(1, dim)] # Cache the input sequence.
    # print("In:", A)
    C = [[0 for _ in range(m + 1)] for m in range(dim)]
    C[0][0] = 1
    for m in range(1, dim):
        C[m][m] = T(m - 1, m - 1) * A[0]
        for k in range(m - 1, 0, -1):
            C[m][k] = sum(A[i] * T(m - i - 1, k - 1) 
                          for i in range(m - k + 1))
    return C
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
        If the requested size > size of given table then 
        an emtpy list is returned.
    """
    def gen(n: int) -> trow:
        if n >= max:
            return []
        return T[n]
    return gen
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
            gen,  Function gen(n:int) -> list[int], defined for all n >= 0. 
            id,   The name of the triangle.
            sim,  A list of A-numbers of closley related OEIS triangles.
            invQ, is the triangle invertible? 
                  Defaults to None meaning 'I do not know'.
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
        return [list(self.gen(n)) 
                for n in range(size)]
    def rev(self, size: int) -> tabl:
        """
        Args:
            size, number of rows
        Returns:
            tabel with reversed rows
        """
        return [list(reversed(self.gen(n))) 
                for n in range(size)]
    def adtab(self, size: int) -> tabl:
        """
        Args:
            size, number of rows
        Returns:
            table of (upward) anti-diagonals
        """
        return [[self.gen(n - k - 1)[k] 
                 for k in range((n + 1) // 2)] 
                 for n in range(1, size + 1)]
    def diag(self, n: int, size: int) -> list[int]:
        """
        Args:
            n, start at row n 
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
    def sum(self, size: int) -> list[int]:
        """
        Args:
            size, number of rows to be summed
        Returns:
            The first 'size' row sums.
        """
        return [sum(self.gen(n)) 
                for n in range(size)]
    def acc(self, size: int) -> tabl:
        """
        Args:
            size, number of rows
        Returns:
            table with rows accumulated
        """
        return [list(accumulate(self.gen(n))) 
                for n in range(size)]
    def mat(self, size: int) -> tabl:
        """
        Args:
            size, number of rows
        Returns:
            matrix with generated table as lower triangle
        """
        return [[self.gen(n)[k] if k <= n else 0 
                 for k in range(size)] 
                 for n in range(size)]
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
        if self.invQ == False:
            return []
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
        row = self.gen(n)
        return sum(c * (x ** j) 
               for (j, c) in enumerate(row))
    def summap(self, s: seq, size: int) -> list[int]:
        """[sum(T(n, k) * s(k) for 0 <= k <= n) for 0 <= n < size]
           For example, if T is the binomial then this is the 
           'binomial transform'.
        Args:
            s, sequence. Recommended to be cached function.
            size, length of the returned list 
        Returns:
            Initial segment of length size of s transformed.
        """
        return [sum(self.gen(n)[k] * s(k) 
                for k in range(n + 1)) 
                for n in range(size)]
    def invmap(self, s: seq, size: int) -> list[int]:
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
        return [sum((-1)**(n-k) * self.gen(n)[k] * s(k) 
                    for k in range(n + 1)) 
                    for n in range(size)]
    def show(self, size: int) -> None:
        """Prints the first 'size' rows with row-number.
        Args:
            size, number of rows
        """
        for n in range(size):
            print([n], self.gen(n))
def SeqToString(seq: list[int], 
                maxchars: int, 
                maxterms: int, 
                sep: str=' ', 
                offset: int=0
    ) -> str:
    """
    Converts a sequence of integers into a string representation.
    Args:
        seq (list[int]): The sequence of integers to be converted.
        maxchars (int): The maximum length of the resulting string.
        maxterms (int): The maximum number of terms included.
        sep (string, optional): String seperator. Default is ' '.
        offset (int, optional): The starting index of the sequence. Defaults to 0.
    Returns:
        str: The string representation of the sequence.
    """
    seqstr = ""
    maxt = maxl = 0
    for trm in seq[offset:]:
        maxt += 1
        if maxt > maxterms:
            break
        s = str(trm) + sep
        maxl += len(s)
        if maxl > maxchars:
            break
        seqstr += s
    return seqstr
class StopWatch:
    def __init__(
        self,
        comment: str = "Elapsed time: "
    ) -> None:
        self.start_time = None
        self.text = comment
    def start(self) -> None:
        """Start a new StopWatch"""
        if self.start_time is not None:
            raise RuntimeError("Watch is running. First stop it.")
        self.start_time = time.perf_counter()
    def stop(self) -> float:
        """Stop the StopWatch, and report the elapsed time."""
        if self.start_time is None:
            raise RuntimeError("Watch is not running.")
        elapsed_time = time.perf_counter() - self.start_time
        self.start_time = None
        print(self.text.rjust(17), "{:0.4f}".format(elapsed_time), "sec")
        return elapsed_time
def QuickTiming(tabl: Table, size: int = 100) -> None:
    t = StopWatch(tabl.id)
    t.start()
    tabl.tab(size)
    t.stop()
def Benchmark(T: Callable[[int, int], int], 
              offset:int = 4, 
              size:int = 4
    ) -> list[float]:
    """Benchmark for functions computing lower triangular arrays.
    Args:
        T(n, k), function defined for n >= 0 and 0 <= k <= n.
        offset > 0, the power of two where the test starts. Defaults to 4.
        size, the length of test run. Defaults to 4.
    Returns:
        List of factors that indicate by what the computing time multiplies 
        when the number of rows doubles.
    Example:
        Benchmark(lambda n, k: n**k)
    """
    B: list[float] = []
    for s in [2 << n for n in range(offset - 1, offset + size)]:
        t = StopWatch(str(s))
        t.start()
        [[T(n, k) for k in range(n + 1)] for n in range(s)]
        B.append(t.stop())
    return [B[i + 1] / B[i] for i in range(size)]
def AnumList() -> list[str]:
    bag = []
    for tab in Tables: 
        for anum in tab.sim:
            bag.append(anum) # type: ignore
    return sorted(bag)       # type: ignore
def AnumInListQ(anum: str) -> bool:
    """Is the A-number referenced in the library?
    Args:
        A-number as string.
 
    Returns:
        If 'True' a similar sequence is probably implemented.
    """
    return anum in AnumList()
def PreView(T:Table, size: int = 8) -> None:
    """
    Args:
        T, table to inspect
        size, number of rows, defaults to 8.
    Returns:
    None. Prints the result for some example parameters.
    """
    print()
    print("NAME       ", T.id)
    print("similars   ", T.sim)
    print("invertible ", T.invQ)
    print("table      ", T.tab(size))
    print("value      ", T.val(size-1, (size-1)//2))
    print("row        ", T.row(size-1))
    print("col        ", T.col(2, size))
    print("sum        ", T.sum(size))
    print("diag       ", T.diag(2, size))
    print("poly       ", [T.poly(n, 1) for n in range(size)])
    print("antidiagtab", T.adtab(size))
    print("accumulated", T.acc(size))
    print("inverted   ", T.inv(size))
    print("reverted   ", T.rev(size))
    print("rev of inv ", T.revinv(size))
    print("inv of rev ", T.invrev(size))
    print("matrix     ", T.mat(size))
    print("flatt seq  ", T.flat(size))
    print("inv rev 11 ", T.invrev11(size-1))
    T11 = Table(T.off(1, 1), "Toffset11")
    print("1-1-based  ", T11.tab(size-1))
    print("summap     ", T.summap(lambda n: n*n, size))
    print("invmap     ", T.invmap(lambda n: n*n, size))
    print("TABLE      "); T.show(size + 2)
    print("Timing 100 rows:", end=''); QuickTiming(T)
def QuickView(prompt: bool = False) -> None:
    for T in Tables: 
        print(T.id, T.sim)
        T.show(6)
        if prompt:
            input("Hit Return/Enter > ")
    # print("Provides efficient implementations for:")
    # print(AnumList())
@cache
def abel(n: int) -> list[int]:
    if n == 0:
        return [1]
    b = binomial(n - 1)
    return [b[k - 1] * n ** (n - k) if k > 0 else 0 for k in range(n + 1)]
Abel = Table(abel, "Abel", ["A137452", "A061356", "A139526"], True)
@cache
def _andre(n: int, k: int) -> int:
    if k == 0 or n == 0: return 1 
    return -sum(Binomial.val(k, j) * _andre(n, j) for j in range(0, k, n)) 
@cache
def andre(n: int) -> list[int]:
    return [abs(_andre(k, n)) for k in range(n + 1)]
Andre = Table(andre, "Andre", ["A375555", "A181937"], True)
@cache
def F(n: int) -> int:
    return factorial(n) ** 3 * ((n + 1) * (n + 1) * (n + 2))
@cache
def baxter(n: int) -> list[int]:
    if n == 0:
        return [1]
    return [0] + [(2 * F(n - 1)) // (F(k - 1) * F(n - k)) for k in range(1, n + 1)]
Baxter = Table(baxter, "Baxter", ["A359363", "A056939"])
@cache
def bell(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = [bell(n - 1)[n - 1]] + bell(n - 1)
    for k in range(1, n + 1):
        row[k] += row[k - 1]
    return row
Bell = Table(bell, "Bell", ["A011971", "A011972", "A123346"], False)
@cache
def bessel(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    row = bessel(n - 1) + [1]
    for k in range(n - 1, 0, -1):
        row[k] = row[k - 1] + (2 * (n - 1) - k) * row[k]
    return row
Bessel = Table(bessel, "Bessel", ["A132062", "A001497", "A001498", "A122850"], True)
@cache
def bessel2(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1, 0]
    row = bessel2(n - 1) + [0]
    row[n] = 0 if n % 2 else row[n - 2]
    for k in range(2, n, 2):
        row[k] = (n * row[k]) // (n - k)
    return row
Bessel2 = Table(
    bessel2,
    "Bessel2",
    ["A359760", "A073278", "A066325", "A099174", "A111924", "A144299", "A104556"],
    False,
)
@cache
def binarypell(n: int) -> list[int]:
    if n == 0:
        return [1]
    arow = binarypell(n-1)
    row = arow + [1]
    for k in range(n-1, 0, -1):
        row[k] = arow[k - 1] + 2 * arow[k]
    row[0] = 2 * arow[0]
    return row
BinaryPell = Table(binarypell, "BinaryPell", ["A038207"], True)
@cache
def binomial(n: int) -> list[int]:
    if n == 0:
        return [1]
    row: list[int] = [1] + binomial(n - 1)
    for k in range(1, n):
        row[k] += row[k + 1]
    return row
Binomial = Table(
    binomial,
    "Binomial",
    [
        "A007318",
        "A074909",
        "A108086",
        "A117440",
        "A118433",
        "A130595",
        "A135278",
        "A154926",
    ],
    True,
)
@cache
def binomialbell(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1, 1]
    a = binomialbell(n - 1) + [1]
    s = sum(a) - 1
    for j in range(n - 1, 0, -1):
        a[j] = (a[j - 1] * n) // j
    a[0] = s
    return a
BinomialBell = Table(binomialbell, "BinomialBell", ["A056857", "A056860"], True)
@cache
def binomialcatalan(n: int) -> list[int]:
    if n == 0:
        return [1]
    a = binomialcatalan(n - 1) + [0]
    row = [0] * (n + 1)
    row[0] = 1
    row[1] = n
    for k in range(2, n + 1):
        row[k] = (a[k] * (n + k + 1) + a[k - 1] * (4 * k - 2)) // (n + 1)
    return row
BinomialCatalan = Table(binomialcatalan, "BinomialCatalan", ["A124644", "A098474"], True)
@cache
def binomialpell(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [2, 2]
    arow = binomialpell(n - 1)
    row = arow + [n + 1]
    for k in range(1, n):
        row[k] = (arow[k - 1] * (n + 1)) // k
    row[0] = 2 * arow[0] + binomialpell(n - 2)[0]
    return row
BinomialPell = Table(binomialpell, "BinomialPell", ["A367211"], True)
@cache
def binomialdiffpell(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1, 1]
    arow = binomialdiffpell(n - 1)
    row = arow + [1]
    for k in range(1, n):
        row[k] = (arow[k - 1] * n) // k
    row[0] = 2 * arow[0] + binomialdiffpell(n - 2)[0]
    return row
BinomialDiffPell = Table(binomialdiffpell, "BinomialDiffPell", ["A367564"], True)
@cache
def catalan(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    pow = catalan(n - 1) + [0]
    row = pow.copy()
    for k in range(n - 1, 0, -1):
        row[k] = pow[k - 1] + 2 * pow[k] + pow[k + 1]
    row[n] = 1
    return row
Catalan = Table(catalan, "Catalan", ["A128899", "A039598"], True)
@cache
def catalanpaths(n: int) -> list[int]:
    if n == 0:
        return [1]
    def r(k: int) -> int:
        return catalanpaths(n - 1)[k] if k >= 0 and k < n else 0
    row = catalanpaths(n - 1) + [1]
    for k in range(0, n):
        row[k] = r(k - 1) + r(k + 1)
    return row
CatalanPaths = Table(
    catalanpaths, "CatalanPaths", ["A053121", "A052173", "A112554", "A322378"], True
)
@cache
def centralcycle(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    row = centralcycle(n - 1) + [0]
    for k in range(n, 0, -1):
        row[k] = (n + k - 1) * (row[k] + row[k - 1])
    return row
CentralCycle = Table(centralcycle, "CentralCycle", ["A269940", "A111999", "A259456"], False)
@cache
def centralset(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    row = centralset(n - 1) + [1]
    for k in range(n - 1, 1, -1):
        row[k] = k**2 * row[k] + row[k - 1]
    return row
CentralSet = Table(centralset, "CentralSet", ["A269945", "A008957", "A036969"], True)
@cache
def chains(n: int) -> list[int]:
    if n == 0:
        return [1]
    ch = chains(n - 1) + [0]
    row = ch.copy()
    row[0] = 2 * ch[0]
    row[n] = n * ch[n - 1]
    for k in range(n - 1, 0, -1):
        row[k] = k * ch[k - 1] + (k + 2) * ch[k]
    return row
Chains = Table(chains, "Chains", ["A038719"], False)
@cache
def charlier(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1, -1]
    a = charlier(n - 1)
    b = [0] + charlier(n - 2)
    c = charlier(n - 1) + [(-1) ** n]
    for k in range(1, n):
        c[k] = a[k] - n * a[k - 1] - (n - 1) * b[k - 1]
    return c
Charlier = Table(charlier, "Charlier", ["A046716", "A094816"], True)
@cache
def chebyshevs(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    rov = chebyshevs(n - 2)
    row = [0] + chebyshevs(n - 1)
    for k in range(0, n - 1):
        row[k] -= rov[k]
    return row
ChebyshevS = Table(
    chebyshevs, "ChebyshevS", ["A049310", "A053119", "A112552", "A168561"], True
)
@cache
def chebyshevt(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    rov = chebyshevt(n - 2)
    row = [0] + chebyshevt(n - 1)
    row[n] = 2 * row[n]
    for k in range(0, n - 1):
        row[k] = 2 * row[k] - rov[k]
    return row
ChebyshevT = Table(chebyshevt, "ChebyshevT", ["A053120", "A039991", "A081265"], True)
@cache
def chebyshevu(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 2]
    rov = chebyshevu(n - 2)
    row = [0] + chebyshevu(n - 1)
    row[n] = 2 * row[n]
    for k in range(0, n - 1):
        row[k] = 2 * row[k] - rov[k]
    return row
ChebyshevU = Table(chebyshevu, "ChebyshevU", ["A053117", "A053118", "A115322"], True)
@cache
def _composition(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    return (
        2 * _composition(n - 1, k)
        + _composition(n - 1, k - 1)
        - 2 * _composition(n - 2, k - 1)
        + _composition(n - k - 1, k - 1)
        - _composition(n - k - 2, k)
    )
@cache
def composition(n: int) -> list[int]:
    return [_composition(n - 1, k - 1) for k in range(n + 1)]
Composition = Table(composition, "Composition", ["A048004"], True)
@cache
def compoacc(n: int) -> list[int]:
    return list(accumulate(composition(n))) 
CompoAcc = Table(compoacc, "CompositionAcc", ["A126198"], False)
@cache
def _compodist(n: int, k: int) -> int:
    if k < 0 or n < 0: return 0
    if k == 0: 
        if n==0: 
            return 1
        else:
            return 0 
    return _compodist(n - k, k) + k * _compodist(n - k, k - 1)
@cache
def compodist(n: int) -> list[int]:
    f = (sqrt(1 + 8*n) - 1) // 2
    return [_compodist(n, k) if k <= f else 0 for k in range(n + 1)]
CompoDist = Table(compodist, "CompositionDist", ["A072574", "A216652"])
@cache
def ctree(n: int) -> list[int]:
    if n % 2 == 1:
        return [1] * (n + 1)
    return [1, 0] * (n // 2) + [1]
CTree = Table(ctree, "CTree", ["A106465", "A106470"], True)
@cache
def delannoy(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1, 1]
    rov = delannoy(n - 2)
    row = delannoy(n - 1) + [1]
    for k in range(n - 1, 0, -1):
        row[k] += row[k - 1] + rov[k - 1]
    return row
Delannoy = Table(delannoy, "Delannoy", ["A008288"], True)
@cache
def divisibility(n: int) -> list[int]:
    if n == 0:
        return [1]
    L = [0 for _ in range(n + 1)]
    L[1] = L[n] = 1
    i = 1
    div = n
    while i < div:
        div, mod = divmod(n, i)
        if mod == 0:
            L[i] = L[div] = 1
        i += 1
    return L
Divisibility = Table(divisibility, "Divisibility", ["A113704", "A051731"], True)
@cache
def dist_latt(n: int, k: int) -> int:
    if k == 0 or n == 0: return 1
    return (dist_latt(n, k - 1)
          + sum(dist_latt(2 * j, k - 1) * dist_latt(n - 1 - 2 * j, k)
            for j in range(1 + (n - 1) // 2)))
@cache
def dyckpaths(n: int) -> list[int]:
    if n == 0:
        return [1]
    pow = dyckpaths(n - 1) + [0]
    row = pow.copy()
    row[0] += row[1]
    row[n] = 1
    for k in range(n - 1, 0, -1):
        row[k] = pow[k - 1] + 2 * pow[k] + pow[k + 1]
    return row
DyckPaths = Table(dyckpaths, "DyckPaths", ["A039599", "A050155"], True)
@cache
def _euclid(n: int, k: int) -> int:
    while k != 0:
        t = k
        k = n % k
        n = t
    return 1 if n == 1 else 0
@cache
def euclid(n: int) -> list[int]:
    return [_euclid(i, n) for i in range(n + 1)]
Euclid = Table(euclid, "Euclid", ["A217831"], False)
@cache
def euler(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = euler(n - 1) + [1]
    for k in range(n, 0, -1):
        row[k] = (row[k - 1] * n) // (k)
    row[0] = -sum((-1) ** (j // 2) * row[j] for j in range(n, 0, -2))
    return row
Euler = Table(euler, "Euler", ["A247453", "A109449"], True)
@cache
def KnuthEulerian(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = KnuthEulerian(n - 1) + [0]
    for k in range(n, 0, -1):
        row[k] = (n - k) * row[k - 1] + (k + 1) * row[k]
    return row
@cache
def eulerian(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    row = eulerian(n - 1) + [1]
    for k in range(n - 1, 0, -1):
        row[k] = (n - k + 1) * row[k - 1] + k * row[k]
    return row
Eulerian = Table(eulerian, "Eulerian", ["A123125", "A173018", "A008292"], True)
@cache
def eulerian2(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    row = eulerian2(n - 1) + [0]
    for k in range(n, 1, -1):
        row[k] = (2 * n - k) * row[k - 1] + k * row[k]
    return row
Eulerian2 = Table(
    eulerian2, "Eulerian2", ["A340556", "A008517", "A112007", "A163936"], False
)
@cache
def eulerianb(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = eulerianb(n - 1) + [1]
    for k in range(n - 1, 0, -1):
        row[k] = (2 * (n - k) + 1) * row[k - 1] + (2 * k + 1) * row[k]
    return row
EulerianB = Table(eulerianb, "EulerianB", ["A060187", "A138076"], True)
@cache
def eulerianzigzag(n: int) -> list[int]:
    b = binomial(n + 1)
    return [sum((-1)**j * b[j] * dist_latt(n, k - j) for j in range(k + 1))
            for k in range(n + 1)]
@cache
def ezz(n: int) -> list[int]:
    n += 2
    b = binomial(n + 1)
    return [sum((-1)**j * b[j] * dist_latt(n, k - j) for j in range(k + 1))
            for k in range(n - 1)]
EulerianZigZag = Table(eulerianzigzag, "EulerianZigZag", ["A205497"], False)
@cache
def eulersec(n: int) -> list[int]:
    if n == 0:
        return [1]
    b = binomial(n)
    row = [b[k] * eulersec(n - k)[0] if k > 0 else 0 for k in range(n + 1)]
    if n % 2 == 0:
        row[0] = -sum(row[2::2])
    return row
EulerSec = Table(eulersec, "EulerSec", ["A119879", "A081658", "A153641"], True)
def eulerS(n: int) -> int:
    return 0 if n % 2 == 1 else eulersec(n)[0]
@cache
def eulertan(n: int) -> list[int]:
    b = binomial(n)
    row = [b[k] * eulertan(n - k)[0] if k > 0 else 0 for k in range(n + 1)]
    if n % 2 == 1:
        row[0] = -sum(row[2::2]) + 1
    return row
EulerTan = Table(
    eulertan, "EulerTan", ["A162660", "A350972", "A155585", "A009006", "A000182"], False
)
def eulerT(n: int) -> int:
    return 0 if n % 2 == 0 else eulertan(n)[0]
@cache
def eytzingerorder(n: int) -> list[int]:
    row = [0] * (n + 1)
    def e_rec(k: int, i: int) -> int:
        if k <= n + 1:
            i = e_rec(2 * k, i)
            row[k - 1] = i
            i = e_rec(2 * k + 1, i + 1)
        return i
    e_rec(1, 0)
    return row
EytzingerOrder = Table(eytzingerorder, "EytzingerOrder", ["A368783"])
@cache
def eytzingerpermutation(n: int) -> list[int]:
    t = n * (n + 1) // 2
    return [eytzingerorder(n)[k] + t for k in range(n + 1)]
EytzingerPermutation = Table(eytzingerpermutation, "EytzingerPerm", ["A375469"])
@cache
def fallingfactorial(n: int) -> list[int]:
    if n == 0:
        return [1]
    r = fallingfactorial(n - 1)
    row = [n * r[k] for k in range(-1, n)]
    row[0] = 1
    return row
FallingFactorial = Table(fallingfactorial, "FallingFact",
             ["A008279", "A068424", "A094587", "A173333", "A181511"],
             False)
@cache
def fibolucas(n: int) -> list[int]:
    if n == 0: return [1]
    if n == 1: return [1, 2]
    if n == 2: return [1, 2, 1]
    rowA = fibolucas(n - 2)
    row  = fibolucas(n - 1) + [1 + n % 2]
    row[2] += 1
    for k in range(3, n):
        row[k] += rowA[k - 2]
    return row
FiboLucas = Table(fibolucas, "FiboLucas", ["A374439"], False)
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
FiboLucasInv = Table(fibolucasinv, "FiboLucasInv", ["A375025"], True)
@cache
def fibolucasrev(n: int) -> list[int]:
    if n == 0: return [1]
    return list(reversed(fibolucas(n)))
FiboLucasRev = Table(fibolucasrev, "FiboLucasRev", ["A124038"], True)
@cache
def fibonacci(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    row = fibonacci(n - 1) + [1]
    s = row[1]
    for k in range(n - 1, 0, -1):
        row[k] += row[k - 1]
    row[0] = s
    return row
Fibonacci = Table(fibonacci, "Fibonacci", ["A354267", "A105809", "A228074"], True)
@cache
def fubini(n: int) -> list[int]:
    if n == 0:
        return [1]
    def r(k: int) -> int:
        return fubini(n - 1)[k] if k <= n - 1 else 0
    row = [0] + fubini(n - 1)
    for k in range(1, n + 1):
        row[k] = k * (r(k - 1) + r(k))
    return row
Fubini = Table(fubini, "Fubini", ["A131689", "A019538", "A090582", "A278075"], False)
@cache
def fusscatalan(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    row = fusscatalan(n - 1) + [fusscatalan(n - 1)[n - 1]]
    return list(accumulate(row))
FussCatalan = Table(fusscatalan, "FussCatalan", ["A355173", "A030237", "A054445"], False)
@cache
def gaussq2(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = gaussq2(n - 1)
    pow = [1] + gaussq2(n - 1)
    p = 2
    for k in range(1, n):
        pow[k] = row[k - 1] + p * row[k]
        p *= 2
    return pow
Gaussq2 = Table(gaussq2, "Gaussq2", ["A022166"], True)
@cache
def genocchi(n: int) -> list[int]:
    if n == 0:
        return [1]
    row: list[int] = [0] + genocchi(n - 1) + [0]
    for k in range(n, 0, -1):
        row[k] += row[k + 1]
    for k in range(2, n + 2):
        row[k] += row[k - 1]
    return row[1:]
Genocchi = Table(genocchi, "Genocchi", ["A297703"], False)
@cache
def harmonic(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    row = harmonic(n - 1) + [1]
    sav = row[1]
    for k in range(n - 1, 0, -1):
        row[k] = (n - 1) * row[k] + row[k - 1]
    row[1] += sav
    return row
Harmonic = Table(harmonic, "Harmonic", ["A358694", "A109822"], True)
@cache
def hermitee(n: int) -> list[int]:
    row = [0] * (n + 1)
    row[n] = 1
    for k in range(n - 2, -1, -2):
        row[k] = (row[k + 2] * (k + 2) * (k + 1)) // (n - k)
    return row
HermiteE = Table(hermitee, "HermiteE", ["A099174", "A066325", "A073278"], True)
@cache
def hermiteh(n: int) -> list[int]:
    row = [0] * (n + 1)
    row[n] = 2**n
    for k in range(n - 2, -1, -2):
        row[k] = (row[k + 2] * (k + 2) * (k + 1)) // (2 * (n - k))
    return row
HermiteH = Table(hermiteh, "HermiteH", ["A060821"], False)
@cache
def hyperharmonic(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = hyperharmonic(n - 1) + [1]
    for m in range(n - 1, 0, -1):
        row[m] = (n - m + 1) * row[m] + row[m - 1]
    row[0] *= n
    return row
HyperHarmonic = Table(hyperharmonic, "HyperHarmonic", ["A165675", "A093905", "A105954", "A165674"], True)
@cache
def jacobsthal(n: int) -> list[int]:
    if n == 0: return [1]
    if n == 1: return [1, 1]
    if n == 2: return [1, 2, 1] 
    Jn1 = jacobsthal(n - 1) 
    Jn2 = jacobsthal(n - 2) + [0]
    row = [1] * (n + 1)
    for k in range(1, n):
        row[k] = Jn1[k-1] + Jn1[k] + 2 * Jn2[k]
    row[0] = Jn1[0] + 2 * Jn2[0]
    return row
Jacobsthal = Table(jacobsthal, "Jacobsthal", ["A322942"], True)
@cache
def kekule(n: int) -> list[int]:
    return [dist_latt(n - k, k) for k in range(n + 1)]
Kekule = Table(kekule, "Kekule", ["A050446", "A050447"], True)
@cache
def labeledgraphs(n: int) -> list[int]:
    if n == 0:
        return [1]
    s = [
        2 ** (((k - n + 1) * (k - n)) // 2)
        * Binomial.val(n - 1, k - 1)
        * labeledgraphs(k)[k]
        for k in range(1, n)
    ]
    b = 2 ** (((n - 1) * n) // 2) - sum(s)
    return [0] + s + [b]
LabeledGraphs = Table(labeledgraphs, "LabeledGraphs", ["A360603"], False)
@cache
def laguerre(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = [0] + laguerre(n - 1)
    for k in range(0, n):
        row[k] += (n + k) * row[k + 1]
    return row
Laguerre = Table(laguerre, "Laguerre", ["A021009", "A021010", "A144084"], True)
@cache
def lah(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = lah(n - 1) + [1]
    row[0] = 0
    for k in range(n - 1, 0, -1):
        row[k] = row[k] * (n + k - 1) + row[k - 1]
    return row
Lah = Table(
    lah, "Lah", ["A271703", "A008297", "A066667", "A089231", "A105278", "A111596"], True
)
@cache
def t(n: int, k: int, m: int) -> int:
    if k < 0 or n < 0:
        return 0
    if k == 0:
        return n**k
    return m * t(n, k - 1, m) + t(n - 1, k, m + 1)
@cache
def lehmer(n: int) -> list[int]:
    return [t(k - 1, n - k, n - k) if n != k else 1 for k in range(n + 1)]
Lehmer = Table(lehmer, "Lehmer", ["A354794", "A039621"], True)
@cache
def leibniz(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = leibniz(n - 1) + [n + 1]
    row[0] = row[n] = n + 1
    for k in range(1, n):
        row[k] = ((n - k + 1) * row[k - 1]) // k
    return row
Leibniz = Table(leibniz, "Leibniz", ["A003506"], False)
@cache
def leibnizscheme(n: int) -> list[int]:
    if n == 0: return [0]
    L = leibnizscheme(n - 1)
    return [L[k] + k for k in range(n)] + [n]
LeibnizScheme = Table(leibnizscheme, "LeibnizScheme", ["A003991"]) 
@cache
def levin(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = levin(n - 1) + [1]
    row[0] = row[n] = (row[n - 1] * (4 * n - 2)) // n
    for k in range(1, n):
        row[k] = ((n - k + 1) * row[k - 1]) // k
    return row
Levin = Table(levin, "Levin", ["A356546"], False)
@cache
def lozanic(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = [1] + lozanic(n - 1)
    for k in range(1, n):
        row[k] += row[k + 1]
    if n % 2 != 0:
        return row
    b = binomial(n // 2 - 1)
    for k in range(1, n, 2):
        row[k] -= b[(k - 1) // 2]
    return row
Lozanic = Table(lozanic, "Lozanic", ["A034851"], True)
@cache
def lucas(n: int) -> list[int]:
    if n == 0: return [2]
    if n == 1: return [1, 2]
    row = lucas(n - 1) + [0]
    for k in range(n, 0, -1):
        row[k] += row[k - 1]
    return row
Lucas = Table(lucas, "Lucas", ["A029635", "A029653"])
@cache
def lucaspoly(n: int) -> list[int]:
    if n == 0: return [1]
    if n == 1: return [1, 0]
    if n == 2: return [1, 1, 1]
    rowA = lucaspoly(n - 2)
    row  = lucaspoly(n - 1) + [(n + 1) % 2]
    row[1] += 1
    for k in range(3, n):
        row[k] += rowA[k - 2]
    return row
LucasPoly = Table(lucaspoly, "LucasPoly", ["A374440"], False)
@cache
def _moebius(n: int) -> int:
    if n == 1:
        return 1
    if n == 2:
        return -1
    return -sum(_moebius(k) for k, i in enumerate(divisibility(n)[: n - 1]) if i != 0)
@cache
def moebius(n: int) -> list[int]:
    if n == 0:
        return [1]
    r = [0 for _ in range(n + 1)]
    r[n] = 1
    for k in range(1, n):
        if n % k == 0:
            r[k] = _moebius(n // k)
    return r
Moebius = Table(moebius, "Moebius", ["A363914", "A054525"], True)
@cache
def monotone(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = [1 for _ in range(n + 1)]
    row[1] = n
    for k in range(1, n):
        row[k + 1] = (row[k] * (n + k)) // (k + 1)
    return row
Monotone = Table(monotone, "Monotone", ["A059481", "A027555"], True)
@cache
def motzkin(n: int) -> list[int]:
    if n == 0:
        return [1]
    def r(k: int) -> int:
        return motzkin(n - 1)[k] if k >= 0 and k < n else 0
    row = motzkin(n - 1) + [1]
    for k in range(0, n):
        row[k] += r(k - 1) + r(k + 1)
    return row
Motzkin = Table(motzkin, "Motzkin", ["A064189", "A026300", "A009766"], True)
@cache
def motzkinpoly(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1, 0]
    h = 0 if n % 2 else (motzkinpoly(n - 2)[n - 2] * 2 * (n - 1)) // (n // 2 + 1)
    row = motzkinpoly(n - 1) + [h]
    for k in range(2, n, 2):
        row[k] = (n * row[k]) // (n - k)
    return row
MotzkinPoly = Table(motzkinpoly, "MotzkinPoly", ["A359364"], False)
@cache
def narayana(n: int) -> list[int]:
    if n < 3:
        return [[1], [0, 1], [0, 1, 1]][n]
    a = narayana(n - 2) + [0, 0]
    row = narayana(n - 1) + [1]
    for k in range(n - 1, 1, -1):
        row[k] = (
            (row[k] + row[k - 1]) * (2 * n - 1)
            - (a[k] - 2 * a[k - 1] + a[k - 2]) * (n - 2)
        ) // (n + 1)
    return row
Narayana = Table(narayana, "Narayana", ["A090181", "A001263", "A131198"], True)
@cache
def naturals(n: int) -> list[int]:
    R = range((n * (n + 1)) // 2, ((n + 1) * (n + 2)) // 2)
    return [i + 1 for i in R]
Naturals = Table(naturals, "Naturals", ['A000027', 'A001477'], True)
@cache
def nicomachus(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = nicomachus(n - 1) + [3 * nicomachus(n - 1)[n - 1]]
    for k in range(0, n):
        row[k] *= 2
    return row
Nicomachus = Table(nicomachus, "Nicomachus", ["A036561", "A081954", "A175840"], False)
@cache
def nimsum(n: int) -> list[int]:
    return [k^(n - k) for k in range(n + 1)]
NimSum = Table(nimsum, "NimSum", ["A003987"], False)
@cache
def one(n: int) -> list[int]:
    if n == 0:
        return [1]
    return one(n - 1) + [1]
One = Table(one, "One", ["A000012", "A008836", "A014077"], True)
@cache
def ordinals(n: int) -> list[int]:
    if n == 0:
        return [0]
    return ordinals(n - 1) + [n]
Ordinals = Table(
    ordinals, "Ordinals", ["A002262", "A002260", "A004736", "A025581"], False
)
@cache
def orderedcycle(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    row = orderedcycle(n - 1) + [0]
    row[n] = row[n] * n
    for k in range(n, 0, -1):
        row[k] = (n - 1) * row[k] + k * row[k - 1]
    return row
OrderedCycle = Table(orderedcycle, "OrderedCycle", ["A225479", "A048594", "A075181"], False)
@cache
def A(n: int, k: int) -> int:
    if n == 0: return int(k == 0)
    if k > n: n, k = k, n
    b = binomial(k + 1)
    return k * A(n - 1, k) + sum(b[j + 1] * A(n - 1, k - j)
                             for j in range(1, k + 1))
@cache
def parades(n: int) -> list[int]:
    return [A(n - k, k) for k in range(n + 1)]
Parades = Table(parades, "Parades", ["A371761", "A272644"], False)
@cache
def part(n: int, k: int) -> int:
    if k < 0 or n < 0:
        return 0
    if k == 0:
        return 1 if n == 0 else 0
    return part(n - 1, k - 1) + part(n - k, k)
@cache
def partition(n: int) -> list[int]:
    return [part(n, k) for k in range(n + 1)]
Partition = Table(partition, "Partition", ["A072233", "A008284", "A058398"], True)
@cache
def partacc(n: int) -> list[int]:
    return list(accumulate(partition(n)))
PartAcc = Table(partacc, "PartitionAcc", ["A026820", "A058400"], False)
@cache
def _partdist(n: int, k: int) -> int:
    if k < 1 or n < k: return 0
    if n == 1: return 1
    return _partdist(n - k, k) + _partdist(n - k, k - 1) 
@cache
def partdist(n: int) -> list[int]:
    if n == 0: return [1]
    f = (sqrt(1 + 8*n) - 1) // 2
    return [_partdist(n, k) if k <= f else 0 for k in range(n + 1)]
PartDist = Table(partdist, "PartitionDist", ["A008289"], False)
@cache
def _partdistsize(n: int, k: int, r: int) -> int:
    if n == 0:
        return 1 if k == 0 else 0
    if k == 0 or r == 0:
        return 0
    if k > n // 2 + 1: return 0
    return (sum(_partdistsize(n - r * j, k - 1, r - 1) 
            for j in range(1, n // r + 1))
           + _partdistsize(n, k, r - 1))
@cache
def partdistsize(n: int) -> list[int]:
    f = (sqrt(1 + 8*n) - 1) // 2
    return [_partdistsize(n, k, n) if k <= f else 0 for k in range(n + 1)]
PartDistSize = Table(partdistsize, "PartitionDistSize", ["A365676", "A116608", "A060177"], False)
@cache
def pascal(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = [1] + pascal(n - 1)
    for k in range(1, n):
        row[k] += row[k + 1]
    return row
Pascal = Table(
    pascal,
    "Pascal",
    [
        "A007318",
        "A074909",
        "A108086",
        "A117440",
        "A118433",
        "A130595",
        "A135278",
        "A154926",
    ],
    True,
)
@cache
def divisors(n: int) -> list[int]:
    return [d for d in range(n, 0, -1) if n % d == 0]
@cache
def h(n: int, k: int) -> int:
    return sum(d * T(d, k) for d in divisors(n))
@cache
def H(n: int, k: int) -> int:
    return sum(d * T(d, k) for d in divisors(n) if k <= d)
@cache
def e(n: int, k: int) -> int:
    return sum(d * T(d, k) for d in divisors(n) if k == d)
@cache
def T(n: int, k: int) -> int:
    if n == 1: return int(k > 0)
    return sum(T(i, k) * h(n - i, k - 1) for i in range(1, n)
           ) // (n - 1)
@cache
def polyatreeacc(n: int) -> list[int]:
    return [T(n + 1, k + 1) for k in range(n + 1)]
PolyaTreeAcc = Table(polyatreeacc, "PolyaTreeAcc", ["A375467"])
@cache
def polyatree(n: int) -> list[int]:
    p = polyatreeacc(n)
    return [int(n < 1)] + [p[k] - p[k-1] for k in range(1, n + 1)]
PolyaTree = Table(polyatree, "PolyaTree", ["A034781"])
@cache
def polygonal(n: int) -> list[int]:
    if n == 0:
        return [0]
    if n == 1:
        return [0, 1]
    rov = polygonal(n - 2)
    row = polygonal(n - 1) + [n]
    row[n - 1] += row[n - 2]
    for k in range(2, n - 1):
        row[k] += row[k] - rov[k]
    return row
Polygonal = Table(
    polygonal, "Polygonal", ["A139600", "A057145", "A134394", "A139601"], False
)
@cache
def powlaguerre(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = powlaguerre(n - 1) + [1]
    row[0] = row[n] = row[0] * n
    for k in range(1, n):
        row[k] = ((n - k + 1) * row[k - 1]) // k
    return row
PowLaguerre = Table(powlaguerre, "PowLaguerre", ["A196347", "A021012"], False)
@cache
def rencontres(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    row = [
        (n - 1) * (rencontres(n - 1)[0] + rencontres(n - 2)[0])
    ] + rencontres(n - 1)
    for k in range(1, n - 1):
        row[k] = (n * row[k]) // k
    return row
Rencontres = Table(rencontres, "Rencontres", ["A008290", "A098825"], True)
@cache
def risingfactorial(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = [1 for _ in range(n + 1)]
    row[1] = n
    for k in range(1, n):
        row[k + 1] = row[k] * (n + k)
    return row
RisingFactorial = Table(risingfactorial, "RisingFact", ["A124320"], False)
@cache
def rootedtree(n: int) -> list[int]:
    p = polyatreeacc(n)
    return [0] + [p[k + 1] - p[k] for k in range(n)]
RootedTree = Table(rootedtree, "RootedTree", ["A034781"])
@cache
def schroeder(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    row = schroeder(n - 1) + [1]
    for k in range(n - 1, 0, -1):
        row[k] += row[k - 1] + row[k + 1]
    return row
Schroeder = Table(
    schroeder,
    "Schroeder",
    ["A122538", "A033877", "A080245", "A080247", "A106579"],
    True,
)
@cache
def schroederpaths(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = schroederpaths(n - 1) + [1]
    for k in range(n, 0, -1):
        row[k] = (row[k - 1] * (2 * n - k)) // k
    row[0] = (row[0] * (4 * n - 2)) // n
    return row
SchroederPaths = Table(schroederpaths, "SchroederP", ["A104684", "A063007"], True)
@cache
def schroederl(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1, 1]
    arow = schroederl(n - 1) + [0]
    row = schroederl(n - 1) + [1]
    row[0] = row[0] + 2 * row[1]
    for k in range(1, n):
        row[k] = arow[k - 1] + 3 * arow[k] + 2 * arow[k + 1]
    return row
SchroederL = Table(schroederl, "SchroederL", ["A172094"], True)
@cache
def seidel(n: int) -> list[int]:
    if n == 0:
        return [1]
    rowA = seidel(n - 1)
    row = [0] + seidel(n - 1)
    row[1] = row[n]
    for k in range(2, n + 1):
        row[k] = row[k - 1] + rowA[n - k]
    return row
Seidel = Table(seidel, "Seidel", ["A008281", "A008282", "A010094"], False)
def seidelboust(n: int) -> list[int]:
    return seidel(n) if n % 2 else seidel(n)[::-1]
SeidelBoust = Table(
    seidelboust, "SeidelBoust", ["A008280", "A108040", "A236935", "A239005"], False
)
@cache
def sierpinski(n: int) -> list[int]:
    return [int(not ~n & k) for k in range(n + 1)]
Sierpinski = Table(
    sierpinski,
    "Sierpinski",
    ["A047999", "A090971", "A114700", "A143200", "A166282"],
    True,
)
@cache
def stirlingcycle(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = [0] + stirlingcycle(n - 1)
    for k in range(1, n):
        row[k] = row[k] + (n - 1) * row[k + 1]
    return row
StirlingCycle = Table(
    stirlingcycle,
    "StirlingCycle",
    ["A132393", "A008275", "A008276", "A048994", "A054654", "A094638", "A130534"],
    True,
)
@cache
def stirlingcycle2(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 0]
    rov = stirlingcycle2(n - 2)
    row = stirlingcycle2(n - 1) + [0]
    for k in range(1, n // 2 + 1):
        row[k] = (n - 1) * (rov[k - 1] + row[k])
    return row
StirlingCycle2 = Table(
    stirlingcycle2, "StirlingCyc2", ["A358622", "A008306", "A106828"], False
)
@cache
def stirlingcycleb(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = stirlingcycleb(n - 1) + [1]
    m = 2 * n - 1
    for k in range(n - 1, 0, -1):
        row[k] = m * row[k] + row[k - 1]
    row[0] *= m
    return row
StirlingCycleB = Table(
    stirlingcycleb, "StirlingCycB", ["A028338", "A039757", "A039758", "A109692"], True
)
@cache
def stirlingset(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = [0] + stirlingset(n - 1)
    for k in range(1, n):
        row[k] = row[k] + k * row[k + 1]
    return row
StirlingSet = Table(
    stirlingset,
    "StirlingSet",
    [
        "A048993",
        "A008277",
        "A008278",
        "A080417",
        "A106800",
        "A151511",
        "A151512",
        "A154959",
        "A213735",
    ],
    True,
)
@cache
def stirlingset2(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 0]
    rov = stirlingset2(n - 2)
    row = stirlingset2(n - 1) + [0]
    for k in range(1, n // 2 + 1):
        row[k] = (n - 1) * rov[k - 1] + k * row[k]
    return row
StirlingSet2 = Table(stirlingset2, "StirlingSet2", ["A358623", "A008299", "A137375"], False)
@cache
def stirlingsetb(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1, 1]
    pow = stirlingsetb(n - 1)
    row = stirlingsetb(n - 1) + [1]
    row[0] += 2 * row[1]
    for k in range(1, n - 1):
        row[k] = 2 * (k + 1) * pow[k + 1] + (2 * k + 1) * pow[k] + pow[k - 1]
    row[n - 1] = (2 * n - 1) * pow[n - 1] + pow[n - 2]
    return row
StirlingSetB = Table(stirlingsetb, "StirlingSetB", ["A154602"], True)
@cache
def sylvester(n: int) -> list[int]:
    def s(n: int, k: int) -> int:
        return sum(
            Binomial.val(n, k - j) * StirlingCycle.val(n - k + j, j) for j in range(k + 1)
        )
    return [s(n, k) for k in range(n + 1)]
Sylvester = Table(sylvester, "Sylvester", ["A341101"], False)
@cache
def ternarytree(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    row = ternarytree(n - 1) + [ternarytree(n - 1)[n - 1]]
    return list(accumulate(accumulate(row)))
TernaryTree = Table(ternarytree, "TernaryTrees", ["A355172"], False)
@cache
def wardset(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    row = wardset(n - 1) + [0]
    for k in range(n, 0, -1):
        row[k] = k * row[k] + (n + k - 1) * row[k - 1]
    return row
WardSet = Table(wardset, "WardSet", ["A269939", "A134991"], False)
@cache
def wardcycle(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    row = wardcycle(n - 1) + [0]
    for k in range(n, 0, -1):
        row[k] = (n + k - 1) * (row[k - 1] + row[k])
    return row
WardCycle = Table(wardcycle, "WardCycle", ["A269940", "A111999", "A259456"], False)
@cache
def worpitzky(n: int) -> list[int]:
    if n == 0:
        return [1]
    row = worpitzky(n - 1) + [0]
    for k in range(n, 0, -1):
        row[k] = k * row[k - 1] + (k + 1) * row[k]
    return row
Worpitzky = Table(
    worpitzky, "Worpitzky",
    ["A028246", "A053440", "A075263", "A130850", "A163626"], 
    False)
def bell_num(n: int) -> int:
    if n == 0:
        return 1
    return bell(n - 1)[-1]
def Bernoulli(n: int) -> Fraction:
    if n < 2:
        return Fraction(1, n + 1)
    if n % 2 == 1:
        return Fraction(0, 1)
    g = genocchi(n // 2 - 1)[-1]
    f = Fraction(g, 2 ** (n + 1) - 2)
    return -f if n % 4 == 0 else f
def euler_num(n: int) -> int:
    return euler(n)[0]
@cache
def eulerphi(n: int) -> int:
    return sum(k * moebius(n)[k] for k in range(n + 1))
def motzkin_num(n: int) -> int:
    return sum(motzkinpoly(n))
def partlist_num(n: int) -> int:
    return sum(lah(n))
def part_num(n: int) -> int:
    return sum(partition(n))
def riordan_num(n: int) -> int:
    return sum((-1) ** (n - k) * BinomialCatalan.val(n, k) for k in range(n + 1))
Tables: list[Table] = [
    Abel,
    Andre,
    Baxter,
    Bell,
    Bessel,
    Bessel2,
    BinaryPell,
    Binomial,
    BinomialBell,
    BinomialCatalan,
    BinomialPell,
    BinomialDiffPell,
    Catalan,
    CatalanPaths,
    CentralCycle,
    CentralSet,
    Chains,
    Charlier,
    ChebyshevS,
    ChebyshevT,
    ChebyshevU,
    Composition,
    CompoAcc,
    CompoDist,
    CTree,
    Delannoy,
    Divisibility,
    DyckPaths,
    Euclid,
    Euler,
    Eulerian,
    Eulerian2,
    EulerianB,
    EulerianZigZag,
    EulerSec,
    EulerTan,
    EytzingerOrder,
    EytzingerPermutation,
    FallingFactorial,
    FiboLucas,
    FiboLucasInv,
    FiboLucasRev,
    Fibonacci,
    Fubini,
    FussCatalan,
    Gaussq2,
    Genocchi,
    Harmonic,
    HermiteE,
    HermiteH,
    HyperHarmonic,
    Jacobsthal,
    Kekule,
    LabeledGraphs,
    Laguerre,
    Lah,
    Lehmer,
    Leibniz,
    LeibnizScheme,
    Levin,
    Lozanic,
    Lucas,
    LucasPoly,
    Moebius,
    Monotone,
    Motzkin,
    MotzkinPoly,
    Narayana,
    Naturals,
    Nicomachus,
    NimSum,
    One,
    Ordinals,
    OrderedCycle,
    Parades,
    Partition,
    PartAcc,
    PartDist,
    PartDistSize,
    Pascal,
    PolyaTreeAcc,
    PolyaTree,
    Polygonal,
    PowLaguerre,
    Rencontres,
    RisingFactorial,
    RootedTree,
    Schroeder,
    SchroederL,
    SchroederPaths,
    Seidel,
    SeidelBoust,
    Sierpinski,
    StirlingCycle,
    StirlingCycle2,
    StirlingCycleB,
    StirlingSet,
    StirlingSet2,
    StirlingSetB,
    Sylvester,
    TernaryTree,
    WardSet,
    WardCycle,
    Worpitzky,
]
# QuickView()