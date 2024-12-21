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


''' OEIS
   Power_Trevinv       -> https://oeis.org/A-999999
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
   Power_TablCol0      -> https://oeis.org/A7
   Power_TablCol1      -> https://oeis.org/A12
   Power_TablDiag0     -> https://oeis.org/A12
   Power_RevPolyRow1   -> https://oeis.org/A12
   Power_TablDiag1     -> https://oeis.org/A27
   Power_PolyRow1      -> https://oeis.org/A27
   Power_RevPolyRow2   -> https://oeis.org/A27
   Power_TablCol2      -> https://oeis.org/A79
   Power_RevCentralO   -> https://oeis.org/A169
   Power_TablCol3      -> https://oeis.org/A244
   Power_BinConv       -> https://oeis.org/A248
   Power_TablDiag2     -> https://oeis.org/A290
   Power_RevPolyRow3   -> https://oeis.org/A290
   Power_CentralE      -> https://oeis.org/A312
   Power_TablDiag3     -> https://oeis.org/A578
   Power_PolyRow2      -> https://oeis.org/A2378
   Power_TransNat0     -> https://oeis.org/A3101
   Power_TablMax       -> https://oeis.org/A3320
   Power_InvBinConv    -> https://oeis.org/A3725
   Power_Trev          -> https://oeis.org/A3992
   Power_RevTalt       -> https://oeis.org/A3992
   Power_Triangle      -> https://oeis.org/A4248
   Power_Talt          -> https://oeis.org/A4248
   Power_CentralO      -> https://oeis.org/A7778
   Power_Toff11        -> https://oeis.org/A9998
   Power_Trev11        -> https://oeis.org/A9999
   Power_TablSum       -> https://oeis.org/A26898
   Power_AbsSum        -> https://oeis.org/A26898
   Power_AltSum        -> https://oeis.org/A38125
   Power_PolyRow3      -> https://oeis.org/A45991
   Power_Tder          -> https://oeis.org/A51129
   Power_RevTransNat0  -> https://oeis.org/A62807
   Power_TransSqrs     -> https://oeis.org/A62809
   Power_RevToff11     -> https://oeis.org/A95884
   Power_AccSum        -> https://oeis.org/A101495
   Power_RevAccRevSum  -> https://oeis.org/A101495
   Power_RevTransNat1  -> https://oeis.org/A101495
   Power_AntiDSum      -> https://oeis.org/A104872
   Power_ColMiddle     -> https://oeis.org/A110132
   Power_RevColMiddle  -> https://oeis.org/A110138
   Power_TablGcd       -> https://oeis.org/A174965
   Power_RevPolyDiag   -> https://oeis.org/A349969
   Power_PosHalf       -> https://oeis.org/A349970
   Power_PolyCol2      -> https://oeis.org/A351279
   Power_PolyCol3      -> https://oeis.org/A351282
   Power_PolyDiag      -> https://oeis.org/A351340
   Power_RevAntiDSum   -> https://oeis.org/A352944
   Power_RevEvenSum    -> https://oeis.org/A353016

   Hits: 49, Distinct: 39, Misses: 20, Doubles: 10
'''
