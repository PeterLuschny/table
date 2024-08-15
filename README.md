# For users:

Installation: Following the advice of https://stackoverflow.com/a/16196400

Query in your shell: 

    python -m site --user-site

Create the path given in the answer: 

    mkdir -p "put the answer from the query"

On Windows this creates the diretory:

    C:\Users\UserName\AppData\Roaming\Python\Python312\site-packages

Put the file Tables.py (only this file!) there.

Next test the installation: Put the following lines in some test.py.


    from functools import cache
    from math import comb as binomial
    from Tables import Table, View, StirlingSet

    View(StirlingSet)


    T = [[ 1 ], [0, 1], [0, -2, 1], [0, 3, -6, 1], [0, -4, 24, -12, 1], 
         [0, 5, -80, 90, -20, 1]]

    Babel = Table(T, "Babel", ["A059297"], True)

    View(Babel)


    @cache
    def abel(n: int) -> list[int]:
        if n == 0: return [1]
        return [binomial(n - 1, k - 1) * n ** (n - k) if k > 0 else 0 
                for k in range(n + 1)]

    Abel = Table(abel, "Abel", ["A137452", "A061356", "A139526"], True)

    View(Abel)


A brief overview of the sequences covered and their relevance can be found in the file _statistics.txt.


# For developers:

The last example above shows how you can use the functionality of Tables with sequence you define.

You are invited to share your code and add it to this library. 
Send a pull request!

The library aims to provide the ~100 most interesting integer triangles listed in the OEIS. 

We have three design constraints:

  1) No use of extern modules (like SymPy or NumPy); only use standard modules.

  2) Keep the simple design philosophy you see in the implementations, which all are based on the rows of a triangle, not on individual terms T(n, k).

  3) We do not aim for one-liners. Readability is more important.


... the documentation is still incomplete. We are working on it.
