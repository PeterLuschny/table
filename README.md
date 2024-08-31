![Tables](imag/IntegerTrianglesPy.png)

# The objectives of this library

* The library aims to provide the ~100 most interesting integer triangles listed in the OEIS. 

* In addition, it provides a dozen methods for manipulating the triangles.


# Installation

Following the advice of https://stackoverflow.com/a/16196400

Query in your shell: 

    python -m site --user-site

Create the path given in the returned answer: 

    mkdir -p "the answer from the query"

On Windows this creates the directory:

    C:\Users\UserName\AppData\Roaming\Python\Python312\site-packages

Put the file Tables.py (only this file!) there.

# Examples

Next test the installation: Put the following lines in some test.py. (This file can also be found in the root.)

 ### Example 1
    from Tables import Tables, Table, PreView, StirlingSet

    PreView(StirlingSet)

 ### Example 2
    from functools import cache
    from math import comb as binomial

    @cache
    def abel(n: int) -> list[int]:
        if n == 0: return [1]
        return [binomial(n - 1, k - 1) * n ** (n - k) if k > 0 else 0 
                for k in range(n + 1)]

    Abel = Table(abel, "Abel", ["A137452", "A061356", "A139526"], True)

    PreView(Abel)

The last example shows how you can use the functionality of Tables with sequences you define yourself.

### Example 3
    for tabl in Tables: 
        print(tabl.id)

This shows the list of the sequences implemented. A brief overview of their relative relevance can be found in the file _statistics.txt.


# How to use

There is only one constructor: Table(...). The parameters are:

    row:  rgen                # The row generator.
    id:   str                 # The name of the sequence.
    sim:  list[str] = ['']    # References to similar OEIS-sequences.
    invQ: bool | None = None  # Is the triangle invertible? 
                              # Default 'None' means 'I do not know'.

The row generator is a function of type: g(n: int) -> list[int] defined for all nonnegative n (see example 3). 
This function should be decorated with '@cache' and return a list of integers of length n + 1.

A Table T provides the following methods:

    val (n:int, k:int)   -> int  | T(n, k)
    poly(n: int, x: int) -> int  | sum(T(n, k) * x^j for j=0..n)
    flat (size: int)     -> list[int] | flattened form of the first size rows
    diag(n, size: int)   -> list[int] | diagonal starting at the left side
    col (k, size: int)   -> list[int] | k-th column starting at the main diagonal
    row (n: int)         -> trow | n-th row of table
    tab (size: int)      -> tabl | table with size rows
    rev (size: int)      -> tabl | tabel with reversed rows
    adtab (size: int)    -> tabl | table of (upward) anti-diagonals
    acc (size: int)      -> tabl | table with rows accumulated
    mat (size: int)      -> tabl | matrix form of lower triangular array
    inv (size: int)      -> tabl | inverse table
    revinv (size: int)   -> tabl | row reversed inverse
    invrev (size: int)   -> tabl | inverse of row reversed
    off (N: int, K: int) -> rgen | new offset (N, K)
    invrev11 (size: int) -> tabl | invrev from offset (1, 1)
    summap(s: seq, size) -> list[int] | linear transformation induced by T
    invmap(s: seq, size) -> list[int] | inverse transformation induced by T

The type 'tabl' is a triangular array that is a list of lists of the form
[[0] * (n + 1) for n in range(size)] representing the first 'size' rows of 
the triangle (see also example 2 above).


# For developers

You are invited to share your code and add it to the library. Only sequences already in the OEIS will be considered. Send a pull request!

Observe the design constraints:

  1) No use of extern modules (like SymPy or NumPy); only use standard modules.

  2) All tables are (0,0)-based. If the table in the OEIS is (1,1)-based, adapt it. Often the best way to do this is to prepend a column (1, 0, 0, ...) to the left of the table.

  3) Keep the design philosophy you see in the code: all implementations are based on the rows of a triangle, not on individual terms T(n, k).

  4) We do not aim for one-liners. Readability is important.


# Efficiency

To give an idea of ​​the performance of the library, we provide the following table. It shows the time required to calculate the first 100 rows of each triangle (which corresponds to the calculation of 5050 terms).

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
                Eytzinger 0.0031 sec
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
                PolyaTree 9.9018 sec
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

102 tables tested!
