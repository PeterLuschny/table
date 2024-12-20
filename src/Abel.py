from functools import cache
from Binomial import binomial
from _tabltypes import Table


"""Abel polynomials (unsigned coefficients).
[0] [1]
[1] [0,        1]
[2] [0,        2,       1]
[3] [0,        9,       6,       1]
[4] [0,       64,      48,      12,      1]
[5] [0,      625,     500,     150,     20,      1]
[6] [0,     7776,    6480,    2160,    360,     30,    1]
[7] [0,   117649,  100842,   36015,   6860,    735,   42,   1]
[8] [0,  2097152, 1835008,  688128, 143360,  17920, 1344,  56, 1]
"""


@cache
def abel(n: int) -> list[int]:
    if n == 0:
        return [1]

    b = binomial(n - 1)
    return [b[k - 1] * n ** (n - k) if k > 0 else 0 for k in range(n + 1)]


Abel = Table(
    abel, 
    "Abel", 
    ["A137452", "A061356", "A139526"], 
    "A059297",
    r"is(k = 0)\ ? \ 0^n : \binom{n-1}{k-1} (-n)^{n - k}" 
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Abel)

'''
https://peterluschny.github.io/table/AbelTraits.html

   Abel_Trev          -> 0
   Abel_Tantidiag     -> 0
   Abel_Tacc          -> 0
   Abel_TablDiag2     -> 0
   Abel_TablDiag3     -> 0
   Abel_TablLcm       -> 0
   Abel_AccSum        -> 0
   Abel_AntiDSum      -> 0
   Abel_ColMiddle     -> 0
   Abel_CentralO      -> 0
   Abel_PolyRow3      -> 0
   Abel_RevToff11     -> 0
   Abel_RevTrev11     -> 0
   Abel_RevTantidiag  -> 0
   Abel_RevTacc       -> 0
   Abel_RevTalt       -> 0
   Abel_RevTder       -> 0
   Abel_RevEvenSum    -> 0
   Abel_RevOddSum     -> 0
   Abel_RevAccRevSum  -> 0
   Abel_RevAntiDSum   -> 0
   Abel_RevColMiddle  -> 0
   Abel_RevCentralO   -> 0
   Abel_RevNegHalf    -> 0
   Abel_RevTransNat1  -> 0
   Abel_RevTransSqrs  -> 0
   Abel_RevPolyDiag   -> 0
   Abel_TablCol0      -> 7
   Abel_TablDiag0     -> 12
   Abel_RevPolyRow1   -> 12
   Abel_TablGcd       -> 27
   Abel_PolyRow1      -> 27
   Abel_TablCol1      -> 169
   Abel_TablMax       -> 169
   Abel_TablSum       -> 272
   Abel_AbsSum        -> 272
   Abel_AltSum        -> 312
   Abel_TablDiag1     -> 2378
   Abel_RevPolyRow2   -> 5408
   Abel_PolyRow2      -> 5563
   Abel_PolyCol2      -> 7334
   Abel_RevPolyRow3   -> 16778
   Abel_PosHalf       -> 52750
   Abel_RevPolyCol3   -> 52752
   Abel_TablCol2      -> 53506
   Abel_TablCol3      -> 53507
   Abel_Tinv          -> 59297
   Abel_Tinv11        -> 59298
   Abel_Trevinv       -> 59299
   Abel_Trevinv11     -> 59300
   Abel_Toff11        -> 61356
   Abel_RevTransNat0  -> 65513
   Abel_NegHalf       -> 85527
   Abel_TransNat0     -> 89946
   Abel_Triangle      -> 137452
   Abel_Talt          -> 137452
   Abel_Trev11        -> 139526
   Abel_PolyDiag      -> 193678
   Abel_OddSum        -> 195136
   Abel_Tder          -> 225465
   Abel_TransSqrs     -> 225497
   Abel_EvenSum       -> 274278
   Abel_PolyCol3      -> 362354
   Abel_CentralE      -> 367254
   Abel_AccRevSum     -> 367255
   Abel_TransNat1     -> 367255
   Abel_BinConv       -> 367256
   Abel_InvBinConv    -> 367257
Hits: 41, Misses: 27, Doubles: 6
'''