from typing import Dict

Ranking : Dict[int, list[str]] = {
     1: ['A048993', 'StirlingSet'],
     2: ['A132393', 'StirlingCycle'],
     3: ['A008279', 'FallingFact'],
     4: ['A039599', 'DyckPaths'],
     5: ['A064189', 'Motzkin'],
     6: ['A128899', 'Catalan'],
     7: ['A113704', 'Divisibility'],
     8: ['A363914', 'Moebius'],
     9: ['A038207', 'BinaryPell'],
    10: ['A122538', 'Schroeder'],
    11: ['A059481', 'Monotone'],
    12: ['A137452', 'Abel'],
    13: ['A072233', 'Partition'],
    14: ['A056857', 'BinomialBell'],
    15: ['A271703', 'Lah'],
    16: ['A132062', 'Bessel'],
    17: ['A090181', 'Narayana'],
    18: ['A008290', 'Rencontres'],
    19: ['A002262', 'Ordinals'],
    20: ['A131689', 'Fubini'],
    21: ['A053121', 'CatalanPaths'],
    22: ['A049310', 'ChebyshevS'],
    23: ['A124644', 'BinomialCatalan'],
    24: ['A119879', 'EulerSec'],
    25: ['A000012', 'One'],
    26: ['A028246', 'Worpitzky'],
    27: ['A106465', 'CTree'],
    28: ['A008288', 'Delannoy'],
    29: ['A123125', 'Eulerian'],
    30: ['A021009', 'Laguerre'],
    31: ['A104684', 'SchroederP'],
    32: ['A028338', 'StirlingCycB'],
    33: ['A225479', 'OrderedCycle'],
}
 
