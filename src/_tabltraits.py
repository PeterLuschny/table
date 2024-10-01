from _tabltypes import Table, rgen, trait
from itertools import accumulate
from more_itertools import flatten
from functools import reduce
from math import lcm, gcd
from fractions import Fraction
from Binomial import Binomial, InvBinomial
import operator 

# #@

def dotproduct(vec: list[int], tor: list[int]) -> int:
    """Returns the dot product of the two vectors."""
    return sum(map(operator.mul, vec, tor))

def Triangle(T: Table, size: int) -> list[int]:
    return T.flat(size)

def Trev(T: Table, size: int) -> list[int]:
    return list(flatten([T.rev(n) for n in range(size)]))

def Tinv(T: Table, size: int) -> list[int]:
    return list(flatten(T.inv(size)))

def Trevinv(T: Table, size: int) -> list[int]:
    return list(flatten(T.revinv(size)))

def Tinvrev(T: Table, size: int) -> list[int]:
    return list(flatten(T.invrev(size)))

def Toff11(T: Table, size: int) -> list[int]:
    T11 = Table(T.off(1, 1), T.id + "off11")
    return T11.flat(size)

def Tinvrev11(T: Table, size: int) -> list[int]:
    InvT11 = T.invrev11(size)  #, T.id + "ioff11")
    return list(flatten(InvT11))

def Tacc(T: Table, size: int) -> list[int]:
    return list(flatten([T.acc(n) for n in range(size)]))

def Tdiff(T: Table, size: int) -> list[int]:
    return list(flatten([T.diff(n) for n in range(size)]))

def TablCol(T: Table, j: int, size: int) -> list[int]:
    return [T.gen(j + k)[j] for k in range(size)]

def TablCol1(T: Table, size: int) -> list[int]:
    return [T.gen(1 + k)[1] for k in range(size)]

def TablCol2(T: Table, size: int) -> list[int]:
    return [T.gen(2 + k)[2] for k in range(size)]

def TablCol3(T: Table, size: int) -> list[int]:
    return [T.gen(3 + k)[3] for k in range(size)]

def TablDiag(T: Table, j: int, size: int) -> list[int]:
    return [T.gen(j + k)[k] for k in range(size)]

def TablDiag1(T: Table, size: int) -> list[int]:
    return [T.gen(1 + k)[k] for k in range(size)]

def TablDiag2(T: Table, size: int) -> list[int]:
    return [T.gen(2 + k)[k] for k in range(size)]

def TablDiag3(T: Table, size: int) -> list[int]:
    return [T.gen(3 + k)[k] for k in range(size)]

def PolyRow(T: Table, row: int, size: int) -> list[int]:
    return [T.poly(row, x) for x in range(size)]

def PolyRow1(T: Table, size: int) -> list[int]:
    return [T.poly(1, x) for x in range(size)]

def PolyRow2(T: Table, size: int) -> list[int]:
    return [T.poly(2, x) for x in range(size)]

def PolyRow3(T: Table, size: int) -> list[int]:
    return [T.poly(3, x) for x in range(size)]

def PolyCol(T: Table, col: int, size: int) -> list[int]:
    return [T.poly(x, col) for x in range(size)]

def PolyCol1(T: Table, size: int) -> list[int]:
    return [T.poly(x, 1) for x in range(size)]

def PolyCol2(T: Table, size: int) -> list[int]:
    return [T.poly(x, 2) for x in range(size)]

def PolyCol3(T: Table, size: int) -> list[int]:
    return [T.poly(x, 3) for x in range(size)]

def PolyDiag(T: Table, size: int) -> list[int]:
    return [T.poly(n, n) for n in range(size)]

# Note our convention to exclude 0 and 1.
def RowLcmGcd(g: rgen, row: int, lg: bool) -> int:
    Z = [v for v in g(row) if v not in [-1, 0, 1]]
    if Z == []: return 1
    return lcm(*Z) if lg else gcd(*Z) 

def TablLcm(T: Table, size: int) -> list[int]:
    return [RowLcmGcd(T.gen, row, True) for row in range(size)]

def TablGcd(T: Table, size: int) -> list[int]:
    return [RowLcmGcd(T.gen, row, False) for row in range(size)]

# Note our convention to use the abs value.
def TablMax(T: Table, size: int) -> list[int]:
    return [reduce(max, (abs(t) for t in T.gen(row))) for row in range(size)]

