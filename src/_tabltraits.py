from _tabltypes import Table, rgen, trait
from _tabloeis import QueryOEIS
from typing import Dict
from itertools import accumulate
from more_itertools import flatten
from functools import reduce
from math import lcm, gcd
from fractions import Fraction
from Binomial import Binomial, InvBinomial
import operator 
from Tables import Tables

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

def Tacc(T: Table, size: int = 7) -> list[int]:
    return list(flatten([T.acc(n) for n in range(size)]))

def Tdiff(T: Table, size: int = 7) -> list[int]:
    return list(flatten([T.diff(n) for n in range(size)]))

def TablCol(T: Table, j: int, size: int = 28) -> list[int]:
    return [T.gen(j + k)[j] for k in range(size)]

def TablCol1(T: Table, size: int = 28) -> list[int]:
    return [T.gen(1 + k)[1] for k in range(size)]

def TablCol2(T: Table, size: int = 28) -> list[int]:
    return [T.gen(2 + k)[2] for k in range(size)]

def TablCol3(T: Table, size: int = 28) -> list[int]:
    return [T.gen(3 + k)[3] for k in range(size)]

def TablDiag(T: Table, j: int, size: int = 28) -> list[int]:
    return [T.gen(j + k)[k] for k in range(size)]

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
    if Z == []: return 1
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
    return [sum(T.antid(n)) for n in range(size)]

