from Tables import TablesList
from Binomial import Binomial, InvBinomial
from _tabltypes import Table, RevTable, rgen, trait
from _tabloeis import QueryOEIS
from _tablutils import SeqToString
from _tablpaths import GetRoot
from typing import Dict, Tuple, TypeAlias
from itertools import accumulate
from more_itertools import flatten
from functools import reduce
from math import lcm, gcd
from fractions import Fraction
import json
import operator


W = {'Abel:Triangle  ': (137452, 0, 25), 'Abel:Tinv      ': (59297, 0, 25), 'Abel:Trev      ': (0, 0, 0), 'Abel:Trevinv   ': (59299, 0, 25), 'Abel:Toff11    ': (61356, 0, 25), 'Abel:Trev11    ': (139526, 0, 25), 'Abel:Tinv11    ': (59298, 0, 25), 'Abel:Trevinv11 ': (59300, 0, 25), 'Abel:Tacc      ': (0, 0, 0), 'Abel:Talt      ': (137452, 0, 25), 'Abel:Tder      ': (225465, 0, 25), 'Abel:TablCol0  ': (7, 0, 25), 'Abel:TablCol1  ': (169, 0, 19), 'Abel:TablCol2  ': (53506, 1, 18), 'Abel:TablCol3  ': (53507, 2, 16), 'Abel:TablDiag0 ': (12, 0, 25), 'Abel:TablDiag1 ': (2378, 0, 25), 'Abel:TablDiag2 ': (0, 0, 0), 'Abel:TablDiag3 ': (0, 0, 0), 'Abel:PolyRow1  ': (27, 0, 24), 'Abel:PolyRow2  ': (5563, 0, 25), 'Abel:PolyRow3  ': (0, 0, 0), 'Abel:PolyCol1  ': (272, 1, 18), 'Abel:PolyCol2  ': (7334, 0, 18), 'Abel:PolyCol3  ': (362354, 0, 19), 'Abel:PolyDiag  ': (193678, 0, 16), 'Abel:TablLcm   ': (0, 0, 0), 'Abel:TablGcd   ': (27, 0, 24), 'Abel:TablMax   ': (169, 0, 19), 'Abel:TablSum   ': (272, 1, 18), 'Abel:EvenSum   ': (274278, 0, 23), 'Abel:OddSum    ': (195136, 0, 24), 'Abel:AltSum    ': (312, 0, 19), 'Abel:AbsSum    ': (272, 1, 18), 'Abel:AccSum    ': (0, 0, 0), 'Abel:AccRevSum ': (367255, 0, 19), 'Abel:AntiDSum  ': (0, 0, 0), 'Abel:ColMiddle ': (0, 0, 0), 'Abel:CentralE  ': (367254, 0, 15), 'Abel:CentralO  ': (0, 0, 0), 'Abel:PosHalf   ': (52750, 0, 16), 'Abel:NegHalf   ': (85527, 0, 17), 'Abel:TransNat0 ': (89946, 0, 18), 'Abel:TransNat1 ': (367255, 0, 19), 'Abel:TransSqrs ': (225497, 0, 19), 'Abel:BinConv   ': (367256, 0, 18), 'Abel:InvBinConv': (367257, 0, 19)}

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
    return [((2**n) * PolyFrac(T, n, Fraction(1, 2))).numerator 
            for n in range(size)]


def NegHalf(T: Table, size: int = 28) -> list[int]:
    return [(((-2) ** n) * PolyFrac(T, n, Fraction(-1, 2))).numerator 
            for n in range(size)]


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

TraitInfo: TypeAlias = Tuple[trait, int, str]

