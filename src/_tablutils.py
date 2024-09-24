from _tabltypes import Table
from typing import Callable
import time
import requests
from requests import get


oeis_schema = '''{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "items": [
      {
        "type": "object",
        "properties": {
          "greeting": {
            "type": "string"
          },
          "query": {
            "type": "string"
          },
          "count": {
            "type": "integer"
          },
          "start": {
            "type": "integer"
          },
          "results": {
            "type": "array",
            "items": [
              {
                "type": "object",
                "properties": {
                  "number": {
                    "type": "integer"
                  },
                  "id": {
                    "type": "string"
                  },
                  "data": {
                    "type": "string"
                  },
                  "name": {
                    "type": "string"
                  },
                  "comment": {
                    "type": "array",
                    "items": [
                      {
                        "type": "string"
                      }
                    ]
                  },
                  "reference": {
                    "type": "array",
                    "items": [
                      {
                        "type": "string"
                      }
                    ]
                  },
                  "link": {
                    "type": "array",
                    "items": [
                      {
                        "type": "string"
                      }
                    ]
                  },
                  "formula": {
                    "type": "array",
                    "items": [
                      {
                        "type": "string"
                      }
                    ]
                  },
                  "maple": {
                    "type": "array",
                    "items": [
                      {
                        "type": "string"
                      }
                    ]
                  },
                  "mathematica": {
                    "type": "array",
                    "items": [
                      {
                        "type": "string"
                      }
                    ]
                  },
                  "program": {
                    "type": "array",
                    "items": [
                      {
                        "type": "string"
                      }
                    ]
                  },
                  "xref": {
                    "type": "array",
                    "items": [
                      {
                        "type": "string"
                      }
                    ]
                  },
                  "keyword": {
                    "type": "string"
                  },
                  "offset": {
                    "type": "string"
                  },
                  "author": {
                    "type": "string"
                  },
                  "ext": {
                    "type": "array",
                    "items": [
                      {
                        "type": "string"
                      }
                    ]
                  },
                  "references": {
                    "type": "integer"
                  },
                  "revision": {
                    "type": "integer"
                  },
                  "time": {
                    "type": "string"
                  },
                  "created": {
                    "type": "string"
                  }
                }
              }
            ]
          }
        }
      }
    ]
  }'''

testdata: dict[str, int | str | list[str] ] = {"number": 367025, "data": "1,4,1,9,9,2,16,36,32,5,25,100,200,125,14,36,225,800,1125,504,42,49,441,2450,6125,6174,2058,132,64,784,6272,24500,43904,32928,8448,429,81,1296,14112,79380,222264,296352,171072,34749,1430", "name": "Triangle read by rows, T(n, k) = [x^k] p(n), where p(n) = (1 - hypergeom([-1/2, -n - 1, -n - 1], [1, 1], 4*x)) / (2*x).", "formula": ["T(n,k) = binomial(n+1,n-k)^2*binomial(2*k,k)/(k+1). - _Detlef Meya_, Nov 19 2023"], "example": ["Triangle T(n, k) starts:", "  [0]   1;", "  [1]   4,    1;", "  [2]   9,    9,     2;", "  [3]  16,   36,    32,      5;", "  [4]  25,  100,   200,    125,     14;", "  [5]  36,  225,   800,   1125,    504,      42;", "  [6]  49,  441,  2450,   6125,   6174,    2058,     132;", "  [7]  64,  784,  6272,  24500,  43904,   32928,    8448,    429;", "  [8]  81, 1296, 14112,  79380, 222264,  296352,  171072,  34749,   1430;", "  [9] 100, 2025, 28800, 220500, 889056, 1852200, 1900800, 868725, 143000, 4862;"], "maple": ["p := n -> (1 - hypergeom([-1/2, -n-1, -n-1], [1, 1], 4*x)) / (2*x):", "T := (n, k) -> coeff(simplify(p(n)), x, k):", "seq(seq(T(n, k), k = 0..n), n = 0..9);"], "mathematica": ["T[n_,k_]:=Binomial[n+1,n-k]^2*Binomial[2*k,k]/(k+1);Flatten[Table[T[n,k],{n,0,9},{k,0,n}]] (* _Detlef Meya_, Nov 19 2023 *)"], "xref": ["Cf. A000290 (first column), A000108 (main diagonal).", "Cf. A367022, A367023, A387024."], "keyword": "nonn,tabl", "offset": "0,2", "author": "_Peter Luschny_, Nov 07 2023", "references": 0, "revision": 14, "time": "2023-11-20T11:52:33-05:00", "created": "2023-11-07T14:43:14-05:00"}

