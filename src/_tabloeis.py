from _tablutils import SeqToString
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

# With CC BY-SA 4.0 from:
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring
def lcsubstr(s: str, t: str) -> tuple[int, int]: 
    """
    The longest common substring of s and t that is contiguous.

    Returns:
        (s, l): The matched substring starts at 's' and has lenght 'l'.
    """
    m = [[0] * (1 + len(t)) for _ in range(1 + len(s))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s)):
        for y in range(1, 1 + len(t)):
            if s[x - 1] == t[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    # lcs_str =  s[x_longest - longest : x_longest] 
    return (x_longest - longest, longest)

def QueryOEIS(
        seqlist: list[int], 
        maxnum: int = 3
    ) -> str:
    """
    Query if a given sequence is present in the OEIS.
    The search uses seqlist[3:] with max string length 160.

    Args:
        seqlist: The sequence to search. Must have at least 28 terms.
        maxnum: max number of sequences to be returned. Defaults to 3.

    Returns:
        str: The A-number of the sequence if found in OEIS, otherwise an empty string.

    Raises:
        Exception: If the OEIS server cannot be reached after multiple attempts.
    """
    minlen = 20
    if len(seqlist) < minlen:
        print("Sequence is too short! We require at least {minlen} terms.")
        return ""

    seqstr = SeqToString(seqlist, 140, 24, ",", 0)
    url = f"https://oeis.org/search?q={seqstr}&fmt=json"

    for _ in range(3):
        time.sleep(0.5)  # give the OEIS server some time to relax
        try:
            jdata: None | list[dict[str, int | str | list[str] ]] = get(url, timeout=20).json()
            if jdata == None:
                print("You looked for:", seqstr)
                print("Sorry, no match found!")
                return ""

            anumber = ""
            for j in range(min(maxnum, len(jdata))):
                seq = jdata[j]
                number = seq["number"]
                anumber = f"A{(6 - len(str(number))) * '0' + str(number)}"
                name = seq["name"]
                print(anumber, name)
                data = seq["data"]
                start, length = lcsubstr(data, seqstr)     # type: ignore
                c = data.count(",", start, start + length) # type: ignore
                print(f"There are {c} consecutive terms matching the search data.")
                print(f"The matched substring starts at {start} and has length {length}.")
                print(data)
            return anumber

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    raise Exception(f"Could not open {url}.")


if __name__ == "__main__":
    from Tables import Tables

    def test() -> None:
        print()
        QueryOEIS([1, 4, 1, 9, 9, 2, 16, 36])
        print()
        QueryOEIS([36,32,5,25,100,200,125,14,36,225,800,1125,504,
                   42,49,441,2450,6125,6174,2058,132,64,784,6272])
        print()
        QueryOEIS([9991,2,48323,4,0,9991,2,48323,4,0,9991,2,48323,4,0,9991,2, 
                   48323,4,0,9991,2,48323,4,0,9991,2,48323,4,0,9991,2,48323])
        print()
        QueryOEIS([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,17,19,20,21,22,23]) 


    def testQuery() -> None:
        for tabl in Tables[:5]:
            print("\nRow sums of:", tabl.id, tabl.sim)
            sumlist = tabl.sum(30)
            QueryOEIS(sumlist)

    test()
    testQuery()
