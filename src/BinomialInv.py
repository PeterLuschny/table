from functools import cache
from _tabltypes import Table
from Binomial import binomial

"""Inverse binomial triangle:

   1;
  -1,    1;
   1,   -2,    1;
  -1,    3,   -3,    1;
   1,   -4,    6,   -4,    1;
  -1,    5,  -10,   10,   -5,    1;
   1,   -6,   15,  -20,   15,   -6,    1;
  -1,    7,  -21,   35,  -35,   21,   -7,    1;
   1,   -8,   28,  -56,   70,  -56,   28,   -8,    1;
  -1,    9,  -36,   84, -126,  126,  -84,   36,   -9,    1;
  ...
"""

@cache
def binomialinv(n: int) -> list[int]:
    return [(-1)**(n - k) * binomial(n)[k] for k in range(n + 1)]


BinomialInf = Table(
    binomialinv,
    "InvBinomial",
    ["A130595"],
    "A007318",
    r"(-1)^{n-k} \, n! \, / (k! \, (n - k)! )",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(BinomialInf)


''' OEIS
    InvBinomial_Tinvrev       -> 0 
    InvBinomial_RevTinv11     -> 0 
    InvBinomial_RevTrevinv11  -> 0 
    InvBinomial_TablSum       -> https://oeis.org/A7
    InvBinomial_AccSum        -> https://oeis.org/A7
    InvBinomial_AccRevSum     -> https://oeis.org/A7
    InvBinomial_TransNat0     -> https://oeis.org/A7
    InvBinomial_TransNat1     -> https://oeis.org/A7
    InvBinomial_TransSqrs     -> https://oeis.org/A7
    InvBinomial_RevAccRevSum  -> https://oeis.org/A7
    InvBinomial_RevTransNat0  -> https://oeis.org/A7
    InvBinomial_RevTransNat1  -> https://oeis.org/A7
    InvBinomial_RevTransSqrs  -> https://oeis.org/A7
    InvBinomial_TablCol0      -> https://oeis.org/A12
    InvBinomial_TablDiag0     -> https://oeis.org/A12
    InvBinomial_PosHalf       -> https://oeis.org/A12
    InvBinomial_PolyCol2      -> https://oeis.org/A12
    InvBinomial_TablCol1      -> https://oeis.org/A27
    InvBinomial_TablDiag1     -> https://oeis.org/A27
    InvBinomial_PolyRow1      -> https://oeis.org/A27
    InvBinomial_RevPolyRow1   -> https://oeis.org/A27
    InvBinomial_AntiDSum      -> https://oeis.org/A45
    InvBinomial_EvenSum       -> https://oeis.org/A79
    InvBinomial_OddSum        -> https://oeis.org/A79
    InvBinomial_AltSum        -> https://oeis.org/A79
    InvBinomial_AbsSum        -> https://oeis.org/A79
    InvBinomial_PolyCol3      -> https://oeis.org/A79
    InvBinomial_RevEvenSum    -> https://oeis.org/A79
    InvBinomial_RevOddSum     -> https://oeis.org/A79
    InvBinomial_RevPolyCol3   -> https://oeis.org/A79
    InvBinomial_TablCol2      -> https://oeis.org/A217
    InvBinomial_TablDiag2     -> https://oeis.org/A217
    InvBinomial_NegHalf       -> https://oeis.org/A244
    InvBinomial_RevNegHalf    -> https://oeis.org/A244
    InvBinomial_PolyRow2      -> https://oeis.org/A290
    InvBinomial_RevPolyRow2   -> https://oeis.org/A290
    InvBinomial_TablCol3      -> https://oeis.org/A292
    InvBinomial_TablDiag3     -> https://oeis.org/A292
    InvBinomial_PolyRow3      -> https://oeis.org/A578
    InvBinomial_RevPolyRow3   -> https://oeis.org/A578
    InvBinomial_CentralE      -> https://oeis.org/A984
    InvBinomial_InvBinConv    -> https://oeis.org/A984
    InvBinomial_TablMax       -> https://oeis.org/A1405
    InvBinomial_ColMiddle     -> https://oeis.org/A1405
    InvBinomial_RevColMiddle  -> https://oeis.org/A1405
    InvBinomial_CentralO      -> https://oeis.org/A1700
    InvBinomial_RevCentralO   -> https://oeis.org/A1700
    InvBinomial_TablLcm       -> https://oeis.org/A2944
    InvBinomial_Tder          -> https://oeis.org/A3506
    InvBinomial_RevTder       -> https://oeis.org/A3506
    InvBinomial_Triangle      -> https://oeis.org/A7318
    InvBinomial_Tinv          -> https://oeis.org/A7318
    InvBinomial_Trev          -> https://oeis.org/A7318
    InvBinomial_Trevinv       -> https://oeis.org/A7318
    InvBinomial_Talt          -> https://oeis.org/A7318
    InvBinomial_RevTalt       -> https://oeis.org/A7318
    InvBinomial_PolyDiag      -> https://oeis.org/A7778
    InvBinomial_RevPolyDiag   -> https://oeis.org/A7778
    InvBinomial_RevAntiDSum   -> https://oeis.org/A11655
    InvBinomial_Tantidiag     -> https://oeis.org/A11973
    InvBinomial_RevTantidiag  -> https://oeis.org/A11973
    InvBinomial_TablGcd       -> https://oeis.org/A14963
    InvBinomial_Toff11        -> https://oeis.org/A74909
    InvBinomial_Trev11        -> https://oeis.org/A74909
    InvBinomial_Tinv11        -> https://oeis.org/A74909
    InvBinomial_Trevinv11     -> https://oeis.org/A74909
    InvBinomial_RevToff11     -> https://oeis.org/A74909
    InvBinomial_RevTrev11     -> https://oeis.org/A74909
    InvBinomial_Tacc          -> https://oeis.org/A97805
    InvBinomial_RevTacc       -> https://oeis.org/A97805
    InvBinomial_BinConv       -> https://oeis.org/A126869

    InvBinomial     , Distinct: 24, Hits: 68, Misses: 3
'''
