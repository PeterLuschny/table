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
 (1) [88] ('A048993', 'StirlingSet', 172, 88, 199, 113, 1, 5, 27)
 (2) [84] ('A132393', 'StirlingCycle', 171, 84, 199, 113, 1, 5, 28)
 (3) [75] ('A008279', 'FallingFact', 147, 75, 164, 88, 1, 4, 17)
 (4) [68] ('A039599', 'DyckPaths', 136, 68, 204, 112, 1, 5, 68)
 (5) [68] ('A064189', 'Motzkin', 146, 68, 208, 114, 1, 5, 62)
 (6) [64] ('A128899', 'Catalan', 128, 64, 204, 116, 1, 5, 76)
 (7) [62] ('A113704', 'Divisibility', 125, 62, 179, 98, 1, 5, 54)
 (8) [60] ('A363914', 'Moebius', 125, 60, 180, 98, 1, 5, 55)
 (9) [59] ('A038207', 'BinaryPell', 174, 59, 200, 72, 1, 5, 26)
(10) [59] ('A122538', 'Schroeder', 132, 59, 202, 114, 1, 5, 70)
--------------------------------------------------------------------
(11) [57] ('A059481', 'Monotone', 110, 57, 162, 98, 1, 4, 52)
(12) [56] ('A137452', 'Abel', 116, 56, 204, 116, 1, 5, 88)
(13) [56] ('A072233', 'Partition', 116, 56, 201, 110, 1, 5, 85)
(14) [55] ('A056857', 'BinomialBell', 110, 55, 209, 120, 1, 5, 99)
(15) [55] ('A271703', 'Lah', 162, 55, 204, 75, 1, 5, 42)
(16) [51] ('A132062', 'Bessel', 114, 51, 203, 113, 1, 5, 89)
(17) [51] ('A090181', 'Narayana', 116, 51, 199, 114, 1, 5, 83)
(18) [50] ('A008290', 'Rencontres', 118, 50, 199, 111, 1, 5, 81)
(19) [48] ('A002262', 'Ordinals', 109, 48, 118, 55, 1, 3, 9)
(20) [47] ('A131689', 'Fubini', 89, 47, 115, 64, 1, 3, 26)
(21) [46] ('A053121', 'CatalanPaths', 126, 46, 196, 88, 1, 5, 70)
(22) [46] ('A049310', 'ChebyshevS', 123, 46, 196, 88, 1, 5, 73)
(23) [45] ('A124644', 'BinomialCatalan', 90, 45, 168, 103, 1, 4, 78)
(24) [45] ('A119879', 'EulerSec', 113, 45, 195, 90, 1, 5, 82)
(25) [44] ('A000012', 'One', 105, 44, 110, 49, 0, 4, 5)
(26) [44] ('A028246', 'Worpitzky', 93, 44, 160, 96, 1, 4, 67)
(27) [43] ('A106465', 'CTree', 108, 43, 148, 72, 1, 4, 40)
(28) [43] ('A008288', 'Delannoy', 111, 43, 166, 89, 1, 4, 55)
(29) [43] ('A123125', 'Eulerian', 96, 43, 199, 114, 1, 5, 103)
(30) [40] ('A021009', 'Laguerre', 138, 40, 211, 75, 1, 5, 73)
--------------------------------------------------------------------
(31) [40] ('A104684', 'SchroederP', 81, 40, 206, 118, 1, 5, 125)
(32) [39] ('A028338', 'StirlingCycB', 107, 39, 206, 116, 1, 5, 99)
(33) [36] ('A225479', 'OrderedCycle', 73, 36, 121, 65, 1, 3, 48)
(34) [37] ('A046716', 'Charlier', 81, 37, 249, 145, 1, 6, 168)
(35) [35] ('A007318', 'Binomial', 152, 35, 160, 38, 1, 4, 8)
(36) [35] ('A007318', 'Pascal', 152, 35, 160, 38, 1, 4, 8)
(37) [34] ('A247453', 'Euler', 130, 34, 211, 74, 1, 5, 81)
(38) [33] ('A165675', 'HyperHarmonic', 84, 33, 206, 118, 1, 5, 122)
(39) [33] ('A036561', 'Nicomachus', 78, 33, 119, 65, 1, 3, 41)
(40) [31] ('A358694', 'Harmonic', 78, 31, 204, 116, 1, 5, 126)
(41) [31] ('A172094', 'SchroederL', 79, 31, 206, 116, 1, 5, 127)
(42) [31] ('A047999', 'Sierpinski', 106, 31, 153, 56, 1, 4, 47)
(43) [30] ('A048004', 'Composition', 66, 30, 201, 115, 1, 5, 135)
(44) [28] ('A269945', 'CentralSet', 78, 28, 199, 115, 1, 5, 121)
(45) [28] ('A038719', 'Chains', 55, 28, 120, 67, 1, 3, 65)
(46) [28] ('A022166', 'Gaussq2', 87, 28, 166, 89, 1, 4, 79)
(47) [28] ('A003506', 'Leibniz', 73, 28, 82, 38, 1, 2, 9)
(48) [28] ('A000027', 'Naturals', 69, 28, 122, 67, 1, 3, 53)
(49) [28] ('A196347', 'PowLaguerre', 68, 28, 82, 38, 1, 2, 14)
(50) [28] ('A358622', 'StirlingCyc2', 59, 28, 115, 60, 1, 3, 56)
--------------------------------------------------------------------
(51) [27] ('A011971', 'Bell', 73, 27, 122, 66, 1, 3, 49)
(52) [27] ('A365676', 'PartitionDist', 64, 27, 121, 63, 1, 3, 57)
(53) [26] ('A355173', 'FussCatalan', 62, 26, 118, 63, 1, 3, 56)
(54) [26] ('A354794', 'Lehmer', 64, 26, 201, 117, 1, 5, 137)
(55) [26] ('A269939', 'WardSet', 52, 26, 118, 65, 1, 3, 66)
(56) [25] ('A053117', 'ChebyshevU', 66, 25, 118, 49, 1, 3, 52)
(57) [25] ('A217831', 'Euclid', 54, 25, 74, 37, 1, 2, 20)
(58) [25] ('A354267', 'Fibonacci', 66, 25, 126, 66, 1, 3, 60)
(59) [25] ('A099174', 'HermiteE', 93, 25, 197, 72, 1, 5, 104)
(60) [25] ('A034851', 'Lozanic', 62, 25, 166, 87, 1, 4, 104)
(61) [25] ('A358623', 'StirlingSet2', 56, 25, 115, 59, 1, 3, 59)
(62) [24] ('A367211', 'BinomialPell', 57, 24, 125, 64, 1, 3, 68)
(63) [24] ('A269940', 'CentralCycle', 48, 24, 115, 64, 1, 3, 67)
(64) [24] ('A053120', 'ChebyshevT', 62, 24, 109, 46, 1, 3, 47)
(65) [24] ('A124320', 'RisingFact', 62, 24, 169, 100, 1, 4, 107)
(66) [23] ('A359760', 'Bessel2', 79, 23, 157, 63, 1, 4, 78)
(67) [23] ('A340556', 'Eulerian2', 55, 23, 118, 65, 1, 3, 63)
(68) [23] ('A359364', 'MotzkinPoly', 66, 23, 157, 77, 1, 4, 91)
(69) [23] ('A008281', 'Seidel', 61, 23, 118, 63, 1, 3, 57)
(70) [22] ('A154602', 'StirlingSetB', 51, 22, 206, 116, 1, 5, 155)
(71) [21] ('A367564', 'BinomialDiffPell', 56, 21, 208, 112, 1, 5, 152)
(72) [20] ('A050446', 'Kekule', 58, 20, 170, 99, 1, 4, 112)
(73) [20] ('A139600', 'Polygonal', 51, 20, 118, 63, 1, 3, 67)
(74) [20] ('A008280', 'SeidelBoust', 43, 20, 121, 66, 1, 3, 78)
(75) [20] ('A341101', 'Sylvester', 41, 20, 122, 67, 1, 3, 81)
(76) [19] ('A356546', 'Levin', 51, 19, 82, 38, 1, 2, 31)
(77) [19] ('A026820', 'PartitionMax', 48, 19, 118, 63, 1, 3, 70)
(78) [18] ('A359363', 'Baxter', 42, 18, 120, 67, 1, 3, 78)
(79) [17] ('A126198', 'CompositionMax', 44, 17, 118, 64, 1, 3, 74)
(80) [16] ('A060187', 'EulerianB', 49, 16, 166, 89, 1, 4, 117)
(81) [16] ('A205497', 'EulerianZigZag', 37, 16, 153, 94, 1, 4, 116)
(82) [16] ('A355172', 'TernaryTrees', 46, 16, 118, 64, 1, 3, 72)
(83) [15] ('A162660', 'EulerTan', 45, 15, 116, 48, 1, 3, 71)
(84) [14] ('A060821', 'HermiteH', 42, 14, 118, 49, 1, 3, 76)
(85) [13] ('A360603', 'LabeledGraphs', 37, 13, 121, 64, 1, 3, 84)
(86) [12] ('A371761', 'Parades', 34, 12, 78, 38, 1, 2, 44)
(87) [10] ('A297703', 'Genocchi', 32, 10, 122, 65, 1, 3, 90)

The statistics were created on 2024-06-16 18:27:42.747889.
"""