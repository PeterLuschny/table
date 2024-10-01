from typing import Dict
from more_itertools import flatten
from _tabltypes import Table
from _tabloeis import QueryOEIS

# #@

def AnumbersDict(T: Table) -> Dict[str, tuple[int, int, int]]:
    """The profile of integer triangles in the OEIS."""

    anum: Dict[str, tuple[int, int, int]] = {} 

    # flat (size: int)     -> list[int] | flattened form of the first size rows
    anum[T.id] = QueryOEIS(T.flat(7))

    # inv (size: int)      -> tabl | inverse table
    anum["inv"] = QueryOEIS(list(flatten(T.inv(7))))

    # revinv (size: int)   -> tabl | row reversed inverse
    anum["revinv"] = QueryOEIS(list(flatten(T.revinv(7))))

    # invrev (size: int)   -> tabl | inverse of row reversed
    anum["invrev"] = QueryOEIS(list(flatten(T.invrev(7))))

    # off (N: int, K: int) -> rgen | new offset (N, K)
    T11 = Table(T.off(1, 1), T.id + "off11")
    anum["off1"] = QueryOEIS(T11.flat(7))

    # invrev11 (size: int) -> tabl | invrev from offset (1, 1)
    InvT11 = Table(T.off(1, 1), T.id + "ioff11")
    anum["ioff1"] = QueryOEIS(InvT11.flat(7))

    # antid (size: int)    -> tabl | table of (upward) anti-diagonals
    ##self.prof["antid"] = QueryOEIS(list(flatten(self.tab.antid(7))))

    return anum

OEISDict: Dict[str, Dict[str, tuple[int, int, int]]] = {} 


if __name__ == "__main__":
    from Tables import Tables

    for i in range(63, 65): 
        T = Tables[i]  # type: ignore
        OEISDict[T.id] = AnumbersDict(T) # type: ignore

    for tabl, dict in OEISDict.items():
        print("*** Table", tabl, "***")
        for trait in dict:
            print('   ', trait, '->', dict[trait])
