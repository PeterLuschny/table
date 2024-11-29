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
# from copy import deepcopy
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


def TablCol(T: Table, col: int, size: int = 28) -> list[int]:
    return [T.gen(col + n)[col] for n in range(size)]


def TablCol0(T: Table, size: int = 28, rev: bool = False) -> list[int]:
    if rev:
        return TablDiag0(T, size)
    else:
        return [T.gen(n)[0] for n in range(size)]


def TablCol1(T: Table, size: int = 28, rev: bool = False) -> list[int]:
    if rev:
        return TablDiag1(T, size)
    else:
        return [T.gen(1 + n)[1] for n in range(size)]


def TablCol2(T: Table, size: int = 28, rev: bool = False) -> list[int]:
    if rev:
        return TablDiag2(T, size)
    else:
        return [T.gen(2 + n)[2] for n in range(size)]


def TablCol3(T: Table, size: int = 28, rev: bool = False) -> list[int]:
    if rev:
        return TablDiag3(T, size)
    else:
        return [T.gen(3 + n)[3] for n in range(size)]


def TablDiag(T: Table, diag: int, size: int = 28) -> list[int]:
    return [T.gen(diag + k)[k] for k in range(size)]


def TablDiag0(T: Table, size: int = 28, rev: bool = False) -> list[int]:
    if rev:
        return TablCol0(T, size)
    else:
        return [T.gen(k)[k] for k in range(size)]


def TablDiag1(T: Table, size: int = 28, rev: bool = False) -> list[int]:
    if rev:
        return TablCol1(T, size)
    else:
        return [T.gen(1 + k)[k] for k in range(size)]


def TablDiag2(T: Table, size: int = 28, rev: bool = False) -> list[int]:
    if rev:
        return TablCol2(T, size)
    else:
        return [T.gen(2 + k)[k] for k in range(size)]


def TablDiag3(T: Table, size: int = 28, rev: bool = False) -> list[int]:
    if rev:
        return TablCol3(T, size)
    else:
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

############################################################################

def Rev_Triangle(t: Table, size: int = 7) -> list[int]:
    T = RevTable(t)
    return T.flat(size)


def Rev_Trev(t: Table, size: int = 7) -> list[int]:
    T = RevTable(t)
    return list(flatten([T.rev(n) for n in range(size)]))


def Rev_Tinv(t: Table, size: int = 7) -> list[int]:
    T = RevTable(t)
    return list(flatten(T.inv(size)))


def Rev_Trevinv(t: Table, size: int = 7) -> list[int]:
    T = RevTable(t)
    return list(flatten(T.revinv(size)))


def Rev_Tinvrev(t: Table, size: int = 7) -> list[int]:
    T = RevTable(t)
    return list(flatten(T.invrev(size)))


def Rev_Toff11(t: Table, size: int = 7) -> list[int]:
    T = RevTable(t)
    T11 = Table(T.off(1, 1), T.id + "off11")
    return T11.flat(size)


def Rev_Trev11(t: Table, size: int = 7) -> list[int]:
    T = RevTable(t)
    return list(flatten([T.rev11(n) for n in range(size)]))


def Rev_Tinv11(t: Table, size: int = 7) -> list[int]:
    T = RevTable(t)
    InvT11 = T.inv11(size)
    return list(flatten(InvT11))


def Rev_Trevinv11(t: Table, size: int = 7) -> list[int]:
    T = RevTable(t)
    return list(flatten(T.revinv11(size)))


def Rev_Tinvrev11(t: Table, size: int = 7) -> list[int]:
    T = RevTable(t)
    InvrevT11 = T.invrev11(size)
    return list(flatten(InvrevT11))


def Rev_Talt(t: Table, size: int = 7) -> list[int]:
    T = RevTable(t)
    return list(flatten([T.alt(n) for n in range(size)]))


