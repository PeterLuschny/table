from functools import cache
from _tabltypes import Table

"""Rising factorial.

[0]  1;
[1]  1, 1;
[2]  1, 2,   6;
[3]  1, 3,  12,  60;
[4]  1, 4,  20, 120,  840;
[5]  1, 5,  30, 210, 1680, 15120;
[6]  1, 6,  42, 336, 3024, 30240, 332640;
[7]  1, 7,  56, 504, 5040, 55440, 665280, 8648640;
"""


@cache
def risingfactorial(n: int) -> list[int]:
    if n == 0:
        return [1]

    row = [1 for _ in range(n + 1)]
    row[1] = n
    for k in range(1, n):
        row[k + 1] = row[k] * (n + k)
    return row


RisingFactorial = Table(
    risingfactorial, 
    "RisingFactorial", 
    ["A124320"], 
    "", 
    r"k! \binom{n+k-1}{k}",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(RisingFactorial)


''' OEIS
    RisingFact_Trev          -> 0 
    RisingFact_Tinvrev       -> 0 
    RisingFact_Toff11        -> 0 
    RisingFact_Trev11        -> 0 
    RisingFact_Tantidiag     -> 0 
    RisingFact_Tacc          -> 0 
    RisingFact_Tder          -> 0 
    RisingFact_EvenSum       -> 0 
    RisingFact_OddSum        -> 0 
    RisingFact_AltSum        -> 0 
    RisingFact_AccSum        -> 0 
    RisingFact_AccRevSum     -> 0 
    RisingFact_AntiDSum      -> 0 
    RisingFact_ColMiddle     -> 0 
    RisingFact_PosHalf       -> 0 
    RisingFact_NegHalf       -> 0 
    RisingFact_TransNat0     -> 0 
    RisingFact_TransNat1     -> 0 
    RisingFact_TransSqrs     -> 0 
    RisingFact_PolyRow3      -> 0 
    RisingFact_PolyCol2      -> 0 
    RisingFact_PolyCol3      -> 0 
    RisingFact_PolyDiag      -> 0 
    RisingFact_RevToff11     -> 0 
    RisingFact_RevTrev11     -> 0 
    RisingFact_RevTinv11     -> 0 
    RisingFact_RevTrevinv11  -> 0 
    RisingFact_RevTantidiag  -> 0 
    RisingFact_RevTacc       -> 0 
    RisingFact_RevTalt       -> 0 
    RisingFact_RevTder       -> 0 
    RisingFact_RevEvenSum    -> 0 
    RisingFact_RevOddSum     -> 0 
    RisingFact_RevAccRevSum  -> 0 
    RisingFact_RevAntiDSum   -> 0 
    RisingFact_RevColMiddle  -> 0 
    RisingFact_RevCentralO   -> 0 
    RisingFact_RevNegHalf    -> 0 
    RisingFact_RevTransNat0  -> 0 
    RisingFact_RevTransNat1  -> 0 
    RisingFact_RevTransSqrs  -> 0 
    RisingFact_RevPolyRow3   -> 0 
    RisingFact_RevPolyCol3   -> 0 
    RisingFact_RevPolyDiag   -> 0 
    RisingFact_TablCol0      -> https://oeis.org/A12
    RisingFact_TablCol1      -> https://oeis.org/A27
    RisingFact_TablGcd       -> https://oeis.org/A27
    RisingFact_PolyRow1      -> https://oeis.org/A27
    RisingFact_RevPolyRow1   -> https://oeis.org/A27
    RisingFact_TablDiag0     -> https://oeis.org/A407
    RisingFact_TablLcm       -> https://oeis.org/A407
    RisingFact_TablMax       -> https://oeis.org/A407
    RisingFact_TablDiag3     -> https://oeis.org/A1761
    RisingFact_TablDiag1     -> https://oeis.org/A1813
    RisingFact_TablCol2      -> https://oeis.org/A2378
    RisingFact_TablDiag2     -> https://oeis.org/A6963
    RisingFact_TablCol3      -> https://oeis.org/A7531
    RisingFact_CentralO      -> https://oeis.org/A64352
    RisingFact_RevPolyRow2   -> https://oeis.org/A117951
    RisingFact_TablSum       -> https://oeis.org/A123680
    RisingFact_AbsSum        -> https://oeis.org/A123680
    RisingFact_Triangle      -> https://oeis.org/A124320
    RisingFact_Talt          -> https://oeis.org/A124320
    RisingFact_PolyRow2      -> https://oeis.org/A136392
    RisingFact_InvBinConv    -> https://oeis.org/A278069
    RisingFact_BinConv       -> https://oeis.org/A278070
    RisingFact_CentralE      -> https://oeis.org/A352601

    RisingFact: Distinct: 17, Hits: 23, Misses: 44
'''