def TablSum(T: Table, size: int) -> list[int]:
    return [T.sum(n) for n in range(size)]

def EvenSum(T: Table, size: int) -> list[int]:
    return [sum(T.gen(n)[::2]) for n in range(size)]

def OddSum(T: Table, size: int) -> list[int]:
    return [sum(T.gen(n)[1::2]) for n in range(size)]

def AltSum(T: Table, size: int) -> list[int]:
    return [sum(T.gen(n)[::2]) - sum(T.gen(n)[1::2]) for n in range(size)]

def AbsSum(T: Table, size: int) -> list[int]:
    return [sum(abs(t) for t in T.gen(n)) for n in range(size)]

def AccSum(T: Table, size: int) -> list[int]:
    return [sum(T.acc(n)) for n in range(size)]

def AccRevSum(T: Table, size: int) -> list[int]:
    return [sum(accumulate(T.rev(n))) for n in range(size)]

def AntiDSum(T: Table, size: int) -> list[int]:
    return [sum(T.antid(n)) for n in range(size)]

def ColMiddle(T: Table, size: int) -> list[int]:
    return [T.gen(n)[n // 2] for n in range(size)]

def CentralE(T: Table, size: int) -> list[int]:
    return [T.gen(2*n)[n] for n in range(size)]

def CentralO(T: Table, size: int) -> list[int]:
    return [T.gen(2*n+1)[n] for n in range(size)]

def ColLeft(T: Table, size: int) -> list[int]:
    return [T.gen(n)[0] for n in range(size)]

def ColRight(T: Table, size: int) -> list[int]:
    return [T.gen(n)[-1] for n in range(size)]

def PolyFrac(T: Table, n: int, x: Fraction) -> Fraction | int:
    return sum(c * (x ** k) for (k, c) in enumerate(T.gen(n)))

def PosHalf(T: Table, size: int) -> list[int]:
    return [((2 ** n) * PolyFrac(T, n, Fraction(1, 2))).numerator 
            for n in range(size)]

def NegHalf(T: Table, size: int) -> list[int]:
    return [(((-2) ** n) * PolyFrac(T, n, Fraction(-1, 2))).numerator for n in range(size)]

def TransNat0(T: Table, size: int) -> list[int]:
    return T.trans(lambda k: k, size)

def TransNat1(T: Table, size: int) -> list[int]:
    return T.trans(lambda k: k + 1, size)

def TransSqrs(T: Table, size: int) -> list[int]:
    return T.trans(lambda k: k * k, size)

def BinConv(T:Table, size: int) -> list[int]:
    return [dotproduct(Binomial.gen(n), T.gen(n)) 
            for n in range(size)]

def InvBinConv(T:Table, size: int) -> list[int]:
    return [dotproduct(InvBinomial.gen(n), T.gen(n)) 
            for n in range(size)]

AllTraits: dict[str, trait] =  {
    "Triangle"  : Triangle,
    "Tinv"      : Tinv,
    "Trev"      : Trev,
    "Trevinv"   : Trevinv,
    "Tinvrev"   : Tinvrev,
    "Toff11"    : Toff11,
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

def Traits(T: Table, LEN: int=10) -> None:
    for id, tr in AllTraits.items():
        name = (T.id + id).ljust(9+len(T.id), ' ') 
        print(name, tr(T, LEN))


if __name__ == "__main__":

    from Abel import Abel
    from StirlingSet import StirlingSet


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

        print(PolyDiag(T, LEN))
        print(TablLcm(T, LEN))
        print(TablGcd(T, LEN))
        print(TablMax(T, LEN))
        print(TablSum(T, LEN))
        print(EvenSum(T, LEN))
        print(OddSum(T, LEN))
        print(AltSum(T, LEN))
        print(AbsSum(T, LEN))
        print(AccSum(T, LEN))
        print(AccRevSum(T, LEN))
        print(AntiDSum(T, LEN))
        print(ColMiddle(T, LEN))
        print(CentralE(T, LEN))
        print(CentralO(T, LEN))
        print(ColLeft(T, LEN))
        print(ColRight(T, LEN))
        print(PosHalf(T, LEN))
        print(NegHalf(T, LEN))
        print(TransNat0(T, LEN))
        print(TransNat1(T, LEN))
        print(TransSqrs(T, LEN))
        print(BinConv(T, LEN))
        print(InvBinConv(T, LEN))

    #test(StirlingSet, 10)
    Traits(Abel)
    Traits(StirlingSet)
