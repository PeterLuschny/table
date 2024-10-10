from Tables import Tables
from Binomial import Binomial, InvBinomial
from _tabltypes import Table, rgen, trait
from _tabloeis import QueryOEIS
from _tablutils import SeqToString
from _tablpaths import GetRoot
from typing import Dict, Tuple, TypeAlias
from itertools import accumulate
from more_itertools import flatten
from functools import reduce
from math import lcm, gcd
from fractions import Fraction
import operator


# #@

# use the defaults for size: 7 rows for tables or 28 terms


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


# Needs 9 rows
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


# Note our convention to exclude 0 and 1.
def RowLcmGcd(g: rgen, row: int, lg: bool) -> int:
    Z = [v for v in g(row) if v not in [-1, 0, 1]]
    if Z == []:
        return 1
    return lcm(*Z) if lg else gcd(*Z)


def TablLcm(T: Table, size: int = 28) -> list[int]:
    return [RowLcmGcd(T.gen, row, True) for row in range(size)]


def TablGcd(T: Table, size: int = 28) -> list[int]:
    return [RowLcmGcd(T.gen, row, False) for row in range(size)]


# Note our convention to use the abs value.
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
    "Triangle  ": (Triangle,  r"\((n,k) \mapsto T_{n, k}\)"),
    "Tinv      ": (Tinv,      r"\((n,k) \mapsto T^{-1}_{n, k}\)"),
    "Trev      ": (Trev,      r"\((n,k) \mapsto T_{n, n - k}\)"),
    "Trevinv   ": (Trevinv,   r"\((n,k) \mapsto T^{-1}_{n, n - k}\)"),
    "Tinvrev   ": (Tinvrev,   r"\((n,k) \mapsto (T_{n, n - k})^{-1}\)"),
    "Toff11    ": (Toff11,    r"\((n,k) \mapsto T_{n + 1, k + 1} \)"),
    "Trev11    ": (Trev11,    r"\((n,k) \mapsto T_{n + 1, n - k + 1} \)"),
    "Tinv11    ": (Tinv11,    r"\((n,k) \mapsto T^{-1}_{n + 1, k + 1}\)"),
    "Trevinv11 ": (Trevinv11, r"\((n,k) \mapsto T^{-1}_{n + 1, n - k + 1}\)"),
    "Tinvrev11 ": (Tinvrev11, r"\((n,k) \mapsto (T_{n + 1, n - k + 1})^{-1}\)"),
    "Tantidiag ": (Tantidiag, r"\((n,k) \mapsto T_{n - k, k} \ \ (k \le n/2)\)"),
    "Tacc      ": (Tacc,      r"\((n,k) \mapsto \sum_{j=0}^{k} T_{n, j}\)"),
    "Talt      ": (Talt,      r"\((n,k) \mapsto T_{n, k}\ (-1)^{k}\)"),
    "Tder      ": (Tder,      r"\((n,k) \mapsto T_{n + 1, k + 1}\ (k + 1) \)"),
    "TablCol0  ": (TablCol0,  r"\(n \mapsto T_{n    , 0}\)"),
    "TablCol1  ": (TablCol1,  r"\(n \mapsto T_{n + 1, 1}\)"),
    "TablCol2  ": (TablCol2,  r"\(n \mapsto T_{n + 2, 2}\)"),
    "TablCol3  ": (TablCol3,  r"\(n \mapsto T_{n + 3, 3}\)"),
    "TablDiag0 ": (TablDiag0, r"\(n \mapsto T_{n    , n}\)"),
    "TablDiag1 ": (TablDiag1, r"\(n \mapsto T_{n + 1, n}\)"),
    "TablDiag2 ": (TablDiag2, r"\(n \mapsto T_{n + 2, n}\)"),
    "TablDiag3 ": (TablDiag3, r"\(n \mapsto T_{n + 3, n}\)"),
    "PolyRow1  ": (PolyRow1,  r"\(n \mapsto \sum_{k=0}^{1} T_{1, k}\  n^k\)"),
    "PolyRow2  ": (PolyRow2,  r"\(n \mapsto \sum_{k=0}^{2} T_{2, k}\  n^k\)"),
    "PolyRow3  ": (PolyRow3,  r"\(n \mapsto \sum_{k=0}^{3} T_{3, k}\  n^k\)"),
    "PolyCol1  ": (PolyCol1,  r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  1^k\)"),
    "PolyCol2  ": (PolyCol2,  r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  2^k\)"),
    "PolyCol3  ": (PolyCol3,  r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  3^k\)"),
    "PolyDiag  ": (PolyDiag,  r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  n^k\)"),
    "TablLcm   ": (TablLcm,   r"\(n \mapsto lcm_{k=0}^{n}\ | T_{n, k} |\ \  (T_{n,k}>1)\)"),
    "TablGcd   ": (TablGcd,   r"\(n \mapsto gcd_{k=0}^{n}\ | T_{n, k} |\ \  (T_{n,k}>1)\)"),
    "TablMax   ": (TablMax,   r"\(n \mapsto max_{k=0}^{n}\ | T_{n, k} |\)"),
    "TablSum   ": (TablSum,   r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\)"),
    "EvenSum   ": (EvenSum,   r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  [2 | k]\)"),
    "OddSum    ": (OddSum,    r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  (1 - [2 | k])\)"),
    "AltSum    ": (AltSum,    r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  (-1)^{k}\)"),
    "AbsSum    ": (AbsSum,    r"\(n \mapsto \sum_{k=0}^{n} | T_{n, k} |\)"),
    "AccSum    ": (AccSum,    r"\(n \mapsto \sum_{k=0}^{n} \sum_{j=0}^{k} T_{n, j}\)"),
    "AccRevSum ": (AccRevSum, r"\(n \mapsto \sum_{k=0}^{n} \sum_{j=0}^{k} T_{n, n - j}\)"),
    "AntiDSum  ": (AntiDSum,  r"\(n \mapsto \sum_{k=0}^{n/2} T_{n - k, k}\)"),
    "ColMiddle ": (ColMiddle, r"\(n \mapsto T_{n, n / 2}\)"),
    "CentralE  ": (CentralE,  r"\(n \mapsto T_{2 n, n}\)"),
    "CentralO  ": (CentralO,  r"\(n \mapsto T_{2 n + 1, n}\)"),
    "PosHalf   ": (PosHalf,   r"\(n \mapsto \sum_{k=0}^{n}   2^{n - k}\ T_{n, k}\)"),
    "NegHalf   ": (NegHalf,   r"\(n \mapsto \sum_{k=0}^{n}(-2)^{n - k}\ T_{n, k}\)"),
    "TransNat0 ": (TransNat0, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  k\)"),
    "TransNat1 ": (TransNat1, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  (k + 1)\)"),
    "TransSqrs ": (TransSqrs, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  k^{2}\)"),
    "BinConv   ": (BinConv,   r"\(n \mapsto \sum_{k=0}^{n} \binom{n}{k} T_{n, k}\)"),
    "InvBinConv": (InvBinConv, r"\(n \mapsto \sum_{k=0}^{n} (-1)^{k}\ \binom{n}{k} T_{n, n-k}\)"),
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
        # use the defaults: 7 rows or 28 terms!
        seq = trai[0](T)  # type: ignore
        if seq != []:
            anum[name] = QueryOEIS(seq)  # type: ignore

    if add:
        GlobalDict[T.id] = anum
    return anum