# #@

def SeqToString(
        seq: list[int],
        maxchars: int,
        maxterms: int,
        sep: str = ' ',
        offset: int = 0
    ) -> str:
    """
    Converts a sequence of integers into a string representation.

    Args:
        seq: The sequence of integers to be converted.
        maxchars: The maximum length of the resulting string.
        maxterms: The maximum number of terms included.
        sep: String seperator. Default is ' '.
        offset: The starting index of the sequence. Defaults to 0.

    Returns:
        str: The string representation of the sequence.

    """
    seqstr = ""
    maxt = maxl = 0
    for trm in seq[offset:]:
        maxt += 1
        if maxt > maxterms:
            break
        s = str(trm) + sep
        maxl += len(s)
        if maxl > maxchars:
            break
        seqstr += s
    return seqstr


def queryOEIS(seqlist: list[int], maxnum: int = 3) -> str:
    """
    Query if a given sequence is present in the OEIS.
    The search uses seq[3:] with max string length 160.

    Args:
        seqlist: The sequence to search. Must have at least 28 terms.
        maxnum: max number of sequences to be returned. Defaults to 3.

    Returns:
        str: The A-number of the sequence if found in OEIS, otherwise an empty string.

    Raises:
        Exception: If the OEIS server cannot be reached after multiple attempts.
    """
    if len(seqlist) < 28:
        print("Sequence is too short!")
        return ""

    seqstr = SeqToString(seqlist, 140, 24, ",", 3)
    url = f"https://oeis.org/search?q={seqstr}&fmt=json"

    for _ in range(3):
        time.sleep(0.5)  # give the OEIS server some time to relax
        try:
            jdata: None | list[dict[str, int | str | list[str] ]] = get(url, timeout=20).json()
            if jdata == None:
                print("Sorry, but no match!")
                return ""

            anumber = ""
            for j in range(min(maxnum, len(jdata))):
                seq = jdata[j]
                number = seq["number"]
                anumber = f"A{(6 - len(str(number))) * '0' + str(number)}"
                print(anumber)
                name = seq["name"]
                print(name)
                data = seq["data"]
                print(data)
            return anumber

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    raise Exception(f"Could not open {url}.")

class StopWatch:
    def __init__(
        self,
        comment: str = "Elapsed time: "
    ) -> None:

        self.start_time = None
        self.text = comment

    def start(self) -> None:
        """Start a new StopWatch"""
        if self.start_time is not None:
            raise RuntimeError("Watch is running. First stop it.")
        self.start_time = time.perf_counter()

    def stop(self) -> float:
        """Stop the StopWatch, and report the elapsed time."""
        if self.start_time is None:
            raise RuntimeError("Watch is not running.")

        elapsed_time = time.perf_counter() - self.start_time
        self.start_time = None

        print(self.text.rjust(17), "{:0.4f}".format(elapsed_time), "sec")

        return elapsed_time


def QuickTiming(tabl: Table, size: int = 100) -> None:
    t = StopWatch(tabl.id)
    t.start()
    tabl.tab(size)
    t.stop()