def Rev_Tacc(t: Table, size: int = 7) -> list[int]:
    T = RevTable(t)
    return list(flatten([T.acc(n) for n in range(size)]))


def Rev_Tdiff(t: Table, size: int = 7) -> list[int]:
    T = RevTable(t)
    return list(flatten([T.diff(n) for n in range(size)]))


def Rev_Tder(t: Table, size: int = 7) -> list[int]:
    T = RevTable(t)
    return list(flatten([T.der(n) for n in range(size)]))


# Needs 9 rows
def Rev_Tantidiag(t: Table, size: int = 9) -> list[int]:
    T = RevTable(t)
    return list(flatten([T.antidiag(n) for n in range(size)]))


def Rev_TablCol(t: Table, col: int, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.gen(col + n)[col] for n in range(size)]


def Rev_TablCol0(T: Table, size: int = 28) -> list[int]:
    #if rev:
    return TablDiag0(T, size)
    #else:
    #    return [T.gen(n)[0] for n in range(size)]


def Rev_TablCol1(T: Table, size: int = 28) -> list[int]:
    #if rev:
    return TablDiag1(T, size)
    #else:
    #    return [T.gen(1 + n)[1] for n in range(size)]


def Rev_TablCol2(T: Table, size: int = 28) -> list[int]:
    #if rev:
    return TablDiag2(T, size)
    #else:
    #    return [T.gen(2 + n)[2] for n in range(size)]


def Rev_TablCol3(T: Table, size: int = 28) -> list[int]:
    #if rev:
    return TablDiag3(T, size)
    #else:
    #    return [T.gen(3 + n)[3] for n in range(size)]


def Rev_TablDiag(t: Table, diag: int, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.gen(diag + k)[k] for k in range(size)]


def Rev_TablDiag0(T: Table, size: int = 28) -> list[int]:
    #if rev:
    return TablCol0(T, size)
    #else:
    #    return [T.gen(k)[k] for k in range(size)]


def Rev_TablDiag1(T: Table, size: int = 28) -> list[int]:
    #if rev:
    return TablCol1(T, size)
    #else:
    #    return [T.gen(1 + k)[k] for k in range(size)]


def Rev_TablDiag2(T: Table, size: int = 28) -> list[int]:
    #if rev:
    return TablCol2(T, size)
    #else:
    #    return [T.gen(2 + k)[k] for k in range(size)]


def Rev_TablDiag3(T: Table, size: int = 28) -> list[int]:
    #if rev:
    return TablCol3(T, size)
    #else:
    #    return [T.gen(3 + k)[k] for k in range(size)]


def Rev_PolyRow(t: Table, row: int, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.poly(row, x) for x in range(size)]


def Rev_PolyRow1(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.poly(1, x) for x in range(size)]


def Rev_PolyRow2(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.poly(2, x) for x in range(size)]


def Rev_PolyRow3(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.poly(3, x) for x in range(size)]


def Rev_PolyCol(t: Table, col: int, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.poly(x, col) for x in range(size)]


def Rev_PolyCol1(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.poly(x, 1) for x in range(size)]


def Rev_PolyCol2(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.poly(x, 2) for x in range(size)]


def Rev_PolyCol3(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.poly(x, 3) for x in range(size)]


def Rev_PolyDiag(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.poly(n, n) for n in range(size)]


# Note our convention to exclude 0 and 1.
def Rev_RowLcmGcd(g: rgen, row: int, lg: bool) -> int:
    Z = [v for v in g(row) if v not in [-1, 0, 1]]
    if Z == []:
        return 1
    return lcm(*Z) if lg else gcd(*Z)