header = [
    '<!DOCTYPE html><html><head><title>Traits></title><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" ',
    'integrity="sha384-nB0miv6/jRmo5UMMR1wu3Gz6NLsoTkbqJghGIsx//Rlm+ZU03BU6SQNC66uf4l5+" crossorigin="anonymous">',
    '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"',
    ' integrity="sha384-7zkQWkzuo3B5mTepMUcHkMB5jZaolc2xDwL6VFqjFALcbeS9Ggm/Yr2r3Dy4lfFg" crossorigin="anonymous"></script>',
    '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" ',
    'integrity="sha384-43gviWU0YVjaDtb/GhzOouOXtZMP/7XUzwPTstBeZFe/+rCMvRwr4yROQP43s0Xk" crossorigin="anonymous"',
    ' onload="renderMathInElement(document.body);"></script>',
    "<style> .katex {font-size:1.0em; color:#004080;}.katex-display {margin-top:0.0em;margin-bottom:0.0em;padding-top:0.5em;padding-bottom:0.4em;}",
    ".katex-display {overflow-x: visible;overflow-y: hidden;}.katex > .katex-html {white-space: normal;}.katex .base {margin-top:2px; margin-bottom:2px;}</style>",
    "<style>body {background-color: #C0C0C0; margin-left: 0.5em;} p{font-family: monospace;color: #004080;}a {color: #804040;}</style></head>",
    "<body width='38%'><iframe name = 'OEISframe' frameborder='0' scrolling='yes' width='62%' height='2200' align='left' title='Sequences' src='https://oeis.org/A137452'> </iframe><p>",
]

