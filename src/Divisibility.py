from functools import cache
from _tabltypes import Table

"""
The divisibility matrix, the indicator function for divisibility.

[ 0]  1
[ 1]  0  1
[ 2]  0  1  1
[ 3]  0  1  0  1
[ 4]  0  1  1  0  1
[ 5]  0  1  0  0  0  1
[ 6]  0  1  1  1  0  0  1
[ 7]  0  1  0  0  0  0  0  1
[ 8]  0  1  1  0  1  0  0  0  1
[ 9]  0  1  0  1  0  0  0  0  0  1
[10]  0  1  1  0  0  1  0  0  0  0  1
"""


@cache
def divisibility(n: int) -> list[int]:
    if n == 0:
        return [1]
    L = [0 for _ in range(n + 1)]
    L[1] = L[n] = 1
    i = 1
    div = n

    while i < div:
        div, mod = divmod(n, i)
        if mod == 0:
            L[i] = L[div] = 1
        i += 1
    return L


Divisibility = Table(
    divisibility,
    "Divisibility",
    ["A113704", "A051731"],
    "A000000",
    r"[n=0 \text{ or } k \text{ divides } n]",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Divisibility)


"""
Dict length: 69
   Divisibility_Trev          -> 0
   Divisibility_Tantidiag     -> 0
   Divisibility_Tacc          -> 0
   Divisibility_NegHalf       -> 0
   Divisibility_InvBinConv    -> 0
   Divisibility_RevToff11     -> 0
   Divisibility_RevTantidiag  -> 0
   Divisibility_RevTacc       -> 0
   Divisibility_RevTalt       -> 0
   Divisibility_RevTder       -> 0
   Divisibility_RevNegHalf    -> 0
   Divisibility_RevPolyDiag   -> 0
   Divisibility_TablSum       -> 5
   Divisibility_AbsSum        -> 5
   Divisibility_TablCol0      -> 7
   Divisibility_TablDiag1     -> 7
   Divisibility_TablDiag2     -> 7
   Divisibility_TablDiag3     -> 7
   Divisibility_CentralO      -> 7
   Divisibility_RevCentralO   -> 7
   Divisibility_Trevinv       -> 12
   Divisibility_Trevinv11     -> 12
   Divisibility_Tinvrev11     -> 12
   Divisibility_TablCol1      -> 12
   Divisibility_TablDiag0     -> 12
   Divisibility_TablLcm       -> 12
   Divisibility_TablGcd       -> 12
   Divisibility_TablMax       -> 12
   Divisibility_CentralE      -> 12
   Divisibility_RevPolyRow1   -> 12
   Divisibility_PolyRow1      -> 27
   Divisibility_RevPolyRow2   -> 27
   Divisibility_TablCol2      -> 35
   Divisibility_RevColMiddle  -> 35
   Divisibility_TransNat0     -> 203
   Divisibility_TransSqrs     -> 1157
   Divisibility_OddSum        -> 1227
   Divisibility_RevOddSum     -> 1227
   Divisibility_RevAntiDSum   -> 1227
   Divisibility_PolyRow2      -> 2378
   Divisibility_RevPolyRow3   -> 2522
   Divisibility_AccRevSum     -> 7503
   Divisibility_TransNat1     -> 7503
   Divisibility_AntiDSum      -> 32741
   Divisibility_PolyRow3      -> 34262
   Divisibility_Toff11        -> 51731
   Divisibility_PolyCol2      -> 55895
   Divisibility_BinConv       -> 56045
   Divisibility_PolyDiag      -> 66108
   Divisibility_PosHalf       -> 74854
   Divisibility_TablCol3      -> 79978
   Divisibility_AccSum        -> 81307
   Divisibility_RevAccRevSum  -> 81307
   Divisibility_RevTransNat1  -> 81307
   Divisibility_RevTransNat0  -> 94471
   Divisibility_AltSum        -> 112329
   Divisibility_Triangle      -> 113704
   Divisibility_Talt          -> 113704
   Divisibility_Trev11        -> 113998
   Divisibility_Tder          -> 127093
   Divisibility_ColMiddle     -> 128174
   Divisibility_Tinv11        -> 174852
   Divisibility_RevTrev11     -> 175992
   Divisibility_EvenSum       -> 183063
   Divisibility_RevEvenSum    -> 320111
   Divisibility_RevPolyCol3   -> 357051
   Divisibility_PolyCol3      -> 363913
   Divisibility_Tinv          -> 363914
   Divisibility_RevTransSqrs  -> 367326
Hits: 57, Misses: 12, Doubles: 23
"""