AllTraits: dict[str, TraitInfo] = {
    "Triangle  ": (Triangle,  7, r"\((n,k) \mapsto T_{n, k}\)"),
    "Tinv      ": (Tinv,      7, r"\((n,k) \mapsto T^{-1}_{n, k}\)"),
    "Trev      ": (Trev,      7, r"\((n,k) \mapsto T_{n, n - k}\)"),
    "Trevinv   ": (Trevinv,   7, r"\((n,k) \mapsto T^{-1}_{n, n - k}\)"),
    "Tinvrev   ": (Tinvrev,   7, r"\((n,k) \mapsto (T_{n, n - k})^{-1}\)"),
    "Toff11    ": (Toff11,    7, r"\((n,k) \mapsto T_{n + 1, k + 1} \)"),
    "Trev11    ": (Trev11,    7, r"\((n,k) \mapsto T_{n + 1, n - k + 1} \)"),
    "Tinv11    ": (Tinv11,    7, r"\((n,k) \mapsto T^{-1}_{n + 1, k + 1}\)"),
    "Trevinv11 ": (Trevinv11, 7, r"\((n,k) \mapsto T^{-1}_{n + 1, n - k + 1}\)"),
    "Tinvrev11 ": (Tinvrev11, 7, r"\((n,k) \mapsto (T_{n + 1, n - k + 1})^{-1}\)"),
    "Tantidiag ": (Tantidiag, 9, r"\((n,k) \mapsto T_{n - k, k} \ \ (k \le n/2)\)"),
    "Tacc      ": (Tacc,      7, r"\((n,k) \mapsto \sum_{j=0}^{k} T_{n, j}\)"),
    "Talt      ": (Talt,      7, r"\((n,k) \mapsto T_{n, k}\ (-1)^{k}\)"),
    "Tder      ": (Tder,      7, r"\((n,k) \mapsto T_{n + 1, k + 1}\ (k + 1) \)"),
    "TablCol0  ": (TablCol0,  28, r"\(n \mapsto T_{n    , 0}\)"),
    "TablCol1  ": (TablCol1,  28, r"\(n \mapsto T_{n + 1, 1}\)"),
    "TablCol2  ": (TablCol2,  28, r"\(n \mapsto T_{n + 2, 2}\)"),
    "TablCol3  ": (TablCol3,  28, r"\(n \mapsto T_{n + 3, 3}\)"),
    "TablDiag0 ": (TablDiag0, 28, r"\(n \mapsto T_{n    , n}\)"),
    "TablDiag1 ": (TablDiag1, 28, r"\(n \mapsto T_{n + 1, n}\)"),
    "TablDiag2 ": (TablDiag2, 28, r"\(n \mapsto T_{n + 2, n}\)"),
    "TablDiag3 ": (TablDiag3, 28, r"\(n \mapsto T_{n + 3, n}\)"),
    "PolyRow1  ": (PolyRow1,  28, r"\(n \mapsto \sum_{k=0}^{1} T_{1, k}\  n^k\)"),
    "PolyRow2  ": (PolyRow2,  28, r"\(n \mapsto \sum_{k=0}^{2} T_{2, k}\  n^k\)"),
    "PolyRow3  ": (PolyRow3,  28, r"\(n \mapsto \sum_{k=0}^{3} T_{3, k}\  n^k\)"),
    "PolyCol1  ": (PolyCol1,  28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  1^k\)"),
    "PolyCol2  ": (PolyCol2,  28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  2^k\)"),
    "PolyCol3  ": (PolyCol3,  28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  3^k\)"),
    "PolyDiag  ": (PolyDiag,  28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  n^k\)"),
    "TablLcm   ": (TablLcm,   28, r"\(n \mapsto \text{lcm}_{k=0}^{n}\ | T_{n, k} |\ \  (T_{n,k}>1)\)"),
    "TablGcd   ": (TablGcd,   28, r"\(n \mapsto \text{gcd}_{k=0}^{n}\ | T_{n, k} |\ \  (T_{n,k}>1)\)"),
    "TablMax   ": (TablMax,   28, r"\(n \mapsto \text{max}_{k=0}^{n}\ | T_{n, k} |\)"),
    "TablSum   ": (TablSum,   28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\)"),
    "EvenSum   ": (EvenSum,   28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  [2 | k]\)"),
    "OddSum    ": (OddSum,    28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  (1 - [2 | k])\)"),
    "AltSum    ": (AltSum,    28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  (-1)^{k}\)"),
    "AbsSum    ": (AbsSum,    28, r"\(n \mapsto \sum_{k=0}^{n} | T_{n, k} |\)"),
    "AccSum    ": (AccSum,    28, r"\(n \mapsto \sum_{k=0}^{n} \sum_{j=0}^{k} T_{n, j}\)"),
    "AccRevSum ": (AccRevSum, 28, r"\(n \mapsto \sum_{k=0}^{n} \sum_{j=0}^{k} T_{n, n - j}\)"),
    "AntiDSum  ": (AntiDSum,  28, r"\(n \mapsto \sum_{k=0}^{n/2} T_{n - k, k}\)"),
    "ColMiddle ": (ColMiddle, 28, r"\(n \mapsto T_{n, n / 2}\)"),
    "CentralE  ": (CentralE,  28, r"\(n \mapsto T_{2 n, n}\)"),
    "CentralO  ": (CentralO,  28, r"\(n \mapsto T_{2 n + 1, n}\)"),
    "PosHalf   ": (PosHalf,   28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k} \ 2^{n - k} \)"),
    "NegHalf   ": (NegHalf,   28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k} \ (-2)^{n - k} \)"),
    "TransNat0 ": (TransNat0, 28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  k\)"),
    "TransNat1 ": (TransNat1, 28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  (k + 1)\)"),
    "TransSqrs ": (TransSqrs, 28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k}\  k^{2}\)"),
    "BinConv   ": (BinConv,   28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, k} \ \binom{n}{k} \)"),
    "InvBinConv": (InvBinConv, 28, r"\(n \mapsto \sum_{k=0}^{n} T_{n, n-k} \ (-1)^{k} \ \binom{n}{k} \)"),
}


