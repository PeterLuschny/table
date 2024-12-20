from functools import cache
from _tabltypes import Table

"""Inverse Catalan triangle. Unsigned version.

   0:   1
   1:   0    1
   2:   0    2    1
   3:   0    3    4    1
   4:   0    4   10    6    1
   5:   0    5   20   21    8    1
   6:   0    6   35   56   36   10    1
   7:   0    7   56  126  120   55   12    1
   8:   0    8   84  252  330  220   78   14    1
   9:   0    9  120  462  792  715  364  105   16    1
  10:   0   10  165  792 1716 2002 1365  560  136   18    1
"""

@cache
def catalaninv(n: int) -> list[int]:
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]

    row = [0]*(n+1)
    c0 = catalaninv(n-2) + [0, 0]
    c1 = catalaninv(n-1) + [0]
    for k in range(1, n+1):
        row[k] = c1[k-1] + 2*c1[k] - c0[k]
    return row


CatalanInv = Table(
    catalaninv,    # the generating function
    "CatalanInv",  # name of the table
    ["A128908", "A053122", "A285072"],   # similar sequences in OEIS
    "A128899",     # id of inverse sequence
    r"T(n,k)=0"    # TeX of defining formula
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(CatalanInv)
 
"""
   Dict length: 68
   CatalanInv_Trev          -> 0
   CatalanInv_Trevinv       -> 0
   CatalanInv_Tantidiag     -> 0
   CatalanInv_Tacc          -> 0
   CatalanInv_Tder          -> 0
   CatalanInv_TablMax       -> 0
   CatalanInv_ColMiddle     -> 0
   CatalanInv_CentralO      -> 0
   CatalanInv_TransSqrs     -> 0
   CatalanInv_PolyDiag      -> 0
   CatalanInv_RevToff11     -> 0
   CatalanInv_RevTrev11     -> 0
   CatalanInv_RevTantidiag  -> 0
   CatalanInv_RevTacc       -> 0
   CatalanInv_RevTalt       -> 0
   CatalanInv_RevTder       -> 0
   CatalanInv_RevOddSum     -> 0
   CatalanInv_RevColMiddle  -> 0
   CatalanInv_RevTransSqrs  -> 0
   CatalanInv_RevPolyDiag   -> 0
   CatalanInv_TablCol0      -> 7
   CatalanInv_TablDiag0     -> 12
   CatalanInv_RevPolyRow1   -> 12
   CatalanInv_TablCol1      -> 27
   CatalanInv_PolyRow1      -> 27
   CatalanInv_AntiDSum      -> 79
   CatalanInv_TablCol2      -> 292
   CatalanInv_TablCol3      -> 389
   CatalanInv_RevPolyRow3   -> 567
   CatalanInv_TablSum       -> 1906
   CatalanInv_AbsSum        -> 1906
   CatalanInv_PosHalf       -> 2450
   CatalanInv_TablDiag3     -> 2492
   CatalanInv_RevPolyRow2   -> 5408
   CatalanInv_PolyRow2      -> 5563
   CatalanInv_TablDiag1     -> 5843
   CatalanInv_RevNegHalf    -> 10673
   CatalanInv_AltSum        -> 11655
   CatalanInv_TablDiag2     -> 14105
   CatalanInv_TransNat0     -> 30267
   CatalanInv_Tinv11        -> 39598
   CatalanInv_RevCentralO   -> 45721
   CatalanInv_NegHalf       -> 49072
   CatalanInv_Trevinv11     -> 50166
   CatalanInv_PolyCol2      -> 52530
   CatalanInv_Toff11        -> 78812
   CatalanInv_RevPolyCol3   -> 99459
   CatalanInv_TablLcm       -> 99996
   CatalanInv_OddSum        -> 113066
   CatalanInv_Tinv          -> 128899
   CatalanInv_Triangle      -> 128908
   CatalanInv_Talt          -> 128908
   CatalanInv_RevAntiDSum   -> 158943
   CatalanInv_CentralE      -> 165817
   CatalanInv_Trev11        -> 172431
   CatalanInv_BinConv       -> 262440
   CatalanInv_RevTransNat0  -> 281199
   CatalanInv_EvenSum       -> 290890
   CatalanInv_PolyCol3      -> 290902
   CatalanInv_AccRevSum     -> 290917
   CatalanInv_TransNat1     -> 290917
   CatalanInv_PolyRow3      -> 317637
   CatalanInv_TablGcd       -> 318829
   CatalanInv_InvBinConv    -> 350290
   CatalanInv_RevEvenSum    -> 376716
   CatalanInv_AccSum        -> 377866
   CatalanInv_RevAccRevSum  -> 377866
   CatalanInv_RevTransNat1  -> 377866
Hits: 48, Misses: 20, Doubles: 7, Distinct: 41
"""