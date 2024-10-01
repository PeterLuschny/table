from typing import Dict
from more_itertools import flatten
from _tabltypes import Table
from _tabloeis import QueryOEIS   

# #@


class Profile:
    """The profile of integer triangles."""
    def __init__(
            self,
            tab : Table,
        ) -> None:

        self.tab = tab
        self.prof: Dict[str, tuple[int,int,int]] = {} 

    def profile(self) -> Dict[str, tuple[int, int, int]]:
        # flat (size: int)     -> list[int] | flattened form of the first size rows
        self.prof[self.tab.id] = QueryOEIS(self.tab.flat(7))

        # sum (size: int)      -> list[int] | sums of the first size rows
        ##self.prof["sum"] = QueryOEIS(self.tab.sum(25))

        # diag(n, size: int)   -> list[int] | diagonal starting at the left side    
        self.prof["diag0"] = QueryOEIS(self.tab.diag(0, 25))
        self.prof["diag1"] = QueryOEIS(self.tab.diag(1, 25))
        self.prof["diag2"] = QueryOEIS(self.tab.diag(2, 25))

        # col (k, size: int)   -> list[int] | k-th column starting at the main diagonal
        self.prof["col0"] = QueryOEIS(self.tab.col(0, 25))
        self.prof["col1"] = QueryOEIS(self.tab.col(1, 25))
        self.prof["col2"] = QueryOEIS(self.tab.col(2, 25))

        # rev (size: int)      -> tabl | table with reversed rows
        ##self.prof["rev"] = QueryOEIS(list(flatten(self.tab.rev(7))))

        # acc (size: int)      -> tabl | table with rows accumulated
        ##self.prof["acc"] = QueryOEIS(list(flatten(self.tab.acc(7))))

        # diff (size: int)     -> tabl | table with first difference of rows
        ##self.prof["diff"] = QueryOEIS(list(flatten(self.tab.diff(7))))

        # inv (size: int)      -> tabl | inverse table
        self.prof["inv"] = QueryOEIS(list(flatten(self.tab.inv(7))))

        # revinv (size: int)   -> tabl | row reversed inverse
        self.prof["revinv"] = QueryOEIS(list(flatten(self.tab.revinv(7))))

        # invrev (size: int)   -> tabl | inverse of row reversed
        self.prof["invrev"] = QueryOEIS(list(flatten(self.tab.invrev(7))))

        # off (N: int, K: int) -> rgen | new offset (N, K)
        T11 = Table(self.tab.off(1, 1), self.tab.id + "off11")
        self.prof["off1"] = QueryOEIS(T11.flat(7))

        # invrev11 (size: int) -> tabl | invrev from offset (1, 1)
        InvT11 = Table(self.tab.off(1, 1), self.tab.id + "ioff11")
        self.prof["ioff1"] = QueryOEIS(InvT11.flat(7))

        # adtab (size: int)    -> tabl | table of (upward) anti-diagonals
        ##self.prof["antid"] = QueryOEIS(list(flatten(self.tab.antid(7))))

        # print(self.prof)
        return self.prof


ProfileDict: Dict[str, Dict[str, tuple[int,int,int]]] = {} 

if __name__ == "__main__":
    from Tables import Tables
    
    def padd(t: Table) -> None:
        P = Profile(t) 
        ProfileDict[t.id] = P.profile()

    for i in range(56, 58): 
        padd(Tables[i])  # type: ignore

    for tabl, dict in ProfileDict.items():
        print("*** Table", tabl, "***")
        for trait in dict:
            print('   ', trait, '->', dict[trait])
