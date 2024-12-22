from functools import cache
from _tabltypes import Table

"""Leibniz's Scheme, multiplication table read by antidiagonals.

[0]  0
[1]  0   1
[2]  0   2    2
[3]  0   3    4   3
[4]  0   4    6   6    4
[5]  0   5    8   9    8    5
[6]  0   6   10  12   12   10    6
[7]  0   7   12  15   16   15   12    7
[8]  0   8   14  18   20   20   18   14   8
[9]  0   9   16  21   24   25   24   21  16  9
"""


@cache
def leibnizscheme(n: int) -> list[int]:
    if n == 0: return [0]
    L = leibnizscheme(n - 1)
    return [L[k] + k for k in range(n)] + [n]

LeibnizScheme = Table(
    leibnizscheme, 
    "LeibnizScheme", 
    ["A003991"], 
    "", 
    r"k\,(n - k + 1)"
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(LeibnizScheme)


''' OEIS
    LeibnizScheme_Tantidiag     -> 0 
    LeibnizScheme_Tacc          -> 0 
    LeibnizScheme_Tder          -> 0 
    LeibnizScheme_PolyRow3      -> 0 
    LeibnizScheme_PolyCol2      -> 0 
    LeibnizScheme_PolyCol3      -> 0 
    LeibnizScheme_PolyDiag      -> 0 
    LeibnizScheme_RevToff11     -> 0 
    LeibnizScheme_RevTrev11     -> 0 
    LeibnizScheme_RevTantidiag  -> 0 
    LeibnizScheme_RevTder       -> 0 
    LeibnizScheme_RevTransSqrs  -> 0 
    LeibnizScheme_RevPolyDiag   -> 0 
    LeibnizScheme_TablCol0      -> https://oeis.org/A7
    LeibnizScheme_InvBinConv    -> https://oeis.org/A7
    LeibnizScheme_RevPolyRow1   -> https://oeis.org/A12
    LeibnizScheme_TablCol1      -> https://oeis.org/A27
    LeibnizScheme_TablDiag0     -> https://oeis.org/A27
    LeibnizScheme_PolyRow1      -> https://oeis.org/A27
    LeibnizScheme_TablGcd       -> https://oeis.org/A34
    LeibnizScheme_RevCentralO   -> https://oeis.org/A290
    LeibnizScheme_TablSum       -> https://oeis.org/A292
    LeibnizScheme_AbsSum        -> https://oeis.org/A292
    LeibnizScheme_BinConv       -> https://oeis.org/A1788
    LeibnizScheme_CentralE      -> https://oeis.org/A2378
    LeibnizScheme_AccSum        -> https://oeis.org/A2415
    LeibnizScheme_TransNat0     -> https://oeis.org/A2415
    LeibnizScheme_RevAccRevSum  -> https://oeis.org/A2415
    LeibnizScheme_RevTransNat1  -> https://oeis.org/A2415
    LeibnizScheme_TablMax       -> https://oeis.org/A2620
    LeibnizScheme_RevColMiddle  -> https://oeis.org/A2620
    LeibnizScheme_Toff11        -> https://oeis.org/A3991
    LeibnizScheme_Trev11        -> https://oeis.org/A3991
    LeibnizScheme_CentralO      -> https://oeis.org/A5563
    LeibnizScheme_TablCol2      -> https://oeis.org/A5843
    LeibnizScheme_TablDiag1     -> https://oeis.org/A5843
    LeibnizScheme_RevPolyRow2   -> https://oeis.org/A5843
    LeibnizScheme_OddSum        -> https://oeis.org/A5993
    LeibnizScheme_RevEvenSum    -> https://oeis.org/A5993
    LeibnizScheme_EvenSum       -> https://oeis.org/A6584
    LeibnizScheme_RevOddSum     -> https://oeis.org/A6584
    LeibnizScheme_AntiDSum      -> https://oeis.org/A6918
    LeibnizScheme_RevAntiDSum   -> https://oeis.org/A6918
    LeibnizScheme_TablCol3      -> https://oeis.org/A8585
    LeibnizScheme_TablDiag2     -> https://oeis.org/A8585
    LeibnizScheme_TablDiag3     -> https://oeis.org/A8586
    LeibnizScheme_TransSqrs     -> https://oeis.org/A24166
    LeibnizScheme_AccRevSum     -> https://oeis.org/A34827
    LeibnizScheme_TransNat1     -> https://oeis.org/A34827
    LeibnizScheme_RevTransNat0  -> https://oeis.org/A34827
    LeibnizScheme_ColMiddle     -> https://oeis.org/A35106
    LeibnizScheme_PosHalf       -> https://oeis.org/A45618
    LeibnizScheme_PolyRow2      -> https://oeis.org/A46092
    LeibnizScheme_NegHalf       -> https://oeis.org/A73371
    LeibnizScheme_Triangle      -> https://oeis.org/A94053
    LeibnizScheme_Trev          -> https://oeis.org/A94053
    LeibnizScheme_Talt          -> https://oeis.org/A94053
    LeibnizScheme_RevTalt       -> https://oeis.org/A94053
    LeibnizScheme_RevNegHalf    -> https://oeis.org/A95977
    LeibnizScheme_RevTacc       -> https://oeis.org/A140765
    LeibnizScheme_AltSum        -> https://oeis.org/A142150
    LeibnizScheme_TablLcm       -> https://oeis.org/A169900
    LeibnizScheme_RevPolyCol3   -> https://oeis.org/A212337
    LeibnizScheme_RevPolyRow3   -> https://oeis.org/A271740

    LeibnizScheme   , Distinct: 32, Hits: 51, Misses: 13
'''