def TableTraits(T: Table) -> None:
    for id, tr in AllTraits.items():
        name = (T.id + id).ljust(9 + len(T.id), " ")
        print(name, tr[0](T, tr[1]))


GlobalDict: Dict[str, Dict[str, int]] = {}


def ShowdGlobalDict() -> None:
    global GlobalDict
    for tabl, dict in GlobalDict.items():
        print(f"*** Table {tabl} ***")
        for trait in dict:
            print(f"    {trait} -> {dict[trait]}")


def FilterDict(olddict: Dict[str, int] )  -> Dict[str, int]:
    anumlist: set[int] = set()
    newdict: Dict[str, int] = {}
    for k, v in olddict.items():
        if not v in anumlist: 
            newdict[k] = v
        anumlist.add(v)
    return newdict


def AnumberDict(
    T: Table, 
    info: bool = False,
    addtoglobal: bool = False,
    addreversed: bool = False,
    filter: bool = False
) -> Dict[str, int]:
    """Collects the A-nunmbers of the traits of T present in the OEIS."""
    print(f"*** Table {T.id} under construction ***")
    global GlobalDict

    TableList = [T, RevTable(T)] if addreversed else [T]
    tdict: Dict[str, int] = {}
    for t in TableList:

        for trid, tr in AllTraits.items():
            name = (t.id + "#" + trid).ljust(10 + len(t.id), " ")
            seq: list[int] = tr[0](t, tr[1]) 
            if seq != []:
                tdict[name] = QueryOEIS(seq, info)
                
        if filter:
            tdict = FilterDict(tdict)

        if addtoglobal:
            GlobalDict[t.id] = tdict

    return tdict


header = '<html><head><title>Traits</title><meta charset="utf-8"><meta name="viewport" content="width=device-width"><script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"> window.MathJax = {loader: {load: ["[tex]/bbox"]}, tex: {packages: {"[+]": ["bbox"]}}}</script></head><body width="38%"><iframe name="OEISframe" frameborder="0" scrolling="yes" width="62%" height="2200" align="left" title="Sequences"'

def AnumbersToFile(
    T: Table, 
    dict: Dict[str, int],
    info: bool = False
)  -> None:
    """Saves the A-numbers of traits present in the OEIS to a file."""
    
    SRC = f'https://oeis.org/{T.sim[0]}'
    SH = f'src={SRC}></iframe><p><span style="white-space: pre">     {T.id}</span><br>'
    hitpath = GetRoot(f"data/{T.id}Traits.html")
    mispath = GetRoot(f"data/{T.id}Missing.html")
    head = header.replace("Traits", T.id)
    TeX = r"\(\bbox[yellow, 5px]{\color{DarkGreen} T_{n, k} \ = \ TTEX } \)" 
    TEX = TeX.replace("TTEX", T.tex)

    with open(hitpath, "w+", encoding="utf-8") as oeis:
        with open(mispath, "w+", encoding="utf-8") as miss:
            oeis.write(head); oeis.write(SH); oeis.write(TEX)
            miss.write(head); miss.write(SH); miss.write(TEX)

            for tr, anum in dict.items():
                if info: print(f"     {tr} -> {anum}")
                tr, trn, tex = AllTraits[tr.split("#")[1]]
                seq = SeqToString(tr(T, trn), 60, 24) 
                if anum == 0:
                    miss.write(f"<br><span style='white-space: pre'>{tr}</span> {tex}<br>")
                    miss.write(seq) 
                else:
                    num = str(anum).rjust(6, "0")
                    url = f"<a href='https://oeis.org/A{num}' target='OEISframe'>A{num}</a>"
                    oeis.write(f"<br>{url} <span style='white-space: pre'>{tr}</span> {tex}<br>")
                    oeis.write(seq) 

            L = "<a href='https://luschny.de/math/seq/tabls/"
            A = f"{L}{T.id}Traits.html'>[online]</a>"
            B = f"{L}{T.id}Missing.html'>[missing]</a>"
            C = f"{L}index.html'>[index]</a>"

            oeis.write(f"<p style='color:blue'>{B}{C}</p></body></html>")
            miss.write(f"<p style='color:blue'>{A}{C}</p></body></html>")