def Rev_TablLcm(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [RowLcmGcd(T.gen, row, True) for row in range(size)]


def Rev_TablGcd(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [RowLcmGcd(T.gen, row, False) for row in range(size)]


# Note our convention to use the abs value.
def Rev_TablMax(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [reduce(max, (abs(t) for t in T.gen(row))) for row in range(size)]


def Rev_TablSum(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.sum(n) for n in range(size)]


def Rev_EvenSum(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [sum(T.gen(n)[::2]) for n in range(size)]


def Rev_OddSum(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [sum(T.gen(n)[1::2]) for n in range(size)]


def Rev_AltSum(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [sum(T.gen(n)[::2]) - sum(T.gen(n)[1::2]) for n in range(size)]


def Rev_AbsSum(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [sum(abs(t) for t in T.gen(n)) for n in range(size)]


def Rev_AccSum(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [sum(T.acc(n)) for n in range(size)]


def Rev_AccRevSum(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [sum(accumulate(T.rev(n))) for n in range(size)]


def Rev_AntiDSum(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [sum(T.antidiag(n)) for n in range(size)]


def Rev_ColMiddle(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.gen(n)[n // 2] for n in range(size)]


def Rev_CentralE(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.gen(2 * n)[n] for n in range(size)]


def Rev_CentralO(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.gen(2 * n + 1)[n] for n in range(size)]


def Rev_ColLeft(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.gen(n)[0] for n in range(size)]


def Rev_ColRight(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [T.gen(n)[-1] for n in range(size)]


def Rev_PolyFrac(t: Table, n: int, x: Fraction) -> Fraction | int:
    T = RevTable(t)
    return sum(c * (x**k) for (k, c) in enumerate(T.gen(n)))


def Rev_PosHalf(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [((2**n) * PolyFrac(T, n, Fraction(1, 2))).numerator 
            for n in range(size)]


def Rev_NegHalf(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [(((-2) ** n) * PolyFrac(T, n, Fraction(-1, 2))).numerator 
            for n in range(size)]


def Rev_TransNat0(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return T.trans(lambda k: k, size)


def Rev_TransNat1(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return T.trans(lambda k: k + 1, size)


def Rev_TransSqrs(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return T.trans(lambda k: k * k, size)


def Rev_BinConv(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [dotproduct(Binomial.gen(n), T.gen(n)) for n in range(size)]


def Rev_InvBinConv(t: Table, size: int = 28) -> list[int]:
    T = RevTable(t)
    return [dotproduct(InvBinomial.gen(n), T.gen(n)) for n in range(size)]

# sum((-1)**(n-k)*Binomial.val(n,k)*Trev(n, k) for k in range(n+1)) for n in range(size)])


"""The basic construction is a map
    (Table:Class, Trait:Function) -> (Anum:Url, TreatInfo:TeXString)
"""

TraitInfo: TypeAlias = Tuple[trait, int, str]

# Registered symbol in superscript with \textbf{amssymb} package:\\[4pt]
# Code\textsuperscript{\tiny{\circledR}}\\[4pt]
# Code\textsuperscript{\circledR}\\[4pt]\\[4pt]

AllTraits: dict[str, TraitInfo] = {
    "Triangle     ": (Triangle,  7, r"\(T_{n, k}\)"),
    "Tinv         ": (Tinv,      7, r"\(T^{-1}_{n, k}\)"),
    "Trev         ": (Trev,      7, r"\(T_{n, n - k}\)"),
    "Trevinv      ": (Trevinv,   7, r"\(T^{-1}_{n, n - k}\)"),
    "Tinvrev      ": (Tinvrev,   7, r"\((T_{n, n - k})^{-1}\)"),
    "Toff11       ": (Toff11,    7, r"\(T_{n + 1, k + 1} \)"),
    "Trev11       ": (Trev11,    7, r"\(T_{n + 1, n - k + 1} \)"),
    "Tinv11       ": (Tinv11,    7, r"\(T^{-1}_{n + 1, k + 1}\)"),
    "Trevinv11    ": (Trevinv11, 7, r"\(T^{-1}_{n + 1, n - k + 1}\)"),
    "Tinvrev11    ": (Tinvrev11, 7, r"\((T_{n + 1, n - k + 1})^{-1}\)"),
    "Tantidiag    ": (Tantidiag, 9, r"\(T_{n - k, k} \ \ (k \le n/2)\)"),
    "Tacc         ": (Tacc,      7, r"\(\sum_{j=0}^{k} T_{n, j}\)"),
    "Talt         ": (Talt,      7, r"\(T_{n, k}\ (-1)^{k}\)"),
    "Tder         ": (Tder,      7, r"\(T_{n + 1, k + 1}\ (k + 1) \)"),
    "TablCol0     ": (TablCol0,  28, r"\(T_{n    , 0}\)"),
    "TablCol1     ": (TablCol1,  28, r"\(T_{n + 1, 1}\)"),
    "TablCol2     ": (TablCol2,  28, r"\(T_{n + 2, 2}\)"),
    "TablCol3     ": (TablCol3,  28, r"\(T_{n + 3, 3}\)"),
    "TablDiag0    ": (TablDiag0, 28, r"\(T_{n    , n}\)"),
    "TablDiag1    ": (TablDiag1, 28, r"\(T_{n + 1, n}\)"),
    "TablDiag2    ": (TablDiag2, 28, r"\(T_{n + 2, n}\)"),
    "TablDiag3    ": (TablDiag3, 28, r"\(T_{n + 3, n}\)"),
    "TablLcm      ": (TablLcm,   28, r"\(\text{lcm}_{k=0}^{n}\ | T_{n, k} |\ \  (T_{n,k}>1)\)"),
    "TablGcd      ": (TablGcd,   28, r"\(\text{gcd}_{k=0}^{n}\ | T_{n, k} |\ \  (T_{n,k}>1)\)"),
    "TablMax      ": (TablMax,   28, r"\(\text{max}_{k=0}^{n}\ | T_{n, k} |\)"),
    "TablSum      ": (TablSum,   28, r"\(\sum_{k=0}^{n} T_{n, k}\)"),
    "EvenSum      ": (EvenSum,   28, r"\(\sum_{k=0}^{n} T_{n, k}\  [2 | k]\)"),
    "OddSum       ": (OddSum,    28, r"\(\sum_{k=0}^{n} T_{n, k}\  (1 - [2 | k])\)"),
    "AltSum       ": (AltSum,    28, r"\(\sum_{k=0}^{n} T_{n, k}\  (-1)^{k}\)"),
    "AbsSum       ": (AbsSum,    28, r"\(\sum_{k=0}^{n} | T_{n, k} |\)"),
    "AccSum       ": (AccSum,    28, r"\(\sum_{k=0}^{n} \sum_{j=0}^{k} T_{n, j}\)"),
    "AccRevSum    ": (AccRevSum, 28, r"\(\sum_{k=0}^{n} \sum_{j=0}^{k} T_{n, n - j}\)"),
    "AntiDSum     ": (AntiDSum,  28, r"\(\sum_{k=0}^{n/2} T_{n - k, k}\)"),
    "ColMiddle    ": (ColMiddle, 28, r"\(T_{n, n / 2}\)"),
    "CentralE     ": (CentralE,  28, r"\(T_{2 n, n}\)"),
    "CentralO     ": (CentralO,  28, r"\(T_{2 n + 1, n}\)"),
    "PosHalf      ": (PosHalf,   28, r"\(\sum_{k=0}^{n} T_{n, k} \ 2^{n - k} \)"),
    "NegHalf      ": (NegHalf,   28, r"\(\sum_{k=0}^{n} T_{n, k} \ (-2)^{n - k} \)"),
    "TransNat0    ": (TransNat0, 28, r"\(\sum_{k=0}^{n} T_{n, k} \ k\)"),
    "TransNat1    ": (TransNat1, 28, r"\(\sum_{k=0}^{n} T_{n, k} \ (k + 1)\)"),
    "TransSqrs    ": (TransSqrs, 28, r"\(\sum_{k=0}^{n} T_{n, k} \ k^{2}\)"),
    "BinConv      ": (BinConv,   28, r"\(\sum_{k=0}^{n} T_{n, k} \ \binom{n}{k} \)"),
    "InvBinConv   ": (InvBinConv, 28, r"\(\sum_{k=0}^{n} T_{n, k} \ (-1)^{n - k} \ \binom{n}{k} \)"),
    "PolyRow1     ": (PolyRow1,  28, r"\(\sum_{k=0}^{1} T_{1, k}\  n^k\)"),
    "PolyRow2     ": (PolyRow2,  28, r"\(\sum_{k=0}^{2} T_{2, k}\  n^k\)"),
    "PolyRow3     ": (PolyRow3,  28, r"\(\sum_{k=0}^{3} T_{3, k}\  n^k\)"),
    "PolyCol2     ": (PolyCol2,  28, r"\(\sum_{k=0}^{n} T_{n, k}\  2^k\)"),
    "PolyCol3     ": (PolyCol3,  28, r"\(\sum_{k=0}^{n} T_{n, k}\  3^k\)"),
    "PolyDiag     ": (PolyDiag,  28, r"\(\sum_{k=0}^{n} T_{n, k}\  n^k\)"),
#
    "RevTinv      ": (Rev_Tinv,      7, r"\(T^{-1}_{n, n-k}\)"),
    "RevTrevinv   ": (Rev_Trevinv,   7, r"\(T^{-1}_{n, n-k}\)"),
    "RevToff11    ": (Rev_Toff11,    7, r"\(T_{n + 1, n-k} \)"),
    "RevTrev11    ": (Rev_Trev11,    7, r"\(T_{n + 1, n-k} \)"),
    "RevTinv11    ": (Rev_Tinv11,    7, r"\(T^{-1}_{n + 1, n-k}\)"),
    "RevTrevinv11 ": (Rev_Trevinv11, 7, r"\(T^{-1}_{n + 1, n-k}\)"),
    "RevTinvrev11 ": (Rev_Tinvrev11, 7, r"\((T_{n + 1, n-k + 1})^{-1}\)"),
    "RevTantidiag ": (Rev_Tantidiag, 9, r"\(T_{n - k, n - 2k} \ \ (k \le n/2)\)"),
    "RevTacc      ": (Rev_Tacc,      7, r"\(\sum_{j=0}^{n-k} T_{n, n-j}\)"),
    "RevTalt      ": (Rev_Talt,      7, r"\(T_{n, n-k}\ (-1)^{n-k}\)"),
    "RevTder      ": (Rev_Tder,      7, r"\(T_{n + 1, n-k}\ (n-k + 1) \)"),
    "RevEvenSum   ": (Rev_EvenSum,   28, r"\(\sum_{k=0}^{n} T_{n, n-k}\  [2 | k]\)"),
    "RevOddSum    ": (Rev_OddSum,    28, r"\(\sum_{k=0}^{n} T_{n, n-k}\  (1 - [2 | k])\)"),
    "RevAccRevSum ": (Rev_AccRevSum, 28, r"\(\sum_{k=0}^{n} \sum_{j=0}^{k} T_{n, n - j}\)"),
    "RevAntiDSum  ": (Rev_AntiDSum,  28, r"\(\sum_{k=0}^{n/2} T_{n - k, n-k}\)"),
    "RevColMiddle ": (Rev_ColMiddle, 28, r"\(T_{n, n / 2}\)"),
    "RevCentralO  ": (Rev_CentralO,  28, r"\(T_{2 n + 1, n}\)"),
    "RevNegHalf   ": (Rev_NegHalf,   28, r"\(\sum_{k=0}^{n} T_{n, n-k}\ (-2)^{n - k} \)"),
    "RevTransNat0 ": (Rev_TransNat0, 28, r"\(\sum_{k=0}^{n} T_{n, n-k}\ k\)"),
    "RevTransNat1 ": (Rev_TransNat1, 28, r"\(\sum_{k=0}^{n} T_{n, n-k}\ (k + 1)\)"),
    "RevTransSqrs ": (Rev_TransSqrs, 28, r"\(\sum_{k=0}^{n} T_{n, n-k}\ k^{2}\)"),
    "RevPolyRow1  ": (Rev_PolyRow1,  28, r"\(\sum_{k=0}^{1} T_{1, n-k}\  n^k\)"),
    "RevPolyRow2  ": (Rev_PolyRow2,  28, r"\(\sum_{k=0}^{2} T_{2, n-k}\  n^k\)"),
    "RevPolyRow3  ": (Rev_PolyRow3,  28, r"\(\sum_{k=0}^{3} T_{3, n-k}\  n^k\)"),
    "RevPolyCol3  ": (Rev_PolyCol3,  28, r"\(\sum_{k=0}^{n} T_{n, n-k}\  3^k\)"),
    "RevPolyDiag  ": (Rev_PolyDiag,  28, r"\(\sum_{k=0}^{n} T_{n, n-k}\  n^k\)"),
}


def TableTraits(T: Table) -> None:
    for id, tr in AllTraits.items():
        name = (T.id + id).ljust(9 + len(T.id), " ")
        print(name, tr[0](T, tr[1]))


GlobalDict: Dict[str, Dict[str, int]] = {}


def ShowGlobalDict() -> None:
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
    addtoglobal: bool = False
) -> Dict[str, int]:
    """Collects the A-nunmbers of the traits of T present in the OEIS."""
    print(f"*** Table {T.id} under construction ***")
    global GlobalDict


    tdict: Dict[str, int] = {}
    for trid, tr in AllTraits.items():
        name = (T.id + "_" + trid).ljust(10 + len(T.id), " ")
        seq: list[int] = tr[0](T, tr[1]) 
        if seq != []:
            tdict[name] = QueryOEIS(seq, info)

    if addtoglobal:
        GlobalDict[T.id] = tdict

    return tdict


header = '<html><head><title>Traits</title><meta charset="utf-8"><meta name="viewport" content="width=device-width"><script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"> window.MathJax = {loader: {load: ["[tex]/bbox"]}, tex: {packages: {"[+]": ["bbox"]}}}</script></head><body width="40%"><iframe name="OEISframe" frameborder="0" scrolling="yes" width="58%" height="2200" align="left" title="Sequences"'

def DictToHtml(
    T: Table, 
    dict: Dict[str, int],
    info: bool = False
)  -> tuple[int, int, int]:
    """Transforms a dictionary {trait, anum} representing the Table T
        into two Html files: TNameTraits.html and TNameMissing.html.
        A trait is 'missing' if the anum in the dictionary is 0.
    """

    SRC = f'https://oeis.org/{T.sim[0]}'
    TID = (T.id).capitalize()
    SH = f'src={SRC}></iframe><p><span style="white-space: pre">     {TID}</span><br>'
    hitpath = GetRoot(f"data/{T.id}Traits.html")
    mispath = GetRoot(f"data/{T.id}Missing.html")
    head = header.replace("Traits", T.id)
    TeX = r"\(\bbox[yellow, 5px]{\color{DarkGreen} T_{n, k} \ = \ TTEX } \)" 
    TEX = TeX.replace("TTEX", T.tex)
    url = f"<a href='https://oeis.org/{T.sim[0]}' target='OEISframe'>{T.sim[0]}</a> "
    hits = misses = doubles = 0
    anumlist: set[int] = set()
    oldanum = T.sim[0] 

    with open(hitpath, "w+", encoding="utf-8") as oeis:
        with open(mispath, "w+", encoding="utf-8") as miss:
            oeis.write(head); oeis.write(SH); oeis.write(url + TEX)
            miss.write(head); miss.write(SH); miss.write(url + TEX)
            d = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}

            for fullname, anum in d.items():
                if info: print(f"   {fullname} -> {anum}")
                traitfun, size, tex = AllTraits[fullname.split("_")[1]]
                seq = SeqToString(traitfun(T, size), 40, 20) 
                if anum == 0:
                    miss.write(f"<br>{tex} &nbsp;&#x27A4;&nbsp; {fullname.split("_")[1]} &nbsp;&#x27A4;&nbsp; " + seq)
                    misses += 1
                else:
                    if anum in anumlist: 
                        doubles += 1
                    Anum = 'A' + str(anum).rjust(6, "0")
                    if anum == oldanum:
                        url = '---------- '
                    else:
                        url = f"<a href='https://oeis.org/{Anum}' target='OEISframe'>{Anum}</a>"
                    oldanum = anum 
                    oeis.write(f"<br>{url} {tex} &nbsp;&#x27A4;&nbsp; {fullname.split("_")[1]} &nbsp;&#x27A4;&nbsp; " + seq)
                    hits += 1
                    anumlist.add(anum)

            L = "<a href='https://peterluschny.github.io/table/"
            A = f"{L}{T.id}Traits.html'>[online]</a>"
            B = f"{L}{T.id}Missing.html'>[missing]</a>"
            C = f"{L}index.html'>[index]</a>"

            oeis.write(f"<p style='color:blue'>{B}{C}</p></body></html>")
            miss.write(f"<p style='color:blue'>{A}{C}</p></body></html>")

    print(f"Hits: {hits}, Misses: {misses}, Doubles: {doubles}")
    return (hits, misses, doubles)


indheader = "<!DOCTYPE html><html lang='en'><head><title>Index</title><meta name='viewport' content='width=device-width,initial-scale=1'><style type='text/css'>body{font-family:Calabri,Arial,sans-serif;font-size:18px;background-color: #804040; color: #C0C0C0}</style><base href='https://peterluschny.github.io/table/' target='_blank'></head><body><table><thead><tr><th align='left'>Sequence</th><th align='left'>OEIS</th><th align='left'>Missing</th></tr></thead><tbody><tr>"

def warn() -> None:
    print("Are you sure? This takes 3-4 hours.")
    print("Don't forget to update Tables.py first.")
    print("Delete the json file?")
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
            dict = AnumberDict(T, True, True)  # type: ignore 
            DictToHtml(T, dict, True)       # type: ignore
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
    try:
        with open(jsonpath, 'r') as file:
            GlobalDict = json.load(file)
    except FileNotFoundError:
        print("No file 'AllTraits.json' found.")
        GlobalDict = {}
        print("New GlobalDict created.")
        return

    print("GlobalDict loaded with file AllTraits.json!")


def AddTable(
    T: Table,
    dict: Dict[str, int] = {}
) -> Dict[str, int]:
    ReadJsonDict()

    if dict == {}:    #info, add2globalDict
        dict = AnumberDict(T, True, True)
    print("Dict length:", len(dict))
    DictToHtml(T, dict, True)
    jsonpath = GetRoot(f"data/AllTraits.json")
    with open(jsonpath, 'w+') as fileson:
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
            DictToHtml(T, dict)    # type: ignore
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
    from Narayana import Narayana        # type: ignore
    from FallingFactorial import FallingFactorial  # type: ignore
    from Divisibility import Divisibility  # type: ignore

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

    # OccList()
    # RefreshHtml(True)

    #RefreshDatabase()

    #for T in TablesList:
    #    print(T.id, T.tex)
    #ReadJsonDict()
    #for k, v in GlobalDict.items():
    #    print(k, len(v.values()))

    #AddTable(Moebius) # type: ignore

    #for k, v in dict.items():
    #    print(k, v)

    #for T in TablesList:
    #    AddTable(T) # type: ignore
