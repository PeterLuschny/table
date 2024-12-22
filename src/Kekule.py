from functools import cache
from DistLattices import dist_latt
from _tabltypes import Table

"""Kekule triangle.

  [0] 1;
  [1] 1,  1;
  [2] 1,  2,  1;
  [3] 1,  3,  3,  1;
  [4] 1,  5,  6,  4,  1;
  [5] 1,  8, 14, 10,  5,  1;
  [6] 1, 13, 31, 30, 15,  6, 1;
  [7] 1, 21, 70, 85, 55, 21, 7, 1;

  # A050446
  [1, 1, 1, 1, 1, 1, 1, 1, 1]
  [1, 2, 3, 4, 5, 6, 7, 8, 9]
  [1, 3, 6, 10, 15, 21, 28, 36, 45]
  [1, 5, 14, 30, 55, 91, 140, 204, 285]
  [1, 8, 31, 85, 190, 371, 658, 1086, 1695]
  [1, 13, 70, 246, 671, 1547, 3164, 5916, 10317]
  [1, 21, 157, 707, 2353, 6405, 15106, 31998, 62349]
  [1, 34, 353, 2037, 8272, 26585, 72302, 173502, 377739]
  [1, 55, 793, 5864, 29056, 110254, 345775, 940005, 2286648]
  [1, 89, 1782, 16886, 102091, 457379, 1654092, 5094220, 13846117]
"""

@cache
def kekule(n: int) -> list[int]:
    return [dist_latt(n - k, k) for k in range(n + 1)]


Kekule = Table(
    kekule, 
    "Kekule", 
    ["A050446", "A050447"], 
    "A000000", 
    r"%%"
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Kekule)


''' OEIS
    Kekule_Tinv          -> 0 
    Kekule_Trevinv       -> 0 
    Kekule_Tinvrev       -> 0 
    Kekule_Toff11        -> 0 
    Kekule_Trev11        -> 0 
    Kekule_Tinv11        -> 0 
    Kekule_Trevinv11     -> 0 
    Kekule_Tantidiag     -> 0 
    Kekule_Tacc          -> 0 
    Kekule_Tder          -> 0 
    Kekule_TablLcm       -> 0 
    Kekule_TablMax       -> 0 
    Kekule_EvenSum       -> 0 
    Kekule_OddSum        -> 0 
    Kekule_AltSum        -> 0 
    Kekule_AccSum        -> 0 
    Kekule_AccRevSum     -> 0 
    Kekule_AntiDSum      -> 0 
    Kekule_ColMiddle     -> 0 
    Kekule_PosHalf       -> 0 
    Kekule_NegHalf       -> 0 
    Kekule_TransNat0     -> 0 
    Kekule_TransNat1     -> 0 
    Kekule_TransSqrs     -> 0 
    Kekule_BinConv       -> 0 
    Kekule_InvBinConv    -> 0 
    Kekule_PolyCol2      -> 0 
    Kekule_PolyCol3      -> 0 
    Kekule_PolyDiag      -> 0 
    Kekule_RevToff11     -> 0 
    Kekule_RevTrev11     -> 0 
    Kekule_RevTinv11     -> 0 
    Kekule_RevTrevinv11  -> 0 
    Kekule_RevTantidiag  -> 0 
    Kekule_RevTacc       -> 0 
    Kekule_RevTder       -> 0 
    Kekule_RevEvenSum    -> 0 
    Kekule_RevOddSum     -> 0 
    Kekule_RevAccRevSum  -> 0 
    Kekule_RevAntiDSum   -> 0 
    Kekule_RevColMiddle  -> 0 
    Kekule_RevCentralO   -> 0 
    Kekule_RevNegHalf    -> 0 
    Kekule_RevTransNat0  -> 0 
    Kekule_RevTransNat1  -> 0 
    Kekule_RevTransSqrs  -> 0 
    Kekule_RevPolyCol3   -> 0 
    Kekule_RevPolyDiag   -> 0 
    Kekule_TablCol0      -> https://oeis.org/A12
    Kekule_TablDiag0     -> https://oeis.org/A12
    Kekule_TablDiag1     -> https://oeis.org/A27
    Kekule_PolyRow1      -> https://oeis.org/A27
    Kekule_RevPolyRow1   -> https://oeis.org/A27
    Kekule_TablCol1      -> https://oeis.org/A45
    Kekule_TablDiag2     -> https://oeis.org/A217
    Kekule_PolyRow2      -> https://oeis.org/A290
    Kekule_RevPolyRow2   -> https://oeis.org/A290
    Kekule_TablDiag3     -> https://oeis.org/A330
    Kekule_PolyRow3      -> https://oeis.org/A578
    Kekule_RevPolyRow3   -> https://oeis.org/A578
    Kekule_TablCol2      -> https://oeis.org/A6356
    Kekule_TablCol3      -> https://oeis.org/A6357
    Kekule_Triangle      -> https://oeis.org/A50446
    Kekule_Talt          -> https://oeis.org/A50446
    Kekule_Trev          -> https://oeis.org/A50447
    Kekule_RevTalt       -> https://oeis.org/A50447
    Kekule_TablGcd       -> https://oeis.org/A99563
    Kekule_CentralO      -> https://oeis.org/A276313
    Kekule_TablSum       -> https://oeis.org/A373353
    Kekule_AbsSum        -> https://oeis.org/A373353
    Kekule_CentralE      -> https://oeis.org/A373659

    Kekule          , Distinct: 16, Hits: 23, Misses: 48
'''
