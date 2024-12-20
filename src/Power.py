from functools import cache
from _tabltypes import Table

"""Powers.

[0]  [1]
[1]  [0, 1]
[2]  [0, 1,   1]
[3]  [0, 1,   2,   1]
[4]  [0, 1,   4,   3,    1]
[5]  [0, 1,   8,   9,    4,   1]
[6]  [0, 1,  16,  27,   16,   5,   1]
[7]  [0, 1,  32,  81,   64,  25,   6,  1]
[8]  [0, 1,  64, 243,  256, 125,  36,  7, 1]
[9]  [0, 1, 128, 729, 1024, 625, 216, 49, 8, 1]

"""

@cache
def power(n: int) -> list[int]:
    if n == 0:
        return [1]

    lrow = power(n - 1)
    return [k * lrow[k] for k in range(n)] + [1]


Power = Table(
    power,        # the generating function
    "Power",      # name of the table
    ["A004248", "A009998", "A051129"], # similar sequences in OEIS
    "A000000",    # inverse triangle exists, but not in OEIS
    r"k^{n - k}"  # TeX of defining formula
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Power)


"""
   Power_Trevinv       -> -999999
   Power_Tinv          -> 0
   Power_Tinv11        -> 0
   Power_Trevinv11     -> 0
   Power_Tinvrev11     -> 0
   Power_Tantidiag     -> 0
   Power_Tacc          -> 0
   Power_TablLcm       -> 0
   Power_EvenSum       -> 0
   Power_OddSum        -> 0
   Power_AccRevSum     -> 0
   Power_NegHalf       -> 0
   Power_TransNat1     -> 0
   Power_RevTrev11     -> 0
   Power_RevTantidiag  -> 0
   Power_RevTacc       -> 0
   Power_RevTder       -> 0
   Power_RevOddSum     -> 0
   Power_RevNegHalf    -> 0
   Power_RevTransSqrs  -> 0
   Power_RevPolyCol3   -> 0
   Power_TablCol0      -> 7
   Power_TablCol1      -> 12
   Power_TablDiag0     -> 12
   Power_RevPolyRow1   -> 12
   Power_TablDiag1     -> 27
   Power_PolyRow1      -> 27
   Power_RevPolyRow2   -> 27
   Power_TablCol2      -> 79
   Power_RevCentralO   -> 169
   Power_TablCol3      -> 244
   Power_BinConv       -> 248
   Power_TablDiag2     -> 290
   Power_RevPolyRow3   -> 290
   Power_CentralE      -> 312
   Power_TablDiag3     -> 578
   Power_PolyRow2      -> 2378
   Power_TransNat0     -> 3101
   Power_TablMax       -> 3320
   Power_InvBinConv    -> 3725
   Power_Trev          -> 3992
   Power_RevTalt       -> 3992
   Power_Triangle      -> 4248
   Power_Talt          -> 4248
   Power_CentralO      -> 7778
   Power_Toff11        -> 9998
   Power_Trev11        -> 9999
   Power_TablSum       -> 26898
   Power_AbsSum        -> 26898
   Power_AltSum        -> 38125
   Power_PolyRow3      -> 45991
   Power_Tder          -> 51129
   Power_RevTransNat0  -> 62807
   Power_TransSqrs     -> 62809
   Power_RevToff11     -> 95884
   Power_AccSum        -> 101495
   Power_RevAccRevSum  -> 101495
   Power_RevTransNat1  -> 101495
   Power_AntiDSum      -> 104872
   Power_ColMiddle     -> 110132
   Power_RevColMiddle  -> 110138
   Power_TablGcd       -> 174965
   Power_RevPolyDiag   -> 349969
   Power_PosHalf       -> 349970
   Power_PolyCol2      -> 351279
   Power_PolyCol3      -> 351282
   Power_PolyDiag      -> 351340
   Power_RevAntiDSum   -> 352944
   Power_RevEvenSum    -> 353016
Hits: 49, Misses: 20, Doubles: 10
"""