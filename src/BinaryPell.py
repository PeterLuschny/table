from functools import cache
from _tabltypes import Table

"""Binary Pell triangle

[0] [  1]
[1] [  2,    1]
[2] [  4,    4,    1]
[3] [  8,   12,    6,    1]
[4] [ 16,   32,   24,    8,    1]
[5] [ 32,   80,   80,   40,   10,   1]
[6] [ 64,  192,  240,  160,   60,  12,   1]
[7] [128,  448,  672,  560,  280,  84,  14,  1]
[8] [256, 1024, 1792, 1792, 1120, 448, 112, 16, 1]
"""


@cache
def binarypell(n: int) -> list[int]:

    if n == 0:
        return [1]

    arow = binarypell(n-1)
    row = arow + [1]
    for k in range(n-1, 0, -1):
        row[k] = arow[k - 1] + 2 * arow[k]
    row[0] = 2 * arow[0]
    return row


BinaryPell = Table(
    binarypell,
    "BinaryPell",
    ["A038207"],
    "A000000",
    r"\binom{n}{k} \, 2^{n-k}"
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(BinaryPell)

'''
Dict length: 68
   BinaryPell_Toff11        -> 0
   BinaryPell_Trev11        -> 0
   BinaryPell_Tinv11        -> 0
   BinaryPell_Trevinv11     -> 0
   BinaryPell_Tacc          -> 0
   BinaryPell_Tder          -> 0
   BinaryPell_TablLcm       -> 0
   BinaryPell_ColMiddle     -> 0
   BinaryPell_TransSqrs     -> 0
   BinaryPell_InvBinConv    -> 0
   BinaryPell_RevTrev11     -> 0
   BinaryPell_RevTacc       -> 0
   BinaryPell_RevTder       -> 0
   BinaryPell_RevNegHalf    -> 7
   BinaryPell_TablDiag0     -> 12
   BinaryPell_AltSum        -> 12
   BinaryPell_PolyRow1      -> 27
   BinaryPell_TablCol0      -> 79
   BinaryPell_AntiDSum      -> 129
   BinaryPell_TablSum       -> 244
   BinaryPell_AbsSum        -> 244
   BinaryPell_NegHalf       -> 244
   BinaryPell_PolyDiag      -> 272
   BinaryPell_PolyRow2      -> 290
   BinaryPell_PolyCol2      -> 302
   BinaryPell_PosHalf       -> 351
   BinaryPell_PolyCol3      -> 351
   BinaryPell_RevPolyCol3   -> 420
   BinaryPell_PolyRow3      -> 578
   BinaryPell_RevAntiDSum   -> 1045
   BinaryPell_TablCol1      -> 1787
   BinaryPell_TablCol2      -> 1788
   BinaryPell_TablCol3      -> 1789
   BinaryPell_BinConv       -> 1850
   BinaryPell_OddSum        -> 3462
   BinaryPell_RevPolyRow1   -> 5408
   BinaryPell_TablDiag1     -> 5843
   BinaryPell_AccRevSum     -> 6234
   BinaryPell_TransNat1     -> 6234
   BinaryPell_EvenSum       -> 7051
   BinaryPell_Trev          -> 13609
   BinaryPell_Trevinv       -> 13609
   BinaryPell_RevTalt       -> 13609
   BinaryPell_RevPolyRow2   -> 16754
   BinaryPell_RevPolyRow3   -> 16755
   BinaryPell_TransNat0     -> 27471
   BinaryPell_Triangle      -> 38207
   BinaryPell_Tinv          -> 38207
   BinaryPell_Talt          -> 38207
   BinaryPell_TablDiag2     -> 46092
   BinaryPell_RevEvenSum    -> 46717
   BinaryPell_CentralE      -> 59304
   BinaryPell_RevTransSqrs  -> 62189
   BinaryPell_RevCentralO   -> 69720
   BinaryPell_CentralO      -> 69723
   BinaryPell_AccSum        -> 81038
   BinaryPell_RevAccRevSum  -> 81038
   BinaryPell_RevTransNat1  -> 81038
   BinaryPell_RevPolyDiag   -> 85527
   BinaryPell_RevColMiddle  -> 98660
   BinaryPell_TablMax       -> 109388
   BinaryPell_RevTantidiag  -> 128099
   BinaryPell_TablDiag3     -> 130809
   BinaryPell_RevOddSum     -> 152011
   BinaryPell_TablGcd       -> 171977
   BinaryPell_Tantidiag     -> 207538
   BinaryPell_RevTransNat0  -> 212697
   BinaryPell_RevToff11     -> 276985
Hits: 55, Misses: 13, Doubles: 11, Distinct: 44
'''
