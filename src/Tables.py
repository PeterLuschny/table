from functools import cache
from itertools import accumulate, islice
from more_itertools import difference, flatten
from functools import reduce
from math import factorial, sqrt, lcm, gcd
from fractions import Fraction
import operator
import time
from pathlib import Path
import requests
import json
from requests import get
from sys import setrecursionlimit, set_int_max_str_digits
from typing import Callable, TypeAlias, Iterator, Dict, Tuple

setrecursionlimit(3000)
set_int_max_str_digits(5000)
path = Path(__file__).parent.parent
strippedpath = (path / "data/stripped").resolve()
oeisnamespath = (path / "data/names").resolve()


def GetRoot(name: str = "") -> Path:
    return (path / name).resolve()


def GetData(name: str) -> Path:
    relpath = f"data/{name}"
    return (path / relpath).resolve()


def GetDataPath(name: str, fix: str) -> Path:
    relpath = f"data/{fix}/{name}.{fix}"
    return (path / relpath).resolve()


def MakeDirectory(dir: Path) -> None:
    """Checks if a path exists, and if not,
    creates the new path."""
    Path(dir).mkdir(parents=True, exist_ok=True)


def EnsureDataDirectories() -> None:
    MakeDirectory(GetRoot("data/csv"))
    MakeDirectory(GetRoot("data/db"))
    MakeDirectory(GetRoot("data/html"))
    MakeDirectory(GetRoot("data/md"))


def InvertMatrix(L: list[list[int]], check: bool = True) -> list[list[int]]:
    """
    Calculates the inverse of a lower triangular matrix.
    Args:
        The lower triangular matrix to be inverted.
        Check whether the inverse exists as an integer matrix, default is True.
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
                    return []
                a, r = divmod(a, b)  # make sure that a is integer
                if r != 0:
                    return []
    return [row[0 : n + 1] for n, row in enumerate(inv)]


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
    A = [seq(i) for i in range(1, dim)]  # Cache the input sequence.
    # print("In:", A)
    C = [[0 for _ in range(m + 1)] for m in range(dim)]
    C[0][0] = 1
    for m in range(1, dim):
        C[m][m] = C[m - 1][m - 1] * A[0]
        for k in range(m - 1, 0, -1):
            C[m][k] = sum(A[i] * C[m - i - 1][k - 1] for i in range(m - k + 1))
    return C


def ConvTriangle(
    T: Callable[[int, int], int], seq: Callable[[int], int], dim: int = 10
) -> list[list[int]]:
    A = [seq(i) for i in range(1, dim)]  # Cache the input sequence.
    # print("In:", A)
    C = [[0 for _ in range(m + 1)] for m in range(dim)]
    C[0][0] = 1
    for m in range(1, dim):
        C[m][m] = T(m - 1, m - 1) * A[0]
        for k in range(m - 1, 0, -1):
            C[m][k] = sum(A[i] * T(m - i - 1, k - 1) for i in range(m - k + 1))
    return C


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
        sim: list[str] = [""],
        invQ: bool | None = None,
        tex: str = "",
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
        self.gen = gen
        self.id = id
        self.sim = sim
        self.invQ = invQ
        self.tex = tex

    def __getitem__(self, n: int) -> list[int]:
        return self.gen(n)

    def itr(self, size: int) -> Iterator[list[int]]:
        return islice(iter(self.tab(size)), size)

    def tab(self, size: int) -> tabl:
        """
        Args:
            size, number of rows
        Returns:
            table generated
        """
        return [list(self.gen(n)) for n in range(size)]

    def mat(self, size: int) -> tabl:
        """
        Args:
            size, number of rows and columns
        Returns:
            matrix with generated table as lower triangle
        """
        return [
            [self.gen(n)[k] if k <= n else 0 for k in range(size)] for n in range(size)
        ]

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
        return [self.gen(n - k)[k] for k in range((n + 2) // 2)]

    def alt(self, n: int) -> trow:
        return [(-1) ** k * term for k, term in enumerate(self.gen(n))]

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
        return [self.gen(n)[k] for n in range(size) for k in range(n + 1)]

    def inv(self, size: int) -> tabl:
        """
        Args:
            size, number of rows
        Returns:
            inverse table
        """
        if not self.invQ:
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
        Subtriangle based in (N, K).
        Args:
            N, shifts row-offset by N
            K, shifts column-offset by K
        Returns:
            row generator of shifted table
        """

        def subgen(n: int) -> trow:
            return self.gen(n + N)[K : N + n + 1]

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
        M = [list(self.off(1, 1)(n)) for n in range(size)]
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
        return sum(c * (x**j) for (j, c) in enumerate(self.gen(n)))

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
        return [sum(self.gen(n)[k] * s(k) for k in range(n + 1)) for n in range(size)]

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
        return [
            sum((-1) ** (n - k) * self.gen(n)[k] * s(k) for k in range(n + 1))
            for n in range(size)
        ]

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