def Benchmark(
        T: Callable[[int, int], int],
        offset: int = 4,
        size: int = 4
    ) -> list[float]:
    """Benchmark for functions computing lower triangular arrays.

    Args:
        T(n, k), function defined for n >= 0 and 0 <= k <= n.
        offset > 0, the power of two where the test starts. Defaults to 4.
        size, the length of test run. Defaults to 4.

    Returns:
        List of factors that indicate by what the computing time multiplies
        when the number of rows doubles.

    Example:
        Benchmark(lambda n, k: n**k)
    """
    B: list[float] = []
    for s in [2 << n for n in range(offset - 1, offset + size)]:
        t = StopWatch(str(s))
        t.start()
        [[T(n, k) for k in range(n + 1)] for n in range(s)]
        B.append(t.stop())
    return [B[i + 1] / B[i] for i in range(size)]


def AnumList() -> list[str]:
    bag = []
    for tab in Tables:
        for anum in tab.sim:
            bag.append(anum)  # type: ignore
    return sorted(bag)        # type: ignore


def AnumInListQ(anum: str) -> bool:
    """Is the A-number referenced in the library?

    Args:
        A-number as string.

    Returns:
        If 'True' a similar sequence is probably implemented.
    """
    return anum in AnumList()


def PreView(T: Table, size: int = 7) -> None:
    """
    Args:
        T, table to inspect
        size, number of rows, defaults to 7.

    Returns:
    None. Prints the result for some example parameters.

    """
    print()
    print("NAME       ", T.id)
    print("similars   ", T.sim)
    print("invertible ", T.invQ)
    print("value      ", T.val(size-1, (size-1)//2))
    print("row        ", T.row(size-1))
    print("col        ", T.col(2, size))
    print("sum        ", T.sum(size))
    print("diag       ", T.diag(2, size))
    print("poly       ", [T.poly(n, 1) for n in range(size)])
    print("table      ", T.tab(size))
    print("accumulated", T.acc(size))
    print("firstdiff  ", T.diff(size))
    print("reverted   ", T.rev(size))
    print("inverted   ", T.inv(size))
    print("antidiagtab", T.adtab(size))
    print("rev of inv ", T.revinv(size))
    print("inv of rev ", T.invrev(size))
    print("matrix     ", T.mat(size))
    print("flatt seq  ", T.flat(size))
    print("inv rev 11 ", T.invrev11(size-1))
    T11 = Table(T.off(1, 1), "Toffset11")
    print("1-1-based  ", T11.tab(size-1))
    print("summap     ", T.summap(lambda n: n*n, size))
    print("invmap     ", T.invmap(lambda n: n*n, size))
    print("TABLE      "); T.show(size + 2)
    print("Timing 100 rows:", end=''); QuickTiming(T)


def QuickView(prompt: bool = False) -> None:
    for T in Tables:
        print(T.id, T.sim)
        T.show(6)
        if prompt:
            input("Hit Return/Enter > ")
# print("Provides efficient implementations for:")
# print(AnumList())


if __name__ == "__main__":
    from Tables import Tables

    # print(AnumInListQ('A021009'))

    def QuickBench() -> None:
        for tabl in Tables:
            QuickTiming(tabl)  # type: ignore

    def OrderBench() -> None:
        for tabl in Tables:
            print(Benchmark(tabl))  # type: ignore

    QuickBench()
    print(f"\n{len(Tables)} tables tested!\n")

    def test() -> None:
        print()
        queryOEIS([1, 4, 1, 9, 9, 2, 16, 36])
        print()
        queryOEIS([1,4,1,9,9,2,16,36,32,5,25,100,200,125,14,36,225,800,1125,504,42,49,441,2450,6125,6174,2058,132,64,784,6272,24500])
        print()
        queryOEIS([9991, 2, 48323, 4, 0,9991, 2, 48323, 4, 0,9991, 2, 48323, 4, 0,9991, 2, 48323, 4, 0,9991, 2, 48323, 4, 0,9991, 2, 48323, 4, 0,9991, 2, 48323, 4, 0])
        print()
        queryOEIS([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45])