indheader = "<!DOCTYPE html><html lang='en'><head><title>Index</title><meta name='viewport' content='width=device-width,initial-scale=1'><style type='text/css'>body{font-family:Calabri,Arial,sans-serif;font-size:18px;background-color: #804040; color: #C0C0C0}</style><base href='https://luschny.de/math/seq/tabls/' target='_blank'></head><body><table><thead><tr><th align='left'>Sequence</th><th align='left'>OEIS</th><th align='left'>Missing</th></tr></thead><tbody><tr>"

def warn() -> None:
    print("Are you sure? This takes 3-4 hours.")
    print("Don't forget to update Tables.py first.")
    print("Hit return >")
    input()

def RefreshDatabase() -> None:
    """Use with caution."""
    warn()

    global GlobalDict

    indexpath = GetRoot(f"data/index.html")
    with open(indexpath, "w+", encoding="utf-8") as index:
        index.write(indheader)

        for T in TablesList:
            dict = AnumberDict(T, True, True, True, True)  # type: ignore 
            AnumbersToFile(T, dict, True)       # type: ignore
            index.write(f"<tr><td align='left'>{T.id}</td><td align='left'><a href='{T.id}Traits.html'>[online]</a></td><td align='left'><a href='{T.id}Missing.html'>[missing]</a></td></tr>")

        index.write("</tbody></table></body></html>")
        index.flush()

    # Save to a JSON file
    jsonpath = GetRoot(f"data/AllTraits.json")
    with open(jsonpath, 'w') as fileson:
        json.dump(GlobalDict, fileson)


def ReadJsonDict() -> None:
    global GlobalDict
    jsonpath = GetRoot(f"data/AllTraits.json")
    with open(jsonpath, 'r') as file:
        GlobalDict = json.load(file)
    print("GlobalDict with all traits installed!")

def AddTable(
    T: Table, 
    addrev: bool=False, 
    filter: bool=False
) -> Dict[str, int]:
    ReadJsonDict()
    dict = AnumberDict(T, True, True, addrev, filter)
    print("Dict length:", len(dict))
    AnumbersToFile(T, dict , True)
    jsonpath = GetRoot(f"data/AllTraits.json")
    with open(jsonpath, 'w') as fileson:
        json.dump(GlobalDict, fileson)
    return dict


def RefreshHtml(filter: bool=False) -> None:
    global GlobalDict
    ReadJsonDict()
    for T in TablesList:
        try:
            dict = GlobalDict[T.id]
            if filter:
                dict = FilterDict(dict)
            AnumbersToFile(T, dict)    # type: ignore
            print(T.id, "dict length:", len(dict))
            T.set_impact(len(dict))
        except KeyError as e: 
            print("KeyError:", e)
            input()
            pass


def OccList() -> None:
    Occurences: Dict[int, list[str]] = {}
    ReadJsonDict()
    li: set[int] = set()
    for d in GlobalDict.values():
        for name, anum in d.items():
            li.add(anum)
            if anum in Occurences: 
                Occurences[anum].append(name)
            else: 
                Occurences[anum] = [name]

    for anum, names in Occurences.items():
        if len(names) > 10:
            print(str(anum).rjust(6, "0"), len(names))
    print(sorted(li), len(li))



if __name__ == "__main__":

    from Abel import Abel                # type: ignore
    from Bell import Bell                # type: ignore
    from Lah import Lah                  # type: ignore
    from DyckPaths import DyckPaths      # type: ignore
    from Binomial import Binomial        # type: ignore
    from StirlingSet import StirlingSet  # type: ignore
    from Motzkin import Motzkin          # type: ignore
    from Worpitzky import Worpitzky      # type: ignore
    from Entringer import Entringer      # type: ignore

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

    #OccList()

    # RefreshHtml(True)
    
    #RefreshDatabase()

    #for T in TablesList:
    #    print(T.id, T.tex)

    #ReadJsonDict()
    #for k, v in GlobalDict.items():
    #    print(k, len(v.values()))
    
    #dict = AddTable(StirlingSet, True, True)
    #for k, v in dict.items():
    #    print(k, v)
