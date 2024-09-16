from _tabltypes import Table
from typing import Callable
import time

# #@

def SeqToString(seq: list[int], 
                maxchars: int, 
                maxterms: int, 
                sep: str=' ', 
                offset: int=0
    ) -> str:
    """
    Converts a sequence of integers into a string representation.

    Args:
        seq (list[int]): The sequence of integers to be converted.
        maxchars (int): The maximum length of the resulting string.
        maxterms (int): The maximum number of terms included.
        sep (string, optional): String seperator. Default is ' '.
        offset (int, optional): The starting index of the sequence. Defaults to 0.

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


def Benchmark(T: Callable[[int, int], int], 
              offset:int = 4, 
              size:int = 4
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
            bag.append(anum) # type: ignore
    return sorted(bag)       # type: ignore


def AnumInListQ(anum: str) -> bool:
    """Is the A-number referenced in the library?

    Args:
        A-number as string.
 
    Returns:
        If 'True' a similar sequence is probably implemented.
    """
    return anum in AnumList()


def PreView(T:Table, size: int = 7) -> None:
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
            print(Benchmark(tabl)) # type: ignore

    QuickBench()
    print(f"\n{len(Tables)} tables tested!\n")
