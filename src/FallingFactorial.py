from functools import cache
from _tabltypes import Table

"""Falling factorial, number of permutations of n things k at a time.

[0]  1
[1]  1,  1
[2]  1,  2,  2
[3]  1,  3,  6,   6
[4]  1,  4, 12,  24,   24
[5]  1,  5, 20,  60,  120,  120
[6]  1,  6, 30, 120,  360,  720,     720
[7]  1,  7, 42, 210,  840,  2520,   5040,   5040;
[8]  1,  8, 56, 336, 1680,  6720,  20160,  40320,   40320;
[9]  1,  9, 72, 504, 3024, 15120,  60480, 181440,  362880,  362880;
"""


@cache
def fallingfactorial(n: int) -> list[int]:
    if n == 0:
        return [1]

    r = fallingfactorial(n - 1)
    row = [n * r[k] for k in range(-1, n)]
    row[0] = 1
    return row


FallingFactorial = Table(
    fallingfactorial,
    "FallingFactorial",
    ["A008279", "A068424", "A094587", "A173333", "A181511"],
    "",
    r"n! / (n - k)!",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(FallingFactorial)


''' OEIS
   FallingFact_Trev11        -> 0 
   FallingFact_Tder          -> 0 
   FallingFact_PolyRow3      -> 0 
   FallingFact_RevTinv11     -> 0 
   FallingFact_RevTrevinv11  -> 0 
   FallingFact_RevTantidiag  -> 0 
   FallingFact_RevTder       -> 0 
   FallingFact_RevPolyRow3   -> 0 
   FallingFact_TablCol0      -> https://oeis.org/A12
   FallingFact_NegHalf       -> https://oeis.org/A23
   FallingFact_TablCol1      -> https://oeis.org/A27
   FallingFact_TablGcd       -> https://oeis.org/A27
   FallingFact_PolyRow1      -> https://oeis.org/A27
   FallingFact_RevPolyRow1   -> https://oeis.org/A27
   FallingFact_TablDiag0     -> https://oeis.org/A142
   FallingFact_TablDiag1     -> https://oeis.org/A142
   FallingFact_TablLcm       -> https://oeis.org/A142
   FallingFact_TablMax       -> https://oeis.org/A142
   FallingFact_AltSum        -> https://oeis.org/A166
   FallingFact_RevNegHalf    -> https://oeis.org/A354
   FallingFact_RevCentralO   -> https://oeis.org/A407
   FallingFact_TablSum       -> https://oeis.org/A522
   FallingFact_AbsSum        -> https://oeis.org/A522
   FallingFact_AccRevSum     -> https://oeis.org/A1339
   FallingFact_TransNat1     -> https://oeis.org/A1339
   FallingFact_TablDiag2     -> https://oeis.org/A1710
   FallingFact_TablDiag3     -> https://oeis.org/A1715
   FallingFact_CentralE      -> https://oeis.org/A1813
   FallingFact_PolyRow2      -> https://oeis.org/A1844
   FallingFact_TablCol2      -> https://oeis.org/A2378
   FallingFact_RevPolyRow2   -> https://oeis.org/A2522
   FallingFact_BinConv       -> https://oeis.org/A2720
   FallingFact_OddSum        -> https://oeis.org/A2747
   FallingFact_RevAntiDSum   -> https://oeis.org/A3470
   FallingFact_CentralO      -> https://oeis.org/A6963
   FallingFact_RevTransNat0  -> https://oeis.org/A7526
   FallingFact_TablCol3      -> https://oeis.org/A7531
   FallingFact_Triangle      -> https://oeis.org/A8279
   FallingFact_Talt          -> https://oeis.org/A8279
   FallingFact_RevEvenSum    -> https://oeis.org/A9179
   FallingFact_InvBinConv    -> https://oeis.org/A9940
   FallingFact_PosHalf       -> https://oeis.org/A10842
   FallingFact_PolyCol2      -> https://oeis.org/A10844
   FallingFact_PolyCol3      -> https://oeis.org/A10845
   FallingFact_RevTransSqrs  -> https://oeis.org/A30297
   FallingFact_RevPolyCol3   -> https://oeis.org/A53486
   FallingFact_RevPolyDiag   -> https://oeis.org/A63170
   FallingFact_Toff11        -> https://oeis.org/A68424
   FallingFact_AntiDSum      -> https://oeis.org/A72374
   FallingFact_RevColMiddle  -> https://oeis.org/A81125
   FallingFact_EvenSum       -> https://oeis.org/A87208
   FallingFact_TransNat0     -> https://oeis.org/A93964
   FallingFact_Trev          -> https://oeis.org/A94587
   FallingFact_RevTalt       -> https://oeis.org/A94587
   FallingFact_AccSum        -> https://oeis.org/A111063
   FallingFact_RevAccRevSum  -> https://oeis.org/A111063
   FallingFact_RevTransNat1  -> https://oeis.org/A111063
   FallingFact_Tinvrev       -> https://oeis.org/A128229
   FallingFact_RevToff11     -> https://oeis.org/A173333
   FallingFact_RevTrev11     -> https://oeis.org/A181511
   FallingFact_RevOddSum     -> https://oeis.org/A186763
   FallingFact_ColMiddle     -> https://oeis.org/A205825
   FallingFact_PolyDiag      -> https://oeis.org/A277452
   FallingFact_TransSqrs     -> https://oeis.org/A343276
   FallingFact_Tantidiag     -> https://oeis.org/A344391
   FallingFact_Tacc          -> https://oeis.org/A347667
   FallingFact_RevTacc       -> https://oeis.org/A367962

    Hits: 59, Distinct: 47, Misses: 8, Doubles: 12
'''
