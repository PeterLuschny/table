from functools import cache
from _tabltypes import Table
from Binomial import binomial

"""Inverse of the rencontres triangle. Unsigned version.

[0] [1]
[1] [0,  1]
[2] [1,  0,   1]
[3] [2,  3,   0,   1]
[4] [3,  8,   6,   0,   1]
[5] [4, 15,  20,  10,   0,   1]
[6] [5, 24,  45,  40,  15,   0,   1]
[7] [6, 35,  84, 105,  70,  21,   0,  1]
[8] [7, 48, 140, 224, 210, 112,  28,  0, 1]
[9] [8, 63, 216, 420, 504, 378, 168, 36, 0, 1]
"""


@cache
def rencontresinv(n: int) -> list[int]:
    if n == 0:
        return [1]

    return [(n - k - 1)*binomial(n)[k] for k in range(n)] + [1]


RencontresInv = Table(
    rencontresinv,
    "RencontresInv",
    ["A055137"],
    "A008290",
    r"\binom{n}{k} (n-k-1)",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(RencontresInv)


"""OEIS
    RencontresInv_Tinv          -> 0
    RencontresInv_Trev          -> 0
    RencontresInv_Trevinv       -> 0
    RencontresInv_Toff11        -> 0
    RencontresInv_Trev11        -> 0
    RencontresInv_Tinv11        -> 0
    RencontresInv_Trevinv11     -> 0
    RencontresInv_Tantidiag     -> 0
    RencontresInv_Tacc          -> 0
    RencontresInv_Tder          -> 0
    RencontresInv_TablCol3      -> 0
    RencontresInv_TablLcm       -> 0
    RencontresInv_EvenSum       -> 0
    RencontresInv_OddSum        -> 0
    RencontresInv_AccSum        -> 0
    RencontresInv_AccRevSum     -> 0
    RencontresInv_AntiDSum      -> 0
    RencontresInv_ColMiddle     -> 0
    RencontresInv_CentralE      -> 0
    RencontresInv_PosHalf       -> 0
    RencontresInv_TransNat0     -> 0
    RencontresInv_TransNat1     -> 0
    RencontresInv_TransSqrs     -> 0
    RencontresInv_BinConv       -> 0
    RencontresInv_InvBinConv    -> 0
    RencontresInv_PolyRow3      -> 0
    RencontresInv_PolyCol2      -> 0
    RencontresInv_PolyCol3      -> 0
    RencontresInv_PolyDiag      -> 0
    RencontresInv_RevToff11     -> 0
    RencontresInv_RevTrev11     -> 0
    RencontresInv_RevTantidiag  -> 0
    RencontresInv_RevTacc       -> 0
    RencontresInv_RevTalt       -> 0
    RencontresInv_RevTder       -> 0
    RencontresInv_RevEvenSum    -> 0
    RencontresInv_RevAccRevSum  -> 0
    RencontresInv_RevAntiDSum   -> 0
    RencontresInv_RevColMiddle  -> 0
    RencontresInv_RevCentralO   -> 0
    RencontresInv_RevTransNat1  -> 0
    RencontresInv_RevTransSqrs  -> 0
    RencontresInv_RevPolyRow3   -> 0
    RencontresInv_RevPolyCol3   -> 0
    RencontresInv_RevPolyDiag   -> 0
    RencontresInv_TablDiag1     -> 7
    RencontresInv_TablDiag0     -> 12
    RencontresInv_TablGcd       -> 12
    RencontresInv_RevPolyRow1   -> 12
    RencontresInv_TablCol0      -> 27
    RencontresInv_PolyRow1      -> 27
    RencontresInv_TablDiag2     -> 217
    RencontresInv_RevNegHalf    -> 325
    RencontresInv_CentralO      -> 917
    RencontresInv_RevTransNat0  -> 1815
    RencontresInv_PolyRow2      -> 2522
    RencontresInv_RevPolyRow2   -> 2522
    RencontresInv_TablCol1      -> 5563
    RencontresInv_TablCol2      -> 5564
    RencontresInv_TablDiag3     -> 7290
    RencontresInv_RevOddSum     -> 36289
    RencontresInv_TablSum       -> 48495
    RencontresInv_AbsSum        -> 48495
    RencontresInv_Triangle      -> 55137
    RencontresInv_Talt          -> 55137
    RencontresInv_AltSum        -> 55642
    RencontresInv_NegHalf       -> 86970
    RencontresInv_TablMax       -> 191522

    RencontresInv: Distinct: 17, Hits: 23, Misses: 45
"""