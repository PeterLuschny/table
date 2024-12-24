from functools import cache
from _tabltypes import Table

"""To call this triangle 'LucasInv' is a (slight) misnomer. 
This is an integer version of the matrix inverse of the Lucas
triangle. T(n, k) = -LucasInv(n, k)*(-2)^(n-k+1). 

  [0]  1;
  [1]  1,   1;
  [2]  1,   3,    1;
  [3]  1,   7,    5,    1;
  [4]  1,  15,   17,    7,    1;
  [5]  1,  31,   49,   31,    9,    1;
  [6]  1,  63,  129,  111,   49,   11,   1;
  [7]  1, 127,  321,  351,  209,   71,  13,   1;
  [8]  1, 255,  769, 1023,  769,  351,  97,  15,   1;
  [9]  1, 511, 1793, 2815, 2561, 1471, 545, 127,  17,  1;
"""


@cache
def lucasinv(n: int) -> list[int]:
    if n == 0: return [1]

    r = [1] + lucasinv(n - 1) 
    for k in range(1, n): 
        r[k] += 2*r[k + 1]
    return  r


LucasInv = Table(
    lucasinv, 
    "LucasInv", 
    ["A112857"], 
    "A029635", 
    r"\sum_{j=k^n} \binom{n}{j} \binom{j-1}{k-1}"
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(LucasInv)


""" OEIS
Dict length: 71
    LucasInv_Tinvrev       -> 0
    LucasInv_Tinv11        -> 0
    LucasInv_Trevinv11     -> 0
    LucasInv_Tacc          -> 0
    LucasInv_Tder          -> 0
    LucasInv_TablLcm       -> 0
    LucasInv_TablMax       -> 0
    LucasInv_AccSum        -> 0
    LucasInv_AccRevSum     -> 0
    LucasInv_ColMiddle     -> 0
    LucasInv_TransNat0     -> 0
    LucasInv_TransNat1     -> 0
    LucasInv_InvBinConv    -> 0
    LucasInv_RevTinv11     -> 0
    LucasInv_RevTrevinv11  -> 0
    LucasInv_RevTantidiag  -> 0
    LucasInv_RevTacc       -> 0
    LucasInv_RevTder       -> 0
    LucasInv_RevEvenSum    -> 0
    LucasInv_RevOddSum     -> 0
    LucasInv_RevAccRevSum  -> 0
    LucasInv_RevAntiDSum   -> 0
    LucasInv_RevColMiddle  -> 0
    LucasInv_RevTransNat0  -> 0
    LucasInv_RevTransNat1  -> 0
    LucasInv_RevTransSqrs  -> 0
    LucasInv_RevPolyRow3   -> 0
    LucasInv_RevPolyCol3   -> 0
    LucasInv_RevPolyDiag   -> 0
    LucasInv_TablCol0      -> 12
    LucasInv_TablDiag0     -> 12
                           -> 83065
    LucasInv_PolyDiag      -> 83069
    LucasInv_PolyRow3      -> 83074
    LucasInv_EvenSum       -> 111277
    LucasInv_Triangle      -> 112857
    LucasInv_Talt          -> 112857
    LucasInv_Trev          -> 119258
    LucasInv_RevTalt       -> 119258
    LucasInv_CentralE      -> 119259
    LucasInv_RevCentralO   -> 178792
    LucasInv_Trev11        -> 193844
    LucasInv_RevToff11     -> 193844
    LucasInv_Toff11        -> 193845
    LucasInv_RevTrev11     -> 193845
    LucasInv_TablDiag3     -> 199899
    LucasInv_Tinv          -> 200139
    LucasInv_CentralO      -> 240721
    LucasInv_PosHalf       -> 247313
    LucasInv_Tantidiag     -> 257597

    LucasInv: Distinct: 31, Hits: 42, Misses: 29
"""