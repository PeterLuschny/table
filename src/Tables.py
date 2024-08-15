from functools import cache
from itertools import accumulate
from math import factorial
from fractions import Fraction
from sys import setrecursionlimit, set_int_max_str_digits
from typing import Callable, TypeAlias
setrecursionlimit(3000)
set_int_max_str_digits(5000)
def InvertMatrix(L: list[list[int]]) -> list[list[int]]:
    """
    Calculates the inverse of a lower triangular matrix.
    Args:
        L (list[list[int]]): The lower triangular matrix.
    Returns:
        list[list[int]]: The integer inverse of the lower triangular matrix if it exists.
        
        []: If the inverse does not exist.
    """
    n = len(L)
    inv = [[0 for i in range(n)] for _ in range(n)]  # Identity matrix
    for i in range(n):
        inv[i][i] = 1
    for k in range(n):
        for j in range(n):
            for i in range(k):
                inv[k][j] -= inv[i][j] * L[k][i]
            a = inv[k][j]
            b = L[k][k]
            if b == 0:
                # print("Warning: Inverse does not exist!")
                # raise ValueError("Inverse does not exist!")
                return []
            a, r = divmod(a, b)  # make sure that a is integer
            if r != 0:
                # print("Warning: Integer terms do not exist!")
                # raise ValueError("Integer terms do not exist!")
                return []
    return [row[0:n + 1] for n, row in enumerate(inv)]
def InvertTriangle(r, dim: int) -> list[list[int]]:
    M = [[r(n)[k] if k <= n else 0 for k in range(dim)] for n in range(dim)]
    return InvertMatrix(M)
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
@cache
def abel(n: int) -> list[int]:
    if n == 0:
        return [1]
    b = binomial(n - 1)
    return [b[k - 1] * n ** (n - k) if k > 0 else 0 for k in range(n + 1)]
Abel = Table(abel, "Abel", ["A137452", "A061356", "A139526"], True)
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
def binomialpell(n):
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
def composition(n: int) -> list[int]:
    if n == 0:
        return [1]
    cm = compomax(n)
    return [cm[k] - cm[k - 1] if k > 0 else 0 for k in range(n + 1)]
Composition = Table(composition, "Composition", ["A048004"], True)
@cache
def compomax(n: int) -> list[int]:
    @cache
    def t(n: int, k: int) -> int:
        if n == 0 or k == 1:
            return 1
        return sum(t(n - j, k) for j in range(1, min(n, k) + 1))
    return [t(n, k) for k in range(n + 1)]
CompoMax = Table(compomax, "CompositionMax", ["A126198"], False)
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
    return FiboLucas.invrev(n+1)[-1]
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
    if n == 0: return [1]
    if n == 1: return [1, 0]
    if n == 2: return [1, 1, 1]
    rowA = lucas(n - 2)
    row  = lucas(n - 1) + [(n + 1) % 2]
    row[1] += 1
    for k in range(3, n):
        row[k] += rowA[k - 2]
    return row
Lucas = Table(lucas, "Lucas", ["A374440"], False)
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
def partnumexact(n: int) -> list[int]:
    return [part(n, k) for k in range(n + 1)]
PartnumExact = Table(partnumexact, "Partition", ["A072233", "A008284", "A058398"], True)
@cache
def _pdist(n: int, k: int, r: int) -> int:
    if n == 0:
        return 1 if k == 0 else 0
    if k == 0 or r == 0:
        return 0
    return (sum(_pdist(n - r * j, k - 1, r - 1) for j in range(1, n // r + 1))
           + _pdist(n, k, r - 1))
@cache
def partnumdist(n) -> list[int]:
    return [_pdist(n, k, n) for k in range(n + 1)]
PartnumDist = Table(partnumdist, "PartitionDist", ["A365676", "A116608", "A060177"], False)
@cache
def partnummax(n: int) -> list[int]:
    return list(accumulate(partnumexact(n)))
PartnumMax = Table(partnummax, "PartitionMax", ["A026820", "A058400"], False)
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
    ["A028246", "A053440", "A075263", "A130850", "A163626"], False   
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
    return sum(partnumexact(n))
def riordan_num(n: int) -> int:
    return sum((-1) ** (n - k) * BinomialCatalan.val(n, k) for k in range(n + 1))
Tables: list[Table] = [
    Abel,
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
    CompoMax,
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
    Kekule,
    LabeledGraphs,
    Laguerre,
    Lah,
    Lehmer,
    Leibniz,
    Levin,
    Lozanic,
    Lucas,
    Moebius,
    Monotone,
    Motzkin,
    MotzkinPoly,
    Narayana,
    Naturals,
    Nicomachus,
    One,
    Ordinals,
    OrderedCycle,
    Parades,
    PartnumExact,
    PartnumDist,
    PartnumMax,
    Pascal,
    Polygonal,
    PowLaguerre,
    Rencontres,
    RisingFactorial,
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
    Worpitzky,
]
# for T in Tables: View(T)
