from _tabltypes import Table
from Binomial import Binomial
from Moebius import Moebius

def binom(n:int, k: int) -> int: return Binomial.val(n,k)

class TableTest:
    """Provides basic methods for manipulating integer triangles."""
    def __init__(
            self,
            tab: Table,
            size: int
        ) -> None:
        self.tab = tab
        self.size = size
 
    def T(self, n:int, k:int) -> int: return self.tab.val(n, k)
    def Tinv(self, n:int, k:int) -> int: return self.tab.val(n, k) 
     
    def test(self, fun: str = "pp") -> list[int]:
        l: list[int] = []

        match fun:
            case r"\(T_{n, k}\)":
                l = [self.T(n, k) 
                     for n in range(self.size) for k in range(n+1)]
            case r"\(T^{-1}_{n, k}\)":
                l = [self.Tinv(n, k) 
                     for n in range(self.size) for k in range(n+1)]
            case r"\(T_{n, n - k}\)":
                l = [self.T(n, n-k) 
                     for n in range(self.size) for k in range(n+1)]
            case r"\(T^{-1}_{n, n - k}\)":
                l = [self.Tinv(n, n-k) 
                     for n in range(self.size) for k in range(n+1)]
            case r"\((T_{n, n - k})^{-1}\)":
                l = []
            case r"\(T_{n + 1, k + 1} \)":
                l = [self.T(n+1, k+1) 
                     for n in range(self.size) for k in range(n+1)]
            case r"\(T_{n + 1, n - k + 1} \)":
                l = [self.T(n+1, n-k + 1) 
                     for n in range(self.size) for k in range(n+1)]
            case r"\(T^{-1}_{n + 1, k + 1}\)":
                l = [self.Tinv(n+1, k + 1) 
                     for n in range(self.size) for k in range(n+1)]
            case r"\(T^{-1}_{n + 1, n - k + 1}\)":
                l = [self.Tinv(n+1, n-k + 1) 
                     for n in range(self.size) for k in range(n+1)]
            case r"\((T_{n + 1, n - k + 1})^{-1}\)":
                l = []
            case r"\(T_{n - k, k} \ \ (k \le n/2)\)":
                l = [self.T(n - k, k) 
                     for n in range(self.size) for k in range(n//2)]
            case r"\(\sum_{j=0}^{k} T_{n, j}\)":
                l = [self.T.acc(n) for n in range(self.size)]
            case r"\(T_{n, k}\ (-1)^{k}\)":
                l = [self.T.alt(n) for n in range(self.size)]
            case r"\(T_{n + 1, k + 1}\ (k + 1) \)":
                l = [self.T(n + 1, k + 1)*(k + 1) 
                     for n in range(self.size) for k in range(n+1)]
            case r"\(T_{n    , 0}\)":
                l = []
            case r"\(T_{n + 1, 1}\)":
                l = []
            case r"\(T_{n + 2, 2}\)":
                l = []
            case r"\(T_{n + 3, 3}\)":
                l = []
            case r"\(T_{n    , n}\)":
                l = []
            case r"\(T_{n + 1, n}\)":
                l = []
            case r"\(T_{n + 2, n}\)":
                l = []
            case r"\(T_{n + 3, n}\)":
                l = []
            case r"\(\text{lcm}_{k=0}^{n}\ | T_{n, k} |\ \  (T_{n,k}>1)\)":
                l = []
            case r"\(\text{gcd}_{k=0}^{n}\ | T_{n, k} |\ \  (T_{n,k}>1)\)":
                l = []
            case r"\(\text{max}_{k=0}^{n}\ | T_{n, k} |\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, k}\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, k}\  [2 | k]\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, k}\  (1 - [2 | k])\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, k}\  (-1)^{k}\)":
                l = []
            case r"\(\sum_{k=0}^{n} | T_{n, k} |\)":
                l = []
            case r"\(\sum_{k=0}^{n} \sum_{j=0}^{k} T_{n, j}\)":
                l = []
            case r"\(\sum_{k=0}^{n} \sum_{j=0}^{k} T_{n, n - j}\)":
                l = []
            case r"\(\sum_{k=0}^{n/2} T_{n - k, k}\)":
                l = []
            case r"\(T_{n, n / 2}\)":
                l = []
            case r"\(T_{2 n, n}\)":
                l = []
            case r"\(T_{2 n + 1, n}\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, k} \ 2^{n - k} \)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, k} \ (-2)^{n - k} \)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, k} \ k\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, k} \ (k + 1)\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, k} \ k^{2}\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, k} \ \binom{n}{k} \)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, k} \ (-1)^{n - k} \ \binom{n}{k} \)":
                l = []
            case r"\(\sum_{k=0}^{1} T_{1, k}\  n^k\)":
                l = []
            case r"\(\sum_{k=0}^{2} T_{2, k}\  n^k\)":
                l = []
            case r"\(\sum_{k=0}^{3} T_{3, k}\  n^k\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, k}\  2^k\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, k}\  3^k\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, k}\  n^k\)":
                l = [sum(self.T(n, k) * n**k 
                    for k in range(n + 1)) for n in range(self.size)]
            case r"\(T^{-1}_{n, n-k}\)":
                l = []
            case r"\(T^{-1}_{n, n-k}\)":
                l = []
            case r"\(T_{n + 1, n-k} \)":
                l = []
            case r"\(T_{n + 1, n-k} \)":
                l = []
            case r"\(T^{-1}_{n + 1, n-k}\)":
                l = []
            case r"\(T^{-1}_{n + 1, n-k}\)":
                l = []
            case r"\((T_{n + 1, n-k + 1})^{-1}\)":
                l = []
            case r"\(T_{n - k, n - 2k} \ \ (k \le n/2)\)":
                l = []
            case r"\(\sum_{j=0}^{n-k} T_{n, n-j}\)":
                l = []
            case r"\(T_{n, n-k}\ (-1)^{n-k}\)":
                l = []
            case r"\(T_{n + 1, n-k}\ (n-k + 1) \)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, n-k}\  [2 | k]\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, n-k}\  (1 - [2 | k])\)":
                l = []
            case r"\(\sum_{k=0}^{n} \sum_{j=0}^{k} T_{n, n - j}\)":
                l = []
            case r"\(\sum_{k=0}^{n/2} T_{n - k, n-k}\)":
                l = []
            case r"\(T_{n, n / 2}\)":
                l = []
            case r"\(T_{2 n + 1, n}\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, n-k}\ (-2)^{n - k} \)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, n-k}\ k\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, n-k}\ (k + 1)\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, n-k}\ k^{2}\)":
                l = []
            case r"\(\sum_{k=0}^{1} T_{1, n-k}\  n^k\)":
                l = []
            case r"\(\sum_{k=0}^{2} T_{2, n-k}\  n^k\)":
                l = []
            case r"\(\sum_{k=0}^{3} T_{3, n-k}\  n^k\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, n-k}\  3^k\)":
                l = []
            case r"\(\sum_{k=0}^{n} T_{n, n-k}\  n^k\)":
                l = [sum(self.T(n, n-k) * n**k 
                    for k in range(n+1)) for n in range(self.size)]
            case _:
                print("That's not a valid function.")

        return l

    #print([sum(T(n, k)*(n**k) for k in range(n+1)) for n in range(9)])
    #print([sum(Trev(n, k)*(n**k) for k in range(n+1)) for n in range(9)])
    #print([sum(T(n, n-k)*(n**k) for k in range(n+1)) for n in range(9)])

if __name__ == "__main__":
    
    t = TableTest(Moebius, 9)

    print(t.test(r"\(\sum_{k=0}^{n} T_{n, k}\  n^k\)"))
    print(t.test(r"\(\sum_{k=0}^{n} T_{n, n-k}\  n^k\)"))