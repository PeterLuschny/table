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

Next test the installation: Put the following lines in some test.py.

 ### Example 1
    from Tables import Tables, Table, View, StirlingSet

    View(StirlingSet)


### Example 2
    T = [[ 1 ], [0, 1], [0, -2, 1], [0, 3, -6, 1], [0, -4, 24, -12, 1], 
         [0, 5, -80, 90, -20, 1]]

    Babel = Table(T, "Babel", ["A059297"], True)

    View(Babel)


 ### Example 3
    from functools import cache
    from math import comb as binomial

    @cache
    def abel(n: int) -> list[int]:
        if n == 0: return [1]
        return [binomial(n - 1, k - 1) * n ** (n - k) if k > 0 else 0 
                for k in range(n + 1)]

    Abel = Table(abel, "Abel", ["A137452", "A061356", "A139526"], True)

    View(Abel)

The last example shows how you can use the functionality of Tables with sequences you define yourself.

### Example 4
    for tabl in Tables: 
        print(tabl.id)

This shows the list of the sequences implemented. A brief overview of their relative relevance can be found in the file _statistics.txt.


# How to use

There is only one constructor: Table(...). The parameters are:

    gen: rgen | tabl          # The generator.
    id: str                   # The name of the sequence.
    sim: list[str] = ['']     # References to similar OEIS-sequences.
    invQ: bool | None = None  # Is the triangle invertible? 
                              # Default 'None' means 'I do not know'.


The generator is either a triangular array of integers as in example 2.

Or a function of type: fun(n: int) -> list[int] defined for all nonnegative n as in example 3. 
This function should be decorated with '@cache' and return a list of integers of length n + 1.

A Table provides the following methods:

    val (n:int, k:int)   -> int  | T(n, k)
    row (n: int)         -> trow | n-th row of table
    tab (size: int)      -> tabl | table with size rows
    rev (size: int)      -> tabl | row reversed
    diag (size: int)     -> tabl | upwards antidiagonals
    acc (size: int)      -> tabl | accumulated rows
    mat (size: int)      -> tabl | matrix form
    flat (size: int)     -> trow | flattened form
    inv (size: int)      -> tabl | inverse table
    revinv (size: int)   -> tabl | row reversed inverse
    invrev (size: int)   -> tabl | inverse of row reversed
    off (N: int, K: int) -> rgen | new offset (N, K)
    invrev11 (size: int) -> tabl | invrev from offset (1, 1)


# For developers

You are invited to share your code and add it to the library. Only sequences already in the OEIS will be considered.
Send a pull request!

Observe the design constraints:

  1) No use of extern modules (like SymPy or NumPy); only use standard modules.

  2) All tables are (0,0)-based. If the table in the OEIS is (1,1)-based, adapt it. Often the best way to do this is to prepend a column (1, 0, 0, ...) to the left of the table.

  3) Keep the design philosophy you see in the code: all implementations are based on the rows of a triangle, not on individual terms T(n, k).

  4) We do not aim for one-liners. Readability is important.
