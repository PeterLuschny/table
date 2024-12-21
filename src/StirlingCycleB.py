from functools import cache
from _tabltypes import Table

"""Stirling cycle B-type.

[0]      1;
[1]      1,      1;
[2]      3,      4,      1;
[3]     15,     23,      9,     1;
[4]    105,    176,     86,    16,     1;
[5]    945,   1689,    950,   230,    25,   1;
[6]  10395,  19524,  12139,  3480,   505,  36,  1;
[7] 135135, 264207, 177331, 57379, 10045, 973, 49, 1;
"""


@cache
def stirlingcycleb(n: int) -> list[int]:
    if n == 0:
        return [1]

    row = stirlingcycleb(n - 1) + [1]

    m = 2 * n - 1
    for k in range(n - 1, 0, -1):
        row[k] = m * row[k] + row[k - 1]
    row[0] *= m

    return row


StirlingCycleB = Table(
    stirlingcycleb,
    "StirlingCycleB",
    ["A028338", "A039757", "A039758", "A109692"],
    "A000000",
    r"\sum_{i=k}^{n} (-2)^{n-i} \binom{i}{k} {n \brack i}",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(StirlingCycleB)


''' OEIS
   StirlingCycB_Toff11        -> 0 
   StirlingCycB_Trev11        -> 0 
   StirlingCycB_Tinv11        -> 0 
   StirlingCycB_Trevinv11     -> 0 
   StirlingCycB_Tantidiag     -> 0 
   StirlingCycB_Tacc          -> 0 
   StirlingCycB_Tder          -> 0 
   StirlingCycB_TablLcm       -> 0 
   StirlingCycB_AccSum        -> 0 
   StirlingCycB_AccRevSum     -> 0 
   StirlingCycB_AntiDSum      -> 0 
   StirlingCycB_ColMiddle     -> 0 
   StirlingCycB_CentralO      -> 0 
   StirlingCycB_TransNat1     -> 0 
   StirlingCycB_TransSqrs     -> 0 
   StirlingCycB_BinConv       -> 0 
   StirlingCycB_InvBinConv    -> 0 
   StirlingCycB_RevToff11     -> 0 
   StirlingCycB_RevTrev11     -> 0 
   StirlingCycB_RevTantidiag  -> 0 
   StirlingCycB_RevTacc       -> 0 
   StirlingCycB_RevTder       -> 0 
   StirlingCycB_RevAccRevSum  -> 0 
   StirlingCycB_RevColMiddle  -> 0 
   StirlingCycB_RevCentralO   -> 0 
   StirlingCycB_RevTransNat1  -> 0 
   StirlingCycB_RevTransSqrs  -> 0 
   StirlingCycB_RevPolyRow3   -> 0 
   StirlingCycB_RevPolyDiag   -> 0 
   StirlingCycB_AltSum        -> https://oeis.org/A7
   StirlingCycB_TablDiag0     -> https://oeis.org/A12
   StirlingCycB_TablGcd       -> https://oeis.org/A12
   StirlingCycB_PolyRow1      -> https://oeis.org/A27
   StirlingCycB_RevPolyRow1   -> https://oeis.org/A27
   StirlingCycB_TablSum       -> https://oeis.org/A165
   StirlingCycB_AbsSum        -> https://oeis.org/A165
   StirlingCycB_TablDiag1     -> https://oeis.org/A290
   StirlingCycB_RevPolyRow2   -> https://oeis.org/A567
   StirlingCycB_TablCol0      -> https://oeis.org/A1147
   StirlingCycB_PolyCol2      -> https://oeis.org/A1147
   StirlingCycB_RevNegHalf    -> https://oeis.org/A1147
   StirlingCycB_EvenSum       -> https://oeis.org/A2866
   StirlingCycB_OddSum        -> https://oeis.org/A2866
   StirlingCycB_PolyCol3      -> https://oeis.org/A2866
   StirlingCycB_RevEvenSum    -> https://oeis.org/A2866
   StirlingCycB_RevOddSum     -> https://oeis.org/A2866
   StirlingCycB_TablCol1      -> https://oeis.org/A4041
   StirlingCycB_TablMax       -> https://oeis.org/A4041
   StirlingCycB_PolyRow2      -> https://oeis.org/A5563
   StirlingCycB_NegHalf       -> https://oeis.org/A7696
   StirlingCycB_PosHalf       -> https://oeis.org/A8545
   StirlingCycB_TablDiag2     -> https://oeis.org/A24196
   StirlingCycB_TablDiag3     -> https://oeis.org/A24197
   StirlingCycB_Triangle      -> https://oeis.org/A28338
   StirlingCycB_Talt          -> https://oeis.org/A28338
   StirlingCycB_TablCol2      -> https://oeis.org/A28339
   StirlingCycB_TablCol3      -> https://oeis.org/A28340
   StirlingCycB_Tinv          -> https://oeis.org/A39755
   StirlingCycB_Trevinv       -> https://oeis.org/A39756
   StirlingCycB_RevPolyCol3   -> https://oeis.org/A49308
   StirlingCycB_Trev          -> https://oeis.org/A109692
   StirlingCycB_RevTalt       -> https://oeis.org/A109692
   StirlingCycB_RevTransNat0  -> https://oeis.org/A197130
   StirlingCycB_RevAntiDSum   -> https://oeis.org/A202153
   StirlingCycB_TransNat0     -> https://oeis.org/A203159
   StirlingCycB_CentralE      -> https://oeis.org/A293318
   StirlingCycB_PolyRow3      -> https://oeis.org/A370912
   StirlingCycB_PolyDiag      -> https://oeis.org/A374866

   Hits: 39, Distinct: 27, Misses: 29, Doubles: 12
'''
