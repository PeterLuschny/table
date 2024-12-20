from functools import cache
from _tabltypes import Table

"""
Inverse of Bessel, unsigned version.

[0]  [1]
[1]  [0, 1]
[2]  [0, 1, 1]
[3]  [0, 0, 3,  1]
[4]  [0, 0, 3,  6,   1]
[5]  [0, 0, 0, 15,  10,   1]
[6]  [0, 0, 0, 15,  45,  15,    1]
[7]  [0, 0, 0,  0, 105, 105,   21,   1]
[8]  [0, 0, 0,  0, 105, 420,  210,  28,  1]
[9]  [0, 0, 0,  0,   0, 945, 1260, 378, 36, 1]
"""

@cache
def besselinv(n: int) -> list[int]:
    if n == 0:
        return [1]

    b = besselinv(n - 1)
    return [0] + [(2*k - n + 1)*b[k] + 
            b[k-1] for k in range(1, n)] + [1]


BesselInv = Table(
    besselinv,    # the generating function
    "BesselInv",  # name of the table
    ["A122848", "A104556", "A096713"],  # similar sequences in OEIS
    "A132062",    # id of inverse sequence
    r"T(n,k)"     # TeX of defining formula
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(BesselInv)
    
"""
   Dict length: 68
   BesselInv_Tantidiag     -> 0
   BesselInv_Tacc          -> 0
   BesselInv_Tder          -> 0
   BesselInv_TablCol3      -> 0
   BesselInv_TablLcm       -> 0
   BesselInv_TablMax       -> 0
   BesselInv_OddSum        -> 0
   BesselInv_AccSum        -> 0
   BesselInv_TransSqrs     -> 0
   BesselInv_BinConv       -> 0
   BesselInv_InvBinConv    -> 0
   BesselInv_PolyDiag      -> 0
   BesselInv_RevToff11     -> 0
   BesselInv_RevTrev11     -> 0
   BesselInv_RevTantidiag  -> 0
   BesselInv_RevTacc       -> 0
   BesselInv_RevTder       -> 0
   BesselInv_RevAccRevSum  -> 0
   BesselInv_RevAntiDSum   -> 0
   BesselInv_RevTransNat1  -> 0
   BesselInv_TablCol0      -> 7
   BesselInv_TablCol1      -> 7
   BesselInv_TablCol2      -> 7
   BesselInv_CentralO      -> 7
   BesselInv_TablDiag0     -> 12
   BesselInv_RevPolyRow1   -> 12
   BesselInv_PolyRow1      -> 27
   BesselInv_RevPolyRow2   -> 27
   BesselInv_TablSum       -> 85
   BesselInv_AbsSum        -> 85
   BesselInv_TablDiag1     -> 217
   BesselInv_RevEvenSum    -> 704
   BesselInv_PolyCol2      -> 898
   BesselInv_CentralE      -> 1147
   BesselInv_RevCentralO   -> 1147
   BesselInv_AltSum        -> 1464
   BesselInv_RevOddSum     -> 1465
   BesselInv_AccRevSum     -> 1475
   BesselInv_TransNat1     -> 1475
   BesselInv_Tinv11        -> 1497
   BesselInv_Trevinv11     -> 1498
   BesselInv_PolyRow2      -> 2378
   BesselInv_RevPolyRow3   -> 16777
   BesselInv_PosHalf       -> 47974
   BesselInv_Toff11        -> 49403
   BesselInv_TablDiag2     -> 50534
   BesselInv_RevNegHalf    -> 62267
   BesselInv_TablGcd       -> 69834
   BesselInv_EvenSum       -> 85386
   BesselInv_Trevinv       -> 104548
   BesselInv_Trev11        -> 111924
   BesselInv_RevPolyCol3   -> 115327
   BesselInv_Triangle      -> 122848
   BesselInv_Talt          -> 122848
   BesselInv_AntiDSum      -> 122849
   BesselInv_ColMiddle     -> 123023
   BesselInv_Tinv          -> 132062
   BesselInv_RevColMiddle  -> 133221
   BesselInv_Trev          -> 144299
   BesselInv_RevTalt       -> 144299
   BesselInv_RevTransNat0  -> 162970
   BesselInv_RevTransSqrs  -> 174764
   BesselInv_TransNat0     -> 189940
   BesselInv_TablDiag3     -> 240440
   BesselInv_RevPolyDiag   -> 277614
   BesselInv_NegHalf       -> 293604
   BesselInv_PolyCol3      -> 335819
   BesselInv_PolyRow3      -> 366151
Hits: 48, Misses: 20, Doubles: 10, Distinct: 38
"""
