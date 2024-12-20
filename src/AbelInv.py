from functools import cache
from _tabltypes import Table
from Binomial import binomial
from Power import power

'''
Inverse of Abel, unsigned version.
Triangle of idempotent numbers 

[0]  1;
[1]  0,  1;
[2]  0,  2,    1;
[3]  0,  3,    6,     1;
[4]  0,  4,   24,    12,     1;
[5]  0,  5,   80,    90,    20,     1;
[6]  0,  6,  240,   540,   240,    30,     1;
[7]  0,  7,  672,  2835,  2240,   525,    42,    1;
[8]  0,  8, 1792, 11340, 15680,  5880,   980,   56,  1;
[9]  0,  9, 4608, 41580, 94080, 52920, 11760, 1260, 72, 1;
'''

@cache
def abelinv(n: int) -> list[int]:

    b = binomial(n)
    p = power(n)
    return [b[k] * p[k] for k in range(n + 1)]



AbelInv = Table(
    abelinv,
    "AbelInv",
    ["A059297", "A059298"],
    "A137452",
    r"\binom{n}{k} k^{n - k}",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(AbelInv)

"""
   AbelInv_Trevinv       -> 0
   AbelInv_Tantidiag     -> 0
   AbelInv_Tacc          -> 0
   AbelInv_Tder          -> 0
   AbelInv_TablDiag2     -> 0
   AbelInv_TablDiag3     -> 0
   AbelInv_TablLcm       -> 0
   AbelInv_TablMax       -> 0
   AbelInv_AccSum        -> 0
   AbelInv_AccRevSum     -> 0
   AbelInv_ColMiddle     -> 0
   AbelInv_CentralO      -> 0
   AbelInv_TransNat1     -> 0
   AbelInv_TransSqrs     -> 0
   AbelInv_PolyRow3      -> 0
   AbelInv_RevToff11     -> 0
   AbelInv_RevTrev11     -> 0
   AbelInv_RevTantidiag  -> 0
   AbelInv_RevTacc       -> 0
   AbelInv_RevTder       -> 0
   AbelInv_RevOddSum     -> 0
   AbelInv_RevAccRevSum  -> 0
   AbelInv_RevCentralO   -> 0
   AbelInv_RevNegHalf    -> 0
   AbelInv_RevTransNat0  -> 0
   AbelInv_RevTransNat1  -> 0
   AbelInv_RevTransSqrs  -> 0
   AbelInv_TablCol0      -> 7
   AbelInv_TablDiag0     -> 12
   AbelInv_RevPolyRow1   -> 12
   AbelInv_TablCol1      -> 27
   AbelInv_TablGcd       -> 27
   AbelInv_PolyRow1      -> 27
   AbelInv_TablSum       -> 248
   AbelInv_AbsSum        -> 248
   AbelInv_TablCol2      -> 1788
   AbelInv_TablDiag1     -> 2378
   AbelInv_AltSum        -> 3725
   AbelInv_RevPolyRow2   -> 5408
   AbelInv_PolyRow2      -> 5563
   AbelInv_EvenSum       -> 9121
   AbelInv_OddSum        -> 9565
   AbelInv_TablCol3      -> 36216
   AbelInv_Triangle      -> 59297
   AbelInv_Talt          -> 59297
   AbelInv_Toff11        -> 59298
   AbelInv_Trev          -> 59299
   AbelInv_RevTalt       -> 59299
   AbelInv_Trev11        -> 59300
   AbelInv_Tinv11        -> 61356
   AbelInv_RevPolyRow3   -> 100536
   AbelInv_Tinv          -> 137452
   AbelInv_Trevinv11     -> 139526
   AbelInv_TransNat0     -> 185298
   AbelInv_RevEvenSum    -> 195509
   AbelInv_PosHalf       -> 216689
   AbelInv_PolyCol2      -> 275707
   AbelInv_RevPolyDiag   -> 295552
   AbelInv_PolyDiag      -> 295623
   AbelInv_PolyCol3      -> 355501
   AbelInv_NegHalf       -> 356819
   AbelInv_RevPolyCol3   -> 356827
   AbelInv_RevAntiDSum   -> 360782
   AbelInv_AntiDSum      -> 360814
   AbelInv_CentralE      -> 367271
   AbelInv_BinConv       -> 367272
   AbelInv_InvBinConv    -> 367273
   AbelInv_RevColMiddle  -> 367274
Hits: 41, Misses: 27, Doubles: 6, Distinct: 35
"""