def SeqToString(
    seq: list[int],
    maxchars: int,
    maxterms: int,
    sep: str = " ",
    offset: int = 0,
    absval: bool = False,
) -> str:
    """
    Converts a sequence of integers into a string representation.
    Args:
        seq: The sequence of integers to be converted.
        maxchars: The maximum length of the resulting string.
        maxterms: The maximum number of terms included.
        sep: String seperator. Default is ' '.
        offset: The starting index of the sequence. Defaults to 0.
        absval: Use the absolute value of the terms. Defaults to False.
    Returns:
        str: The string representation of the sequence.
    """
    seqstr = ""
    maxt = maxl = 0
    for trm in seq[offset:]:
        maxt += 1
        if maxt > maxterms:
            break
        if absval:
            s = str(abs(trm)) + sep
        else:
            s = str(trm) + sep
        maxl += len(s)
        if maxl > maxchars:
            break
        seqstr += s
    return seqstr


class StopWatch:
    def __init__(self, comment: str = "Elapsed time: ") -> None:
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


def Benchmark(
    T: Callable[[int, int], int], offset: int = 4, size: int = 4
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
            bag.append(anum)  # type: ignore
    return sorted(bag)  # type: ignore


def AnumInListQ(anum: str) -> bool:
    """Is the A-number referenced in the library?
    Args:
        A-number as string.
    Returns:
        If 'True' a similar sequence is probably implemented.
    """
    return anum in AnumList()


def PreView(T: Table, size: int = 7) -> None:
    """
    Args:
        T, table to inspect
        size, number of rows, defaults to 7.
    Returns:
    None. Prints the result for some example parameters.
    """
    print()
    print("NAME       ", T.id)
    print("similars   ", T.sim)
    print("invertible ", T.invQ)
    print("value      ", T.val(size - 1, (size - 1) // 2))
    print("row        ", T.row(size - 1))
    print("col        ", T.col(2, size))
    print("sum        ", T.sum(size))
    print("diag       ", T.diag(2, size))
    print("poly       ", [T.poly(n, 1) for n in range(size)])
    print("table      ", T.tab(size))
    print("accumulated", T.acc(size))
    print("firstdiff  ", T.diff(size))
    print("derivative ", T.der(size))
    print("reverted   ", T.rev(size))
    print("inverted   ", T.inv(size))
    print("antidiagtab", T.antidiag(size))
    print("rev of inv ", T.revinv(size))
    print("inv of rev ", T.invrev(size))
    print("matrix     ", T.mat(size))
    print("flatt seq  ", T.flat(size))
    print("inv rev 11 ", T.invrev11(size - 1))
    print("rev inv 11 ", T.revinv11(size - 1))
    T11 = Table(T.off(1, 1), "Toffset11")
    print("1-1-based  ", T11.tab(size - 1))
    print("trans      ", T.trans(lambda n: n * n, size))
    print("invtrans   ", T.invtrans(lambda n: n * n, size))
    print("TABLE      ")
    T.show(size + 2)
    print("Timing 100 rows:", end="")
    QuickTiming(T)


def QuickView(prompt: bool = False) -> None:
    for T in Tables:
        print(T.id, T.sim)
        T.show(6)
        if prompt:
            input("Hit Return/Enter > ")


def lcsubstr(s: str, t: str) -> tuple[int, int]:
    """
    The longest common substring of s and t that is contiguous.
    Returns:
        (s, l): The matched substring starts at 's' and has lenght 'l'.
    """
    m = [[0] * (1 + len(t)) for _ in range(1 + len(s))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s)):
        for y in range(1, 1 + len(t)):
            if s[x - 1] == t[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    # lcs_str =  s[x_longest - longest : x_longest]
    return (x_longest - longest, longest)


def QueryOEIS(
    seqlist: list[int], maxnum: int = 1, info: bool = False, minlen: int = 24
) -> tuple[int, int, int]:
    """
    Query if a given sequence is present in the OEIS. At least 24 terms of
    the sequence must be given. The first three terms and signs are disregard.
    Sequences with huge terms might have to few terms to give reliable results.
    This is a heuristic function, understand it's limited reach.
    Args:
        seqlist: The sequence to search. Must have at least 24 terms.
        maxnum: max number of sequences to be returned. Defaults to 1.
        info: Prints details, otherwise is quiet except for warnings. Defaults to False.
        minlen: At least {minlen} terms are required.
    Returns:
        Returns a triple (anum, sl, dl) of integers:
        - anum is the A-number of the sequence,
        - sl is the number is of unmatched terms at the start of the sequence,
        - dl is the number of the matched terms.
        Returns (0, 0, 0) if the sequence was not found.
        If sl < 5 and dl > 12, then anum probably matches the sequence,
        modulo a couple of first terms and the signs.
    Raises:
        Exception: If the OEIS server cannot be reached after multiple attempts.
    """
    if len(seqlist) < minlen:
        print(f"Sequence is too short! We require at least {minlen} terms.")
        print("You provided:", seqlist)
        return (0, 0, 0)
    # Warning. These 'magical' constants are very sensible!
    seqstr = SeqToString(seqlist, 180, 25, ",", 3, True)
    url = f"https://oeis.org/search?q={seqstr}&fmt=json"
    for _ in range(3):
        time.sleep(0.5)  # give the OEIS server some time to relax
        try:
            jdata: None | list[dict[str, int | str | list[str]]] = get(
                url, timeout=20
            ).json()
            if jdata == None:
                if 0 == sum(seqlist[::2]) or 0 == sum(seqlist[1::2]):
                    seqlist = [k for k in seqlist if k != 0]
                    seqstr = SeqToString(seqlist, 180, 25, ",", 3, True)
                    if info:
                        print("Searching list without zeros:", seqstr)
                    url = f"https://oeis.org/search?q={seqstr}&fmt=json"
                    raise ValueError("Try again")
                if info:
                    print("Sorry, no match found for:", seqstr)
                return (0, 0, 0)
            number = sl = dl = ol = 0
            for j in range(min(maxnum, len(jdata))):
                seq = jdata[j]
                number = seq["number"]
                anumber = f"A{(6 - len(str(number))) * '0' + str(number)}"
                name = seq["name"]
                data = seq["data"].replace("-", "")  # type: ignore
                seqstr = SeqToString(seqlist, 600, 25, ",", 0, True)
                start, length = lcsubstr(data, seqstr)  # type: ignore
                ol = data.count(",")  # type: ignore
                sl = data.count(",", 0, start)  # type: ignore
                dl = data.count(",", start, start + length)  # type: ignore
                if dl < 12:
                    print(f"\n*** WARNING! Only {dl} out of {ol} terms match! ***\n")
                if info or dl < 12:
                    print("You searched:", seqstr)
                    print("OEIS-data is:", data)  # type: ignore
                    print(
                        f"Starting at index {sl} the next {dl} consecutive terms match. The matched substring starts at {start} and has length {length}."
                    )
                    print("*** Found:", anumber, name)
                if dl > 12:
                    break
            return (int(number), int(sl), int(dl))  # type: ignore
        except ValueError:
            continue
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
    raise Exception(f"Could not open {url}.")


def dotproduct(vec: list[int], tor: list[int]) -> int:
    """Returns the dot product of the two vectors."""
    return sum(map(operator.mul, vec, tor))


def Triangle(T: Table, size: int = 7) -> list[int]:
    return T.flat(size)


def Trev(T: Table, size: int = 7) -> list[int]:
    return list(flatten([T.rev(n) for n in range(size)]))


def Tinv(T: Table, size: int = 7) -> list[int]:
    return list(flatten(T.inv(size)))


def Trevinv(T: Table, size: int = 7) -> list[int]:
    return list(flatten(T.revinv(size)))


def Tinvrev(T: Table, size: int = 7) -> list[int]:
    return list(flatten(T.invrev(size)))


def Toff11(T: Table, size: int = 7) -> list[int]:
    T11 = Table(T.off(1, 1), T.id + "off11")
    return T11.flat(size)


def Trev11(T: Table, size: int = 7) -> list[int]:
    return list(flatten([T.rev11(n) for n in range(size)]))


def Tinv11(T: Table, size: int = 7) -> list[int]:
    InvT11 = T.inv11(size)
    return list(flatten(InvT11))


def Trevinv11(T: Table, size: int = 7) -> list[int]:
    return list(flatten(T.revinv11(size)))


def Tinvrev11(T: Table, size: int = 7) -> list[int]:
    InvrevT11 = T.invrev11(size)
    return list(flatten(InvrevT11))


def Talt(T: Table, size: int = 7) -> list[int]:
    return list(flatten([T.alt(n) for n in range(size)]))


def Tacc(T: Table, size: int = 7) -> list[int]:
    return list(flatten([T.acc(n) for n in range(size)]))


def Tdiff(T: Table, size: int = 7) -> list[int]:
    return list(flatten([T.diff(n) for n in range(size)]))


def Tder(T: Table, size: int = 7) -> list[int]:
    return list(flatten([T.der(n) for n in range(size)]))


def Tantidiag(T: Table, size: int = 9) -> list[int]:
    return list(flatten([T.antidiag(n) for n in range(size)]))


def TablCol(T: Table, j: int, size: int = 28) -> list[int]:
    return [T.gen(j + k)[j] for k in range(size)]


def TablCol0(T: Table, size: int = 28) -> list[int]:
    return [T.gen(k)[0] for k in range(size)]


def TablCol1(T: Table, size: int = 28) -> list[int]:
    return [T.gen(1 + k)[1] for k in range(size)]


def TablCol2(T: Table, size: int = 28) -> list[int]:
    return [T.gen(2 + k)[2] for k in range(size)]


def TablCol3(T: Table, size: int = 28) -> list[int]:
    return [T.gen(3 + k)[3] for k in range(size)]


def TablDiag(T: Table, j: int, size: int = 28) -> list[int]:
    return [T.gen(j + k)[k] for k in range(size)]


def TablDiag0(T: Table, size: int = 28) -> list[int]:
    return [T.gen(k)[k] for k in range(size)]


def TablDiag1(T: Table, size: int = 28) -> list[int]:
    return [T.gen(1 + k)[k] for k in range(size)]


def TablDiag2(T: Table, size: int = 28) -> list[int]:
    return [T.gen(2 + k)[k] for k in range(size)]


def TablDiag3(T: Table, size: int = 28) -> list[int]:
    return [T.gen(3 + k)[k] for k in range(size)]


def PolyRow(T: Table, row: int, size: int = 28) -> list[int]:
    return [T.poly(row, x) for x in range(size)]


def PolyRow1(T: Table, size: int = 28) -> list[int]:
    return [T.poly(1, x) for x in range(size)]


def PolyRow2(T: Table, size: int = 28) -> list[int]:
    return [T.poly(2, x) for x in range(size)]


def PolyRow3(T: Table, size: int = 28) -> list[int]:
    return [T.poly(3, x) for x in range(size)]


def PolyCol(T: Table, col: int, size: int = 28) -> list[int]:
    return [T.poly(x, col) for x in range(size)]


def PolyCol1(T: Table, size: int = 28) -> list[int]:
    return [T.poly(x, 1) for x in range(size)]


def PolyCol2(T: Table, size: int = 28) -> list[int]:
    return [T.poly(x, 2) for x in range(size)]


def PolyCol3(T: Table, size: int = 28) -> list[int]:
    return [T.poly(x, 3) for x in range(size)]


def PolyDiag(T: Table, size: int = 28) -> list[int]:
    return [T.poly(n, n) for n in range(size)]


def RowLcmGcd(g: rgen, row: int, lg: bool) -> int:
    Z = [v for v in g(row) if v not in [-1, 0, 1]]
    if Z == []:
        return 1
    return lcm(*Z) if lg else gcd(*Z)


def TablLcm(T: Table, size: int = 28) -> list[int]:
    return [RowLcmGcd(T.gen, row, True) for row in range(size)]


def TablGcd(T: Table, size: int = 28) -> list[int]:
    return [RowLcmGcd(T.gen, row, False) for row in range(size)]


def TablMax(T: Table, size: int = 28) -> list[int]:
    return [reduce(max, (abs(t) for t in T.gen(row))) for row in range(size)]


def TablSum(T: Table, size: int = 28) -> list[int]:
    return [T.sum(n) for n in range(size)]


def EvenSum(T: Table, size: int = 28) -> list[int]:
    return [sum(T.gen(n)[::2]) for n in range(size)]


def OddSum(T: Table, size: int = 28) -> list[int]:
    return [sum(T.gen(n)[1::2]) for n in range(size)]


def AltSum(T: Table, size: int = 28) -> list[int]:
    return [sum(T.gen(n)[::2]) - sum(T.gen(n)[1::2]) for n in range(size)]


def AbsSum(T: Table, size: int = 28) -> list[int]:
    return [sum(abs(t) for t in T.gen(n)) for n in range(size)]


def AccSum(T: Table, size: int = 28) -> list[int]:
    return [sum(T.acc(n)) for n in range(size)]


def AccRevSum(T: Table, size: int = 28) -> list[int]:
    return [sum(accumulate(T.rev(n))) for n in range(size)]


def AntiDSum(T: Table, size: int = 28) -> list[int]:
    return [sum(T.antidiag(n)) for n in range(size)]


def ColMiddle(T: Table, size: int = 28) -> list[int]:
    return [T.gen(n)[n // 2] for n in range(size)]


def CentralE(T: Table, size: int = 28) -> list[int]:
    return [T.gen(2 * n)[n] for n in range(size)]


def CentralO(T: Table, size: int = 28) -> list[int]:
    return [T.gen(2 * n + 1)[n] for n in range(size)]


def ColLeft(T: Table, size: int = 28) -> list[int]:
    return [T.gen(n)[0] for n in range(size)]


def ColRight(T: Table, size: int = 28) -> list[int]:
    return [T.gen(n)[-1] for n in range(size)]


def PolyFrac(T: Table, n: int, x: Fraction) -> Fraction | int:
    return sum(c * (x**k) for (k, c) in enumerate(T.gen(n)))


def PosHalf(T: Table, size: int = 28) -> list[int]:
    return [((2**n) * PolyFrac(T, n, Fraction(1, 2))).numerator for n in range(size)]


def NegHalf(T: Table, size: int = 28) -> list[int]:
    return [
        (((-2) ** n) * PolyFrac(T, n, Fraction(-1, 2))).numerator for n in range(size)
    ]


def TransNat0(T: Table, size: int = 28) -> list[int]:
    return T.trans(lambda k: k, size)


def TransNat1(T: Table, size: int = 28) -> list[int]:
    return T.trans(lambda k: k + 1, size)


def TransSqrs(T: Table, size: int = 28) -> list[int]:
    return T.trans(lambda k: k * k, size)


def BinConv(T: Table, size: int = 28) -> list[int]:
    return [dotproduct(Binomial.gen(n), T.gen(n)) for n in range(size)]


def InvBinConv(T: Table, size: int = 28) -> list[int]:
    return [dotproduct(InvBinomial.gen(n), T.gen(n)) for n in range(size)]


"""The basic construction is a map
    (Table:Class, Trait:Function) -> (Anum:Url, TreatInfo:TeXString)
"""
TraitInfo: TypeAlias = Tuple[trait, str]
AllTraits: dict[str, TraitInfo] = {
    "Triangle  ": (Triangle, r"\((n,k) \mapsto T_{n, k}\)"),
    "Tinv      ": (Tinv, r"\((n,k) \mapsto T^{-1}_{n, k}\)"),
    "Trev      ": (Trev, r"\((n,k) \mapsto T_{n, n - k}\)"),
    "Trevinv   ": (Trevinv, r"\((n,k) \mapsto T^{-1}_{n, n - k}\)"),
    "Tinvrev   ": (Tinvrev, r"\((n,k) \mapsto (T_{n, n - k})^{-1}\)"),
    "Toff11    ": (Toff11, r"\((n,k) \mapsto T_{n + 1, k + 1} \)"),
    "Trev11    ": (Trev11, r"\((n,k) \mapsto T_{n + 1, n - k + 1} \)"),
    "Tinv11    ": (Tinv11, r"\((n,k) \mapsto T^{-1}_{n + 1, k + 1}\)"),
    "Trevinv11 ": (Trevinv11, r"\((n,k) \mapsto T^{-1}_{n + 1, n - k + 1}\)"),
    "Tinvrev11 ": (Tinvrev11, r"\((n,k) \mapsto (T_{n + 1, n - k + 1})^{-1}\)"),
    "Tantidiag ": (Tantidiag, r"\((n,k) \mapsto T_{n - k, k} \ \ (k \le n/2)\)"),
    "Tacc      ": (Tacc, r"\((n,k) \mapsto \sum_{j=0}^{k} T_{n, j}\)"),
    "Talt      ": (Talt, r"\((n,k) \mapsto T_{n, k}\ (-1)^{k}\)"),
    "Tder      ": (Tder, r"\((n,k) \mapsto T_{n + 1, k + 1}\ (k + 1) \)"),
    "TablCol0  ": (TablCol0, r"\(n \mapsto T_{n    , 0}\)"),
    "TablCol1  ": (TablCol1, r"\(n \mapsto T_{n + 1, 1}\)"),
    "TablCol2  ": (TablCol2, r"\(n \mapsto T_{n + 2, 2}\)"),
    "TablCol3  ": (TablCol3, r"\(n \mapsto T_{n + 3, 3}\)"),
    "TablDiag0 ": (TablDiag0, r"\(n \mapsto T_{n    , n}\)"),
    "TablDiag1 ": (TablDiag1, r"\(n \mapsto T_{n + 1, n}\)"),
    "TablDiag2 ": (TablDiag2, r"\(n \mapsto T_{n + 2, n}\)"),
    "TablDiag3 ": (TablDiag3, r"\(n \mapsto T_{n + 3, n}\)"),
    "PolyRow1  ": (PolyRow1, r"\(n \mapsto \sum_{k=0}^{1} T_{1, k}\  n^k\)"),
    "PolyRow2  ": (PolyRow2, r"\(n \mapsto \sum_{k=0}^{2} T_{2, k}\  n^k\)"),
    "PolyRow3  ": (PolyRow3, r"\(n \mapsto \sum_{k=0}^{3} T_{3, k}\  n^k\)"),
    "PolyCol1  ": (PolyCol1, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  1^k\)"),
    "PolyCol2  ": (PolyCol2, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  2^k\)"),
    "PolyCol3  ": (PolyCol3, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  3^k\)"),
    "PolyDiag  ": (PolyDiag, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  n^k\)"),
    "TablLcm   ": (
        TablLcm,
        r"\(n \mapsto \text{lcm}_{k=0}^{n}\ | T_{n, k} |\ \  (T_{n,k}>1)\)",
    ),
    "TablGcd   ": (
        TablGcd,
        r"\(n \mapsto \text{gcd}_{k=0}^{n}\ | T_{n, k} |\ \  (T_{n,k}>1)\)",
    ),
    "TablMax   ": (TablMax, r"\(n \mapsto \text{max}_{k=0}^{n}\ | T_{n, k} |\)"),
    "TablSum   ": (TablSum, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\)"),
    "EvenSum   ": (EvenSum, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  [2 | k]\)"),
    "OddSum    ": (OddSum, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  (1 - [2 | k])\)"),
    "AltSum    ": (AltSum, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  (-1)^{k}\)"),
    "AbsSum    ": (AbsSum, r"\(n \mapsto \sum_{k=0}^{n} | T_{n, k} |\)"),
    "AccSum    ": (AccSum, r"\(n \mapsto \sum_{k=0}^{n} \sum_{j=0}^{k} T_{n, j}\)"),
    "AccRevSum ": (
        AccRevSum,
        r"\(n \mapsto \sum_{k=0}^{n} \sum_{j=0}^{k} T_{n, n - j}\)",
    ),
    "AntiDSum  ": (AntiDSum, r"\(n \mapsto \sum_{k=0}^{n/2} T_{n - k, k}\)"),
    "ColMiddle ": (ColMiddle, r"\(n \mapsto T_{n, n / 2}\)"),
    "CentralE  ": (CentralE, r"\(n \mapsto T_{2 n, n}\)"),
    "CentralO  ": (CentralO, r"\(n \mapsto T_{2 n + 1, n}\)"),
    "PosHalf   ": (PosHalf, r"\(n \mapsto \sum_{k=0}^{n}   2^{n - k}\ T_{n, k}\)"),
    "NegHalf   ": (NegHalf, r"\(n \mapsto \sum_{k=0}^{n}(-2)^{n - k}\ T_{n, k}\)"),
    "TransNat0 ": (TransNat0, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  k\)"),
    "TransNat1 ": (TransNat1, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  (k + 1)\)"),
    "TransSqrs ": (TransSqrs, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  k^{2}\)"),
    "BinConv   ": (BinConv, r"\(n \mapsto \sum_{k=0}^{n} \binom{n}{k} T_{n, k}\)"),
    "InvBinConv": (
        InvBinConv,
        r"\(n \mapsto \sum_{k=0}^{n} (-1)^{k}\ \binom{n}{k} T_{n, n-k}\)",
    ),
}


def TableTraits(T: Table) -> None:
    for id, tr in AllTraits.items():
        name = (T.id + id).ljust(9 + len(T.id), " ")
        print(name, tr[0](T))  # type: ignore


GlobalDict: Dict[str, Dict[str, tuple[int, int, int]]] = {}


def ShowdGlobalDict() -> None:
    for tabl, dict in GlobalDict.items():
        print(f"*** Table {tabl} ***")
        for trait in dict:
            print(f"    {trait} -> {dict[trait]}")


def AnumberDict(T: Table, add: bool = False) -> Dict[str, tuple[int, int, int]]:
    """Collects the A-nunmbers of traits present in the OEIS.
    Add: Add to global OEISDict if requested. Defaults to False.
    """
    anum: Dict[str, tuple[int, int, int]] = {}
    for id, trai in AllTraits.items():
        name = (T.id + ":" + id).ljust(10 + len(T.id), " ")
        # use the defaults: 7 rows or 28 terms! Tantidiag 9 rows.
        seq = trai[0](T)  # type: ignore
        if seq != []:
            anum[name] = QueryOEIS(seq)  # type: ignore
    if add:
        GlobalDict[T.id] = anum
    return anum


header = [
    '<html><head><title>Traits></title><meta charset="utf-8"><meta name="viewport" content="width=device-width"><script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script></head><body width="38%"><iframe name="OEISframe" frameborder="0" scrolling="yes" width="62%" height="2200" align="left" title="Sequences"'
]


def AnumbersToFile(T: Table, add: bool = False) -> None:
    """Saves the A-numbers of traits present in the OEIS to a file."""
    SRC = f"https://oeis.org/{T.sim[0]}"
    SH = f"src={SRC}></iframe><p>"
    print(f"*** Table {T.id} under construction ***")
    hitpath = GetRoot(f"data/{T.id}Traits.html")
    mispath = GetRoot(f"data/{T.id}Missing.html")
    dict = AnumberDict(T, add)  # W
    with open(hitpath, "w+", encoding="utf-8") as oeis:
        with open(mispath, "w+", encoding="utf-8") as miss:
            for h in header:
                oeis.write(h)
                miss.write(h)
            oeis.write(SH)
            miss.write(SH)
            oeis.write(T.tex)
            miss.write(T.tex)
            for trait, anum in dict.items():
                print(f"     {trait} -> {anum}")
                tname = AllTraits[trait.split(":")[1]]
                tex = tname[1]
                seq = SeqToString(tname[0](T), 60, 24)  # type: ignore
                if anum[0] == 0:
                    miss.write(
                        f"<br><span style='white-space: pre'>{trait}</span> {tex}<br>"
                    )
                    miss.write(seq)  # type: ignore
                else:
                    num = str(anum[0]).rjust(6, "0")
                    url = f"<a href='https://oeis.org/A{num}' target='OEISframe'>A{num}</a>"
                    oeis.write(
                        f"<br>{url} <span style='white-space: pre'>{trait}</span> {tex}<br>"
                    )
                    oeis.write(seq)  # type: ignore
            L = "<a href='https://luschny.de/math/seq/tabls/"
            A = f"{L}{T.id}Traits.html'>[online]</a>"
            B = f"{L}{T.id}Missing.html'>[missing]</a>"
            C = f"{L}index.html'>[index]</a>"
            oeis.write(f"<p style='color:blue'>{B}{C}</p></body></html>")
            miss.write(f"<p style='color:blue'>{A}{C}</p></body></html>")


indheader = "<!DOCTYPE html><html lang='en'><head><meta name='viewport' content='width=device-width,initial-scale=1'><style type='text/css'>body{font-family:Calabri,Arial,sans-serif;font-size:18px;background-color: #804040; color: #C0C0C0}</style><base href='https://luschny.de/math/seq/tabls/' target='_blank'></head><body><table><thead><tr><th align='left'>Sequence</th><th align='left'>OEIS</th><th align='left'>Missing</th></tr></thead><tbody><tr>"


def warn() -> None:
    print("Are you sure? This takes 3-4 hours.")
    print("Don't forget to update Tables.py first.")
    input()


def RefreshDatabase() -> None:
    """Use with caution."""
    warn()
    global GlobalDict
    GlobalDict = {}
    indexpath = GetRoot(f"data/index.html")
    with open(indexpath, "w+", encoding="utf-8") as index:
        index.write(indheader)
        for tbl in Tables:
            AnumbersToFile(tbl, True)  # type: ignore
            index.write(
                f"<tr><td align='left'>{tbl.id}</td><td align='left'><a href='{tbl.id}Traits.html'>[online]</a></td><td align='left'><a href='{tbl.id}Missing.html'>[missing]</a></td></tr>"
            )
        index.write("</tbody></table></body></html>")
        index.flush()
    # Save to a JSON file
    jsonpath = GetRoot(f"data/AllTraits.json")
    with open(jsonpath, "w") as fileson:
        json.dump(GlobalDict, fileson)


def ReadTraitJson() -> None:
    with open("data.json", "r") as file:
        data = json.load(file)
    # Now, data is a Python dictionary
    print(data)


@cache
def abel(n: int) -> list[int]:
    if n == 0:
        return [1]
    b = binomial(n - 1)
    return [b[k - 1] * n ** (n - k) if k > 0 else 0 for k in range(n + 1)]


Abel = Table(
    abel,
    "Abel",
    ["A137452", "A061356", "A139526"],
    True,
    r"\(T_{n, k} = is(k = 0)\ ? \ 0^n : \binom{n-1}{k-1} (-n)^{n - k}\)",
)


@cache
def _andre(n: int, k: int) -> int:
    if k == 0 or n == 0:
        return 1
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


Bell = Table(
    bell,
    "Bell",
    ["A011971", "A011972", "A123346"],
    False,
    r"\(T_{n, k} = \sum_{j=0}^{k} \binom{k}{j} Bell_{n - k + j}\)",
)


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
    arow = binarypell(n - 1)
    row = arow + [1]
    for k in range(n - 1, 0, -1):
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


def invbinomial(n: int) -> list[int]:
    return [(-1) ** (n + k) * binomial(n)[k] for k in range(n + 1)]


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
InvBinomial = Table(invbinomial, "InvBinomial", ["A130595"], True)


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


BinomialCatalan = Table(
    binomialcatalan, "BinomialCatalan", ["A124644", "A098474"], True
)


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


CentralCycle = Table(
    centralcycle, "CentralCycle", ["A269940", "A111999", "A259456"], False
)


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
    if k < 0 or n < 0:
        return 0
    if k == 0:
        if n == 0:
            return 1
        else:
            return 0
    return _compodist(n - k, k) + k * _compodist(n - k, k - 1)


@cache
def compodist(n: int) -> list[int]:
    f = (sqrt(1 + 8 * n) - 1) // 2
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
    if k == 0 or n == 0:
        return 1
    return dist_latt(n, k - 1) + sum(
        dist_latt(2 * j, k - 1) * dist_latt(n - 1 - 2 * j, k)
        for j in range(1 + (n - 1) // 2)
    )


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


DyckPaths = Table(
    dyckpaths,
    "DyckPaths",
    ["A039599", "A050155"],
    True,
    r"\(T_{n, k}\ =\ \binom{2n}{n - k} (2k + 1) / (n + k + 1)\)",
)


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


Euler = Table(euler, "Euler", ["A363394", "A247453", "A109449"], True)


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
    eulerian2,
    "Eulerian2",
    ["A340556", "A201637", "A008517", "A112007", "A163936"],
    False,
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
    return [
        sum((-1) ** j * b[j] * dist_latt(n, k - j) for j in range(k + 1))
        for k in range(n + 1)
    ]


@cache
def ezz(n: int) -> list[int]:
    n += 2
    b = binomial(n + 1)
    return [
        sum((-1) ** j * b[j] * dist_latt(n, k - j) for j in range(k + 1))
        for k in range(n - 1)
    ]


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


EytzingerOrder = Table(eytzingerorder, "EytzingerOrder", ["A375825"])


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


FallingFactorial = Table(
    fallingfactorial,
    "FallingFact",
    ["A008279", "A068424", "A094587", "A173333", "A181511"],
    False,
)


@cache
def fibolucas(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1, 2]
    if n == 2:
        return [1, 2, 1]
    rowA = fibolucas(n - 2)
    row = fibolucas(n - 1) + [1 + n % 2]
    row[2] += 1
    for k in range(3, n):
        row[k] += rowA[k - 2]
    return row


FiboLucas = Table(fibolucas, "FiboLucas", ["A374439"], False)


@cache
def fibolucasinv(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [-2, 1]
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
    if n == 0:
        return [1]
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


FussCatalan = Table(
    fusscatalan, "FussCatalan", ["A355173", "A030237", "A054445"], False
)


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


HyperHarmonic = Table(
    hyperharmonic, "HyperHarmonic", ["A165675", "A093905", "A105954", "A165674"], True
)


@cache
def jacobsthal(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1, 1]
    if n == 2:
        return [1, 2, 1]
    Jn1 = jacobsthal(n - 1)
    Jn2 = jacobsthal(n - 2) + [0]
    row = [1] * (n + 1)
    for k in range(1, n):
        row[k] = Jn1[k - 1] + Jn1[k] + 2 * Jn2[k]
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
    lah,
    "Lah",
    ["A271703", "A008297", "A066667", "A089231", "A105278", "A111596"],
    True,
    r"\(T_{n, k} = is(k = 0)\ ? \ 0^n : \binom{n}{k} (n-1)!/(k-1)! \)",
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
    if n == 0:
        return [0]
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
    if n == 0:
        return [2]
    if n == 1:
        return [1, 2]
    row = lucas(n - 1) + [0]
    for k in range(n, 0, -1):
        row[k] += row[k - 1]
    return row


Lucas = Table(lucas, "Lucas", ["A029635", "A029653"])


@cache
def lucaspoly(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [1, 0]
    if n == 2:
        return [1, 1, 1]
    rowA = lucaspoly(n - 2)
    row = lucaspoly(n - 1) + [(n + 1) % 2]
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


Motzkin = Table(
    motzkin,
    "Motzkin",
    ["A064189", "A026300", "A009766"],
    True,
    r"\( T(n, k) \ =\  \binom{n}{k} hyper_{2,1}([(k - n)/2, (k - n + 1)/2], [k + 2], 4) \)",
)


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


Naturals = Table(naturals, "Naturals", ["A000027", "A001477"], True)


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
    return [k ^ (n - k) for k in range(n + 1)]


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


OrderedCycle = Table(
    orderedcycle, "OrderedCycle", ["A225479", "A048594", "A075181"], False
)


@cache
def A(n: int, k: int) -> int:
    if n == 0:
        return int(k == 0)
    if k > n:
        n, k = k, n
    b = binomial(k + 1)
    return k * A(n - 1, k) + sum(b[j + 1] * A(n - 1, k - j) for j in range(1, k + 1))


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
    if k < 1 or n < k:
        return 0
    if n == 1:
        return 1
    return _partdist(n - k, k) + _partdist(n - k, k - 1)


@cache
def partdist(n: int) -> list[int]:
    if n == 0:
        return [1]
    f = (sqrt(1 + 8 * n) - 1) // 2
    return [_partdist(n, k) if k <= f else 0 for k in range(n + 1)]


PartDist = Table(partdist, "PartitionDist", ["A008289"], False)


@cache
def _partdistsize(n: int, k: int, r: int) -> int:
    if n == 0:
        return 1 if k == 0 else 0
    if k == 0 or r == 0:
        return 0
    if k > n // 2 + 1:
        return 0
    return sum(
        _partdistsize(n - r * j, k - 1, r - 1) for j in range(1, n // r + 1)
    ) + _partdistsize(n, k, r - 1)


@cache
def partdistsize(n: int) -> list[int]:
    f = (sqrt(1 + 8 * n) - 1) // 2
    return [_partdistsize(n, k, n) if k <= f else 0 for k in range(n + 1)]


PartDistSize = Table(
    partdistsize, "PartitionDistSize", ["A365676", "A116608", "A060177"], False
)


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
    if n == 1:
        return int(k > 0)
    return sum(T(i, k) * h(n - i, k - 1) for i in range(1, n)) // (n - 1)


@cache
def polyatreeacc(n: int) -> list[int]:
    return [T(n + 1, k + 1) for k in range(n + 1)]


PolyaTreeAcc = Table(polyatreeacc, "PolyaTreeAcc", ["A375467"])


@cache
def polyatree(n: int) -> list[int]:
    p = polyatreeacc(n)
    return [int(n < 1)] + [p[k] - p[k - 1] for k in range(1, n + 1)]


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
    row = [(n - 1) * (rencontres(n - 1)[0] + rencontres(n - 2)[0])] + rencontres(n - 1)
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
    r"\(T(n, k)\ = \ (1/k!) \sum_{j=0}^{k} (-1)^{k-j} \binom{k}{j} j^{n} \)",
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


StirlingSet2 = Table(
    stirlingset2, "StirlingSet2", ["A358623", "A008299", "A137375"], False
)


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
            Binomial.val(n, k - j) * StirlingCycle.val(n - k + j, j)
            for j in range(k + 1)
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
    worpitzky,
    "Worpitzky",
    ["A028246", "A053440", "A075263", "A130850", "A163626"],
    False,
)


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
    InvBinomial,
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