"""
Ranking of triangles with regard to their impact:

*** Premier League ***

Stirlingset     Hits: 62, Distinct: 52, Misses:  7, 
Fallingfact     Hits: 59, Distinct: 47, Misses:  8, 
Stirlingcycle   Hits: 62, Distinct: 43, Misses:  6, 
Binarypell      Hits: 55, Distinct: 44, Misses: 13, 
Lah             Hits: 54, Distinct: 44, Misses: 14, 
Lucas           Hits: 60, Distinct: 44, Misses:  6,
Partition       Hits: 54, Distinct: 42, Misses: 15, 
Catalaninv      Hits: 48, Distinct: 41, Misses: 20, 
Fubini          Hits: 49, Distinct: 41, Misses: 16, 
Power           Hits: 49, Distinct: 39, Misses: 20, 
Besselinv       Hits: 48, Distinct: 38, Misses: 20, 
Dyckpaths       Hits: 50, Distinct: 38, Misses: 18, 
Motzkin         Hits: 47, Distinct: 37, Misses: 21, 
Catalan         Hits: 43, Distinct: 36, Misses: 25,
Monotone        Hits: 51, Distinct: 36, Misses: 16, 
Eulerian        Hits: 55, Distinct: 36, Misses: 14, 

*** Second Division ***

Abel            Hits: 41, Distinct: 35, Misses: 27, 
Abelinv         Hits: 41, Distinct: 35, Misses: 27, 
Schroeder       Hits: 44, Distinct: 35, Misses: 24, 
Laguerre        Hits: 43, Distinct: 35, Misses: 25, 
Narayana        Hits: 54, Distinct: 35, Misses: 15, 
Bessel          Hits: 41, Distinct: 34, Misses: 27, 
Binomialbell    Hits: 41, Distinct: 34, Misses: 27, 
Divisibility    Hits: 57, Distinct: 34, Misses: 12, 
Catalanpaths    Hits: 51, Distinct: 33, Misses: 17, 
Chebyshevs      Hits: 48, Distinct: 33, Misses: 20, 
Orderedcycle    Hits: 38, Distinct: 33, Misses: 26, 
Nicomachus      Hits: 41, Distinct: 33, Misses: 23,
Binomialcatalan Hits: 38, Distinct: 32, Misses: 29, 
LeibnizScheme   Hits: 51, Distinct: 31, Misses: 13,
Rencontres      Hits: 42, Distinct: 31, Misses: 26, 
Worpitzky       Hits: 41, Distinct: 30, Misses: 26, 

# Efficiency

To give an idea of the performance of the library, we provide the following table. 
It shows the time required to calculate the first 100 rows of each triangle 
(which corresponds to the calculation of 5050 terms).

                     Abel 0.0052 sec
                    Andre 0.0320 sec
                   Baxter 0.0110 sec
                     Bell 0.0037 sec
                   Bessel 0.0020 sec
                  Bessel2 0.0021 sec
               BinaryPell 0.0020 sec
                 Binomial 0.0005 sec
             BinomialBell 0.0033 sec
          BinomialCatalan 0.0079 sec
             BinomialPell 0.0034 sec
         BinomialDiffPell 0.0067 sec
                  Catalan 0.0026 sec
             CatalanPaths 0.0049 sec
             CentralCycle 0.0023 sec
               CentralSet 0.0029 sec
                   Chains 0.0062 sec
                 Charlier 0.0054 sec
               ChebyshevS 0.0029 sec
               ChebyshevT 0.0015 sec
               ChebyshevU 0.0032 sec
              Composition 0.0188 sec
           CompositionAcc 0.0016 sec
          CompositionDist 0.0029 sec
                    CTree 0.0003 sec
                 Delannoy 0.0025 sec
             Divisibility 0.0010 sec
                DyckPaths 0.0023 sec
                   Euclid 0.0068 sec
                    Euler 0.0044 sec
                 Eulerian 0.0029 sec
                Eulerian2 0.0027 sec
                EulerianB 0.0041 sec
           EulerianZigZag 0.3919 sec
                 EulerSec 0.0026 sec
                 EulerTan 0.0023 sec
           EytzingerOrder 0.0028 sec
            EytzingerPerm 0.0018 sec
              FallingFact 0.0012 sec
                FiboLucas 0.0012 sec
             FiboLucasInv 0.0012 sec
             FiboLucasRev 0.0008 sec
                Fibonacci 0.0014 sec
                   Fubini 0.0063 sec
              FussCatalan 0.0010 sec
                  Gaussq2 0.0037 sec
                 Genocchi 0.0032 sec
                 Harmonic 0.0018 sec
                 HermiteE 0.0027 sec
                 HermiteH 0.0019 sec
            HyperHarmonic 0.0018 sec
               Jacobsthal 0.0022 sec
                   Kekule 0.0045 sec
            LabeledGraphs 0.0245 sec
                 Laguerre 0.0024 sec
                      Lah 0.0096 sec
                   Lehmer 0.2257 sec
                  Leibniz 0.0018 sec
            LeibnizScheme 0.0008 sec
                    Levin 0.0025 sec
                  Lozanic 0.0016 sec
                    Lucas 0.0011 sec
                LucasPoly 0.0015 sec
                  Moebius 0.0020 sec
                 Monotone 0.0052 sec
                  Motzkin 0.0061 sec
              MotzkinPoly 0.0018 sec
                 Narayana 0.0050 sec
                 Naturals 0.0011 sec
               Nicomachus 0.0014 sec
                   NimSum 0.0007 sec
                      One 0.0003 sec
                 Ordinals 0.0004 sec
             OrderedCycle 0.0035 sec
                  Parades 0.0693 sec
                Partition 0.0093 sec
             PartitionAcc 0.0008 sec
            PartitionDist 0.0026 sec
        PartitionDistSize 0.3128 sec
                   Pascal 0.0011 sec
             PolyaTreeAcc 0.4634 sec
                Polygonal 0.0013 sec
              PowLaguerre 0.0031 sec
               Rencontres 0.0026 sec
               RisingFact 0.0018 sec
               RootedTree 0.0012 sec
                Schroeder 0.0020 sec
               SchroederL 0.0023 sec
               SchroederP 0.0042 sec
                   Seidel 0.0020 sec
              SeidelBoust 0.0005 sec
               Sierpinski 0.0019 sec
            StirlingCycle 0.0025 sec
             StirlingCyc2 0.0012 sec
             StirlingCycB 0.0033 sec
              StirlingSet 0.0036 sec
             StirlingSet2 0.0057 sec
             StirlingSetB 0.0036 sec
                Sylvester 0.1552 sec
             TernaryTrees 0.0012 sec
                  WardSet 0.0031 sec
                WardCycle 0.0026 sec
                Worpitzky 0.0025 sec

                  103 tables tested!

( 1) [88] ('A048993', 'StirlingSet', 172, 88, 199, 113, 1, 5, 27)
( 2) [84] ('A132393', 'StirlingCycle', 171, 84, 199, 113, 1, 5, 28)
( 3) [75] ('A008279', 'FallingFact', 147, 75, 164, 88, 1, 4, 17)
( 4) [68] ('A039599', 'DyckPaths', 136, 68, 204, 112, 1, 5, 68)
( 5) [68] ('A064189', 'Motzkin', 146, 68, 208, 114, 1, 5, 62)
( 6) [65] ('A128899', 'Catalan', 129, 65, 204, 116, 1, 5, 75)
( 7) [62] ('A113704', 'Divisibility', 125, 62, 179, 98, 1, 5, 54)
( 8) [60] ('A363914', 'Moebius', 125, 60, 180, 98, 1, 5, 55)
( 9) [59] ('A038207', 'BinaryPell', 174, 59, 200, 72, 1, 5, 26)
(10) [59] ('A122538', 'Schroeder', 132, 59, 202, 114, 1, 5, 70)
--------------------------------------------------------------------
(11) [57] ('A059481', 'Monotone', 110, 57, 162, 98, 1, 4, 52)
(12) [56] ('A137452', 'Abel', 116, 56, 204, 116, 1, 5, 88)
(13) [56] ('A072233', 'Partition', 116, 56, 201, 110, 1, 5, 85)
(14) [55] ('A056857', 'BinomialBell', 110, 55, 209, 120, 1, 5, 99)
(15) [55] ('A271703', 'Lah', 162, 55, 204, 75, 1, 5, 42)
(16) [52] ('A132062', 'Bessel', 117, 52, 203, 113, 1, 5, 86)
(17) [51] ('A090181', 'Narayana', 116, 51, 199, 114, 1, 5, 83)
(18) [50] ('A008290', 'Rencontres', 118, 50, 199, 111, 1, 5, 81)
(19) [48] ('A002262', 'Ordinals', 109, 48, 118, 55, 1, 3, 9)
(20) [47] ('A131689', 'Fubini', 89, 47, 115, 64, 1, 3, 26)
(21) [46] ('A053121', 'CatalanPaths', 126, 46, 196, 88, 1, 5, 70)
(22) [46] ('A049310', 'ChebyshevS', 123, 46, 196, 88, 1, 5, 73)
(23) [46] ('A119879', 'EulerSec', 114, 46, 195, 90, 1, 5, 81)
(24) [45] ('A124644', 'BinomialCatalan', 90, 45, 168, 103, 1, 4, 78)
(25) [44] ('A008288', 'Delannoy', 112, 44, 166, 89, 1, 4, 54)
(26) [44] ('A000012', 'One', 105, 44, 110, 49, 0, 4, 5)
(27) [44] ('A028246', 'Worpitzky', 93, 44, 160, 96, 1, 4, 67)
(28) [43] ('A106465', 'CTree', 108, 43, 148, 72, 1, 4, 40)
(29) [43] ('A123125', 'Eulerian', 96, 43, 199, 114, 1, 5, 103)
(30) [42] ('A124038', 'FiboLucasRev', 88, 42, 211, 123, 1, 5, 123)
--------------------------------------------------------------------
(31) [40] ('A021009', 'Laguerre', 138, 40, 211, 75, 1, 5, 73)
(32) [40] ('A104684', 'SchroederP', 81, 40, 206, 118, 1, 5, 125)
(33) [40] ('A028338', 'StirlingCycB', 108, 40, 206, 116, 1, 5, 98)
(34) [38] ('A374439', 'FiboLucas', 75, 38, 169, 106, 1, 4, 94)
(35) [38] ('A375025', 'FiboLucasInv', 76, 38, 211, 122, 1, 5, 135)
(36) [37] ('A046716', 'Charlier', 81, 37, 249, 145, 1, 6, 168)
(37) [37] ('A225479', 'OrderedCycle', 76, 37, 121, 65, 1, 3, 45)
(38) [35] ('A007318', 'Binomial', 152, 35, 160, 38, 1, 4, 8)
(39) [35] ('A007318', 'Pascal', 152, 35, 160, 38, 1, 4, 8)
(40) [34] ('A247453', 'Euler', 130, 34, 211, 74, 1, 5, 81)
(41) [33] ('A165675', 'HyperHarmonic', 84, 33, 206, 118, 1, 5, 122)
(42) [33] ('A036561', 'Nicomachus', 78, 33, 119, 65, 1, 3, 41)
(43) [31] ('A358694', 'Harmonic', 78, 31, 204, 116, 1, 5, 126)
(44) [31] ('A172094', 'SchroederL', 79, 31, 206, 116, 1, 5, 127)
(45) [31] ('A047999', 'Sierpinski', 106, 31, 153, 56, 1, 4, 47)
(46) [30] ('A048004', 'Composition', 66, 30, 201, 115, 1, 5, 135)
(47) [28] ('A269945', 'CentralSet', 78, 28, 199, 115, 1, 5, 121)
(48) [28] ('A038719', 'Chains', 55, 28, 120, 67, 1, 3, 65)
(49) [28] ('A022166', 'Gaussq2', 87, 28, 166, 89, 1, 4, 79)
(50) [28] ('A003506', 'Leibniz', 73, 28, 82, 38, 1, 2, 9)
--------------------------------------------------------------------
(51) [28] ('A000027', 'Naturals', 69, 28, 122, 67, 1, 3, 53)
(52) [28] ('A196347', 'PowLaguerre', 68, 28, 82, 38, 1, 2, 14)
(53) [28] ('A358622', 'StirlingCyc2', 59, 28, 115, 60, 1, 3, 56)
(54) [27] ('A011971', 'Bell', 73, 27, 122, 66, 1, 3, 49)
(55) [27] ('A365676', 'PartitionDist', 64, 27, 121, 63, 1, 3, 57)
(56) [26] ('A355173', 'FussCatalan', 62, 26, 118, 63, 1, 3, 56)
(57) [26] ('A354794', 'Lehmer', 64, 26, 201, 117, 1, 5, 137)
(58) [26] ('A269939', 'WardSet', 52, 26, 118, 65, 1, 3, 66)
(59) [25] ('A053117', 'ChebyshevU', 66, 25, 118, 49, 1, 3, 52)
(60) [25] ('A217831', 'Euclid', 54, 25, 74, 37, 1, 2, 20)
(61) [25] ('A354267', 'Fibonacci', 66, 25, 126, 66, 1, 3, 60)
(62) [25] ('A099174', 'HermiteE', 93, 25, 197, 72, 1, 5, 104)
(63) [25] ('A034851', 'Lozanic', 62, 25, 166, 87, 1, 4, 104)
(64) [25] ('A358623', 'StirlingSet2', 56, 25, 115, 59, 1, 3, 59)
(65) [24] ('A367211', 'BinomialPell', 57, 24, 125, 64, 1, 3, 68)
(66) [24] ('A269940', 'CentralCycle', 48, 24, 115, 64, 1, 3, 67)
(67) [24] ('A053120', 'ChebyshevT', 62, 24, 109, 46, 1, 3, 47)
(68) [24] ('A124320', 'RisingFact', 62, 24, 169, 100, 1, 4, 107)
(69) [23] ('A359760', 'Bessel2', 79, 23, 157, 63, 1, 4, 78)
(70) [23] ('A340556', 'Eulerian2', 55, 23, 118, 65, 1, 3, 63)
(71) [23] ('A359364', 'MotzkinPoly', 66, 23, 157, 77, 1, 4, 91)
(72) [23] ('A008281', 'Seidel', 61, 23, 118, 63, 1, 3, 57)
(73) [22] ('A154602', 'StirlingSetB', 51, 22, 206, 116, 1, 5, 155)
(74) [21] ('A367564', 'BinomialDiffPell', 56, 21, 208, 112, 1, 5, 152)
(75) [21] ('A205497', 'EulerianZigZag', 46, 21, 153, 94, 1, 4, 107)
(76) [21] ('A374440', 'Lucas', 50, 21, 163, 99, 1, 4, 113)
(77) [20] ('A050446', 'Kekule', 58, 20, 170, 99, 1, 4, 112)
(78) [20] ('A139600', 'Polygonal', 51, 20, 118, 63, 1, 3, 67)
(79) [20] ('A008280', 'SeidelBoust', 43, 20, 121, 66, 1, 3, 78)
(80) [20] ('A341101', 'Sylvester', 41, 20, 122, 67, 1, 3, 81)
(81) [19] ('A356546', 'Levin', 51, 19, 82, 38, 1, 2, 31)
(82) [19] ('A026820', 'PartitionMax', 48, 19, 118, 63, 1, 3, 70)
(83) [18] ('A359363', 'Baxter', 42, 18, 120, 67, 1, 3, 78)
(84) [17] ('A126198', 'CompositionMax', 44, 17, 118, 64, 1, 3, 74)
(85) [16] ('A060187', 'EulerianB', 49, 16, 166, 89, 1, 4, 117)
(86) [16] ('A355172', 'TernaryTrees', 46, 16, 118, 64, 1, 3, 72)
(87) [15] ('A162660', 'EulerTan', 45, 15, 116, 48, 1, 3, 71)
(88) [14] ('A060821', 'HermiteH', 42, 14, 118, 49, 1, 3, 76)
(89) [13] ('A360603', 'LabeledGraphs', 37, 13, 121, 64, 1, 3, 84)
(90) [12] ('A371761', 'Parades', 34, 12, 78, 38, 1, 2, 44)
(91) [10] ('A297703', 'Genocchi', 32, 10, 122, 65, 1, 3, 90)
The statistics were created on 2024-12-01 12:23:52.064881 .
"""