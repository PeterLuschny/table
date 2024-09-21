![Tables](imag/IntegerTrianglesPy.png)

# The objectives of this library

* The library aims to provide the ~100 most interesting integer triangles listed in the OEIS. If you are new to this subject look into the [ranking](https://github.com/PeterLuschny/table/blob/main/src/Ranking.txt) of the triangles to see where to begin your studies.

* In addition, it provides a dozen methods for manipulating the triangles.

* Further, the library serves as the basis for a project in which the triangles are analyzed in more detail and connections to other sequences are investigated.  You can take a look here: [TriangleAnalyser](https://luschny.de/math/oeis/Abel.html).

# Installation

Currently there is only one dependency. Make sure your Python has the "more_itertools" package installed.

* If you want to use the package only in one project just copy the file "Tables.py" (only this file!) into the root directory of your project.

* If you want to install it globaly into your Python environment do this: Following the advice from [stackoverflow](https://stackoverflow.com/a/16196400) query the Python user directory in your shell:

      python -m site --user-site

  If the returned directory does not yet exist create it with:

      mkdir -p "the answer from the query"

  On Windows this creates the directory:

      C:\Users\UserName\AppData\Roaming\Python\Python312\site-packages

  Then move the file Tables.py (only this file!) to this directory.

* If you want to use it in a SageMath Jupyter notebook, then put on top of the file

      load("Tables.py")

* If you want to contribute to the development fork it on GitHub.


# Example use

Next test the installation.

 ### Example 1
    from Tables import QuickView

    QuickView()

This shows the list of the sequences implemented.

Use a Table from the library:

 ### Example 2
    from Tables import PreView, StirlingSet

    PreView(StirlingSet)

Define your own Table:

 ### Example 3
    from Tables import Table, PreView
    from functools import cache
    from math import comb as binomial

    @cache
    def abel(n: int) -> list[int]:
        if n == 0: return [1]
        return [binomial(n - 1, k - 1) * n ** (n - k) if k > 0 else 0
                for k in range(n + 1)]

    Abel = Table(abel, "Abel", ["A137452", "A061356", "A139526"], True)

    PreView(Abel)


# How to use

There is only one constructor: Table(...). The parameters are:

    row:  gen                 # The row generator, gen(n:int) -> list[int].
    id:   str                 # The name of the triangle.
    sim:  list[str] = ['']    # References to similar OEIS-sequences.
    invQ: bool | None = None  # Is the triangle invertible?
                              # Default 'None' means 'I do not know'.

The row generator is a function of type: g(n: int) -> list[int] defined for all nonnegative n.
This function should be decorated with '@cache' and return a list of integers of length n + 1.

A Table T provides the following methods:

    val (n:int, k:int)   -> int  | T(n, k)
    poly(n: int, x: int) -> int  | sum(T(n, k) * x^j for j=0..n)
    flat (size: int)     -> list[int] | flattened form of the first size rows
    diag(n, size: int)   -> list[int] | diagonal starting at the left side
    col (k, size: int)   -> list[int] | k-th column starting at the main diagonal
    sum (size: int)      -> list[int] | sums of the first size rows
    row (n: int)         -> trow | n-th row of table
    tab (size: int)      -> tabl | table with size rows
    rev (size: int)      -> tabl | table with reversed rows
    adtab (size: int)    -> tabl | table of (upward) anti-diagonals
    acc (size: int)      -> tabl | table with rows accumulated
    diff (size: int)     -> tabl | table with first difference of rows
    mat (size: int)      -> tabl | matrix form of lower triangular array
    inv (size: int)      -> tabl | inverse table
    revinv (size: int)   -> tabl | row reversed inverse
    invrev (size: int)   -> tabl | inverse of row reversed
    off (N: int, K: int) -> rgen | new offset (N, K)
    invrev11 (size: int) -> tabl | invrev from offset (1, 1)
    summap(s: seq, size) -> list[int] | linear transformation induced by T
    invmap(s: seq, size) -> list[int] | inverse transformation induced by T
    show(size: int)      -> None | prints the first 'size' rows with row-numbers

The type 'tabl' is a triangular array that is a list of lists of the form
[[0] * (n + 1) for n in range(size)] representing the first 'size' rows of
the triangle.


# For developers

You are invited to share your code and add it to the library. Only sequences already in the OEIS will be considered. Please send a pull request!

Observe the design constraints:

  1) No use of extern modules like SymPy or NumPy; only use standard modules, but the use of the package [more-itertools](https://pypi.org/project/more-itertools/) is OK.

  2) All tables are (0,0)-based. If the table in the OEIS is (1,1)-based, adapt it. Often the best way to do this is to prepend a column (1, 0, 0, ...) to the left of the table.

  3) Keep the design philosophy you see in the code: base the implementations on the rows of a triangle, not on the individual T(n, k), whenever possible. In other words, we regard a triangle as a 1-dim sequence of lists, not as a 2-dim matrix of terms.

  4) We do not aim for one-liners. Readability is important.

Workflow:

  1) Copy the Template.py file, rename the copy "Myseq.py", and replace in the file the function "template" with your sequence function "myseq" and the class "Template" by "Myseq". Note the case sensitivity and that "@cache" for "myseq" is mandatory.

  2) In the file _tablmake insert the names "Myseq.py" and "Myseq" in the list of files and classes.

  3) Execute the file _tablmake (producing a new Tables.py). Done.
