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
    "FallingFact",
    ["A008279", "A068424", "A094587", "A173333", "A181511"],
    "",
    r"n! / (n - k)!",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(FallingFactorial)


"""
Dict length: 67
   FallingFact_Trev11        -> 0
   FallingFact_Tder          -> 0
   FallingFact_PolyRow3      -> 0
   FallingFact_RevTinv11     -> 0
   FallingFact_RevTrevinv11  -> 0
   FallingFact_RevTantidiag  -> 0
   FallingFact_RevTder       -> 0
   FallingFact_RevPolyRow3   -> 0
   FallingFact_TablCol0      -> 12
   FallingFact_NegHalf       -> 23
   FallingFact_TablCol1      -> 27
   FallingFact_TablGcd       -> 27
   FallingFact_PolyRow1      -> 27
   FallingFact_RevPolyRow1   -> 27
   FallingFact_TablDiag0     -> 142
   FallingFact_TablDiag1     -> 142
   FallingFact_TablLcm       -> 142
   FallingFact_TablMax       -> 142
   FallingFact_AltSum        -> 166
   FallingFact_RevNegHalf    -> 354
   FallingFact_RevCentralO   -> 407
   FallingFact_TablSum       -> 522
   FallingFact_AbsSum        -> 522
   FallingFact_AccRevSum     -> 1339
   FallingFact_TransNat1     -> 1339
   FallingFact_TablDiag2     -> 1710
   FallingFact_TablDiag3     -> 1715
   FallingFact_CentralE      -> 1813
   FallingFact_PolyRow2      -> 1844
   FallingFact_TablCol2      -> 2378
   FallingFact_RevPolyRow2   -> 2522
   FallingFact_BinConv       -> 2720
   FallingFact_OddSum        -> 2747
   FallingFact_RevAntiDSum   -> 3470
   FallingFact_CentralO      -> 6963
   FallingFact_RevTransNat0  -> 7526
   FallingFact_TablCol3      -> 7531
   FallingFact_Triangle      -> 8279
   FallingFact_Talt          -> 8279
   FallingFact_RevEvenSum    -> 9179
   FallingFact_InvBinConv    -> 9940
   FallingFact_PosHalf       -> 10842
   FallingFact_PolyCol2      -> 10844
   FallingFact_PolyCol3      -> 10845
   FallingFact_RevTransSqrs  -> 30297
   FallingFact_RevPolyCol3   -> 53486
   FallingFact_RevPolyDiag   -> 63170
   FallingFact_Toff11        -> 68424
   FallingFact_AntiDSum      -> 72374
   FallingFact_RevColMiddle  -> 81125
   FallingFact_EvenSum       -> 87208
   FallingFact_TransNat0     -> 93964
   FallingFact_Trev          -> 94587
   FallingFact_RevTalt       -> 94587
   FallingFact_AccSum        -> 111063
   FallingFact_RevAccRevSum  -> 111063
   FallingFact_RevTransNat1  -> 111063
   FallingFact_Tinvrev       -> 128229
   FallingFact_RevToff11     -> 173333
   FallingFact_RevTrev11     -> 181511
   FallingFact_RevOddSum     -> 186763
   FallingFact_ColMiddle     -> 205825
   FallingFact_PolyDiag      -> 277452
   FallingFact_TransSqrs     -> 343276
   FallingFact_Tantidiag     -> 344391
   FallingFact_Tacc          -> 347667
   FallingFact_RevTacc       -> 367962
Hits: 59, Misses: 8, Doubles: 12
"""