"""
W = {'Abel:Triangle  ': (137452, 0, 25), 'Abel:Tinv      ': (59297, 0, 25), 'Abel:Trev      ': (0, 0, 0), 'Abel:Trevinv   ': (59299, 0, 25), 'Abel:Toff11    ': (61356, 0, 25), 'Abel:Trev11    ': (139526, 0, 25), 'Abel:Tinv11    ': (59298, 0, 25), 'Abel:Trevinv11 ': (59300, 0, 25), 'Abel:Tacc      ': (0, 0, 0), 'Abel:Talt      ': (137452, 0, 25), 'Abel:Tder      ': (225465, 0, 25), 'Abel:TablCol0  ': (7, 0, 25), 'Abel:TablCol1  ': (169, 0, 19), 'Abel:TablCol2  ': (53506, 1, 18), 'Abel:TablCol3  ': (53507, 2, 16), 'Abel:TablDiag0 ': (12, 0, 25), 'Abel:TablDiag1 ': (2378, 0, 25), 'Abel:TablDiag2 ': (0, 0, 0), 'Abel:TablDiag3 ': (0, 0, 0), 'Abel:PolyRow1  ': (27, 0, 24), 'Abel:PolyRow2  ': (5563, 0, 25), 'Abel:PolyRow3  ': (0, 0, 0), 'Abel:PolyCol1  ': (272, 1, 18), 'Abel:PolyCol2  ': (7334, 0, 18), 'Abel:PolyCol3  ': (362354, 0, 19), 'Abel:PolyDiag  ': (193678, 0, 16), 'Abel:TablLcm   ': (0, 0, 0), 'Abel:TablGcd   ': (27, 0, 24), 'Abel:TablMax   ': (169, 0, 19), 'Abel:TablSum   ': (272, 1, 18), 'Abel:EvenSum   ': (274278, 0, 23), 'Abel:OddSum    ': (195136, 0, 24), 'Abel:AltSum    ': (312, 0, 19), 'Abel:AbsSum    ': (272, 1, 18), 'Abel:AccSum    ': (0, 0, 0), 'Abel:AccRevSum ': (367255, 0, 19), 'Abel:AntiDSum  ': (0, 0, 0), 'Abel:ColMiddle ': (0, 0, 0), 'Abel:CentralE  ': (367254, 0, 15), 'Abel:CentralO  ': (0, 0, 0), 'Abel:PosHalf   ': (52750, 0, 16), 'Abel:NegHalf   ': (85527, 0, 17), 'Abel:TransNat0 ': (89946, 0, 18), 'Abel:TransNat1 ': (367255, 0, 19), 'Abel:TransSqrs ': (225497, 0, 19), 'Abel:BinConv   ': (367256, 0, 18), 'Abel:InvBinConv': (367257, 0, 19)}
"""


def AnumbersToFile(T: Table) -> None:
    """Saves the A-numbers of traits present in the OEIS to a file."""
    print(f"*** Table {T.id} under construction ***")
    hitpath = GetRoot(f"data/{T.id}Traits.html")
    mispath = GetRoot(f"data/{T.id}Missing.html")
    dict = AnumberDict(T)  # W

    with open(hitpath, "w+", encoding="utf-8") as oeis:
        with open(mispath, "w+", encoding="utf-8") as miss:
            for h in header:
                oeis.write(h)
                miss.write(h)
            oeis.write(T.tex)
            miss.write(T.tex)
            for trait, anum in dict.items():
                print(f"     {trait} -> {anum}")
                tname = AllTraits[trait.split(":")[1]]
                tex = tname[1]
                seq = SeqToString(tname[0](T), 60, 24)  # type: ignore
                if anum[0] == 0:
                    miss.write(f"<br><span style='white-space: pre'>{trait}</span> {tex}<br>")
                    miss.write(seq)  # type: ignore
                else:
                    num = str(anum[0]).rjust(6, "0")
                    url = f"<a href='https://oeis.org/A{num}' target='OEISframe'>A{num}</a>"
                    oeis.write(f"<br>{url} <span style='white-space: pre'>{trait}</span> {tex}<br>")
                    oeis.write(seq)  # type: ignore
            oeis.write(f"<p style='font-size:large'><a href='https://luschny.de/math/seq/tabls/{T.id}Missing.html'>[MISSING TRAITS]</a><a href='https://luschny.de/math/seq/tabls/TablIndex.html'>[INDEX]</a></p></body></html>")
            miss.write(f"<p style='font-size:large'><a href='https://luschny.de/math/seq/tabls/{T.id}Traits.html'>[PUBLISHED TRAITS]</a><a href='https://luschny.de/math/seq/tabls/TablIndex.html'>[INDEX]</a></p></body></html>")


def RefreshDatabase() -> None:
    """Use with caution."""
    print("Are you sure? This takes 3-4 hours.")
    print("Don't forget to update Tables.py first.")
    input()
    for tbl in Tables:
        AnumbersToFile(tbl)  # type: ignore


if __name__ == "__main__":

    from Abel import Abel  # type: ignore
    from Bell import Bell  # type: ignore
    from Lah import Lah  # type: ignore
    from DyckPaths import DyckPaths  # type: ignore
    from Binomial import Binomial  # type: ignore
    from StirlingSet import StirlingSet  # type: ignore
    from Motzkin import Motzkin  # type: ignore
    from Worpitzky import Worpitzky  # type: ignore

    def test(T: Table, LEN: int) -> None:
        print("TablCol")
        for n in range(4):
            print(TablCol(T, n, LEN))
        print("TablDiag")
        for n in range(4):
            print(TablDiag(T, n, LEN))
        print("PolyRow")
        for n in range(4):
            print(PolyRow(T, n, LEN))
        print("PolyCol")
        for n in range(4):
            print(PolyCol(T, n, LEN))
        print()

    # test(Abel, 10)
    # AnumbersToFile(Abel)

    # RefreshDatabase()