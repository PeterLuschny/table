from functools import cache
from _tabltypes import Table
from Divisibility import divisibility

"""Moebius Matrix.

[0] 1
[1] 0,  1
[2] 0, -1,  1
[3] 0, -1,  0,  1
[4] 0,  0, -1,  0,  1
[5] 0, -1,  0,  0,  0, 1
[6] 0,  1, -1, -1,  0, 0, 1
[7] 0, -1,  0,  0,  0, 0, 0, 1
[8] 0,  0,  0,  0, -1, 0, 0, 0, 1
[9] 0,  0,  0, -1,  0, 0, 0, 0, 0, 1
"""


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


Moebius = Table(
    moebius,
    "Moebius",
    ["A363914", "A054525"],
    "A000000",
    r"M^{-1}(n, k); M(n, k) = [k \le n \ \& \ k | n]",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Moebius)


"""
Dict length: 68
   Moebius_Trevinv       -> 0
   Moebius_Tantidiag     -> 0
   Moebius_Tacc          -> 0
   Moebius_BinConv       -> 0
   Moebius_InvBinConv    -> 0
   Moebius_RevToff11     -> 0
   Moebius_RevTrev11     -> 0
   Moebius_RevTacc       -> 0
   Moebius_RevTalt       -> 0
   Moebius_RevTder       -> 0
   Moebius_RevAntiDSum   -> 0
   Moebius_RevNegHalf    -> 0
   Moebius_RevTransSqrs  -> 0
   Moebius_RevPolyCol3   -> 0
   Moebius_RevPolyDiag   -> 0
   Moebius_TablCol0      -> 7
   Moebius_TablDiag1     -> 7
   Moebius_TablDiag2     -> 7
   Moebius_TablDiag3     -> 7
   Moebius_TablSum       -> 7
   Moebius_EvenSum       -> 7
   Moebius_OddSum        -> 7
   Moebius_AltSum        -> 7
   Moebius_CentralO      -> 7
   Moebius_RevEvenSum    -> 7
   Moebius_RevOddSum     -> 7
   Moebius_RevCentralO   -> 7
   Moebius_AccSum        -> 10
   Moebius_AccRevSum     -> 10
   Moebius_TransNat0     -> 10
   Moebius_TransNat1     -> 10
   Moebius_RevAccRevSum  -> 10
   Moebius_RevTransNat0  -> 10
   Moebius_RevTransNat1  -> 10
   Moebius_Trev          -> 12
   Moebius_Trev11        -> 12
   Moebius_TablCol2      -> 12
   Moebius_TablDiag0     -> 12
   Moebius_TablLcm       -> 12
   Moebius_TablGcd       -> 12
   Moebius_TablMax       -> 12
   Moebius_CentralE      -> 12
   Moebius_RevTantidiag  -> 12
   Moebius_RevPolyRow1   -> 12
   Moebius_PolyRow1      -> 27
   Moebius_RevPolyRow2   -> 27
   Moebius_RevColMiddle  -> 35
   Moebius_PolyRow2      -> 2378
   Moebius_RevPolyRow3   -> 5563
   Moebius_TransSqrs     -> 7434
   Moebius_PolyRow3      -> 7531
   Moebius_TablCol1      -> 8966
   Moebius_PolyCol2      -> 27375
   Moebius_AbsSum        -> 34444
   Moebius_Tinv11        -> 51731
   Moebius_PolyCol3      -> 54718
   Moebius_AntiDSum      -> 98018
   Moebius_Tinv          -> 113704
   Moebius_Trevinv11     -> 113998
   Moebius_Tder          -> 127448
   Moebius_ColMiddle     -> 128174
   Moebius_Toff11        -> 174852
   Moebius_PolyDiag      -> 252764
   Moebius_Triangle      -> 363914
   Moebius_Talt          -> 363914
   Moebius_TablCol3      -> 365807
   Moebius_NegHalf       -> 367773
   Moebius_PosHalf       -> 367774
Hits: 53, Misses: 15, Doubles: 28, Distinct: 25
"""