def ColMiddle(T: Table, size: int = 28) -> list[int]:
    return [T.gen(n)[n // 2] for n in range(size)]

def CentralE(T: Table, size: int = 28) -> list[int]:
    return [T.gen(2*n)[n] for n in range(size)]

def CentralO(T: Table, size: int = 28) -> list[int]:
    return [T.gen(2*n+1)[n] for n in range(size)]

def ColLeft(T: Table, size: int = 28) -> list[int]:
    return [T.gen(n)[0] for n in range(size)]

def ColRight(T: Table, size: int = 28) -> list[int]:
    return [T.gen(n)[-1] for n in range(size)]

def PolyFrac(T: Table, n: int, x: Fraction) -> Fraction | int:
    return sum(c * (x ** k) for (k, c) in enumerate(T.gen(n)))

def PosHalf(T: Table, size: int = 28) -> list[int]:
    return [((2 ** n) * PolyFrac(T, n, Fraction(1, 2))).numerator 
            for n in range(size)]

def NegHalf(T: Table, size: int = 28) -> list[int]:
    return [(((-2) ** n) * PolyFrac(T, n, Fraction(-1, 2))).numerator for n in range(size)]

def TransNat0(T: Table, size: int = 28) -> list[int]:
    return T.trans(lambda k: k, size)

def TransNat1(T: Table, size: int = 28) -> list[int]:
    return T.trans(lambda k: k + 1, size)

def TransSqrs(T: Table, size: int = 28) -> list[int]:
    return T.trans(lambda k: k * k, size)

def BinConv(T:Table, size: int = 28) -> list[int]:
    return [dotproduct(Binomial.gen(n), T.gen(n)) 
            for n in range(size)]

def InvBinConv(T:Table, size: int = 28) -> list[int]:
    return [dotproduct(InvBinomial.gen(n), T.gen(n)) 
            for n in range(size)]

AllTraits: dict[str, trait] =  {
    "Triangle"  : Triangle,
    "Tinv"      : Tinv,
    "Trev"      : Trev,
    "Trevinv"   : Trevinv,
    "Tinvrev"   : Tinvrev,
    "Toff11"    : Toff11,
    "Trev11"    : Trev11,
    "Tinv11"    : Tinv11,
    "Trevinv11" : Trevinv11,
    "Tinvrev11" : Tinvrev11,
    "Tacc"      : Tacc,
    "Tdiff"     : Tdiff,
    "TablCol1"  : TablCol1,
    "TablCol2"  : TablCol2,
    "TablCol3"  : TablCol3,
    "TablDiag1" : TablDiag1,
    "TablDiag2" : TablDiag2,
    "TablDiag3" : TablDiag3,
    "PolyRow1"  : PolyRow1,
    "PolyRow2"  : PolyRow2,
    "PolyRow3"  : PolyRow3,
    "PolyCol1"  : PolyCol1,
    "PolyCol2"  : PolyCol2,
    "PolyCol3"  : PolyCol3,
    "PolyDiag"  : PolyDiag,
    "TablLcm"   : TablLcm,
    "TablGcd"   : TablGcd,
    "TablMax"   : TablMax,
    "TablSum"   : TablSum,
    "EvenSum"   : EvenSum,
    "OddSum"    : OddSum,
    "AltSum"    : AltSum,
    "AbsSum"    : AbsSum,
    "AccSum"    : AccSum,
    "AccRevSum" : AccRevSum,
    "AntiDSum"  : AntiDSum,
    "ColMiddle" : ColMiddle,
    "CentralE"  : CentralE,
    "CentralO"  : CentralO,
    "PosHalf"   : PosHalf,
    "NegHalf"   : NegHalf,
    "TransSqrs" : TransSqrs,
    "TransNat0" : TransNat0,
    "TransNat1" : TransNat1,
    "BinConv"   : BinConv,
    "InvBinConv": InvBinConv,
}

def TraitsList(T: Table) -> None:
    for id, tr in AllTraits.items():
        name = (T.id + id).ljust(9 + len(T.id), ' ') 
        print(name, tr(T)) # type: ignore


def AnumbersDict(T: Table) -> Dict[str, tuple[int, int, int]]:
    """Collects the A-nunmbers of traits present in the OEIS."""

    anum: Dict[str, tuple[int, int, int]] = {}

    for id, trai in AllTraits.items():
        name = (T.id + id).ljust(9 + len(T.id), ' ')
        # use the defaults: 7 rows or 28 terms!
        seq = trai(T)    # type: ignore
        if seq != []:
            anum[name] = QueryOEIS(seq) # type: ignore

    return anum

OEISDict: Dict[str, Dict[str, tuple[int, int, int]]] = {} 

def BuildOEISDict() -> None:
    """Joins the traits with the A-numbers present in the OEIS."""
    for T in Tables:
        OEISDict[T.id] = AnumbersDict(T) # type: ignore

    for tabl, dict in OEISDict.items():
        print("*** Table", tabl, "***")
        for trait in dict:
            print('   ', f"{trait} -> {dict[trait]}")


def OEISDictToFile() -> None:
    """Saves the A-numbers of traits present in the OEIS to a file."""
    for T in Tables[32:33]:
        OEISDict[T.id] = AnumbersDict(T) # type: ignore

    tablpath = "Traits.html"
    with open(tablpath, "w+", encoding="utf-8") as dest:
        dest.write("<!doctype html><title>Traits</title><style>p{font-family:monospace;font-size:xx-small;}</style><p>\n")
        for tabl, dict in OEISDict.items():
            print(f"*** Table {tabl} ***", flush = True)
            for trait in dict:
                print(f"     {trait} -> {dict[trait]}")
                n = dict[trait][0]
                if n != 0:
                    num = str(n).rjust(6, '0')
                    url = f"<a href='https://oeis.org/A{num}'>A{num}</a>" 
                    dest.write(f"<br>{url} {trait}")

    print(f"Info: Traits represented in the OEIS written to {tablpath}.")


if __name__ == "__main__":

    from Abel import Abel               # type: ignore
    from StirlingSet import StirlingSet # type: ignore

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
    # print(AnumbersDict(StirlingSet))
    
    def tost() -> None:
        for i in range(2): 
            T = Tables[i]                    # type: ignore
            OEISDict[T.id] = AnumbersDict(T) # type: ignore

        for tabl, dict in OEISDict.items():
            print("*** Table", tabl, "***")
            for trait in dict:
                print('   ', trait, '->', dict[trait])

    #tost()
    OEISDictToFile()
