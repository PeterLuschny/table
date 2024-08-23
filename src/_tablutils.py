from _tabltypes import Table
import time

# #@

def PreView(T:Table, size: int = 6) -> None:
    """
    Args:
        T, table to inspect
        size, number of rows, defaults to 6.

    Returns:
    None. Prints the result for some example parameters.

    """
    print()
    print("NAME       ", T.id)
    print("similars   ", T.sim)
    print("invertible ", T.invQ)
    print("table      ", T.tab(size))
    print("value      ", T.val(size-1, (size-1)//2))
    print("row        ", T.row(size-1))
    print("col        ", T.col(2, size))
    print("diag       ", T.diag(2, size))
    print("poly       ", [T.poly(n, 1) for n in range(size)])
    print("antidiagtab", T.adtab(size))
    print("accumulated", T.acc(size))
    print("inverted   ", T.inv(size))
    print("reverted   ", T.rev(size))
    print("rev of inv ", T.revinv(size))
    print("inv of rev ", T.invrev(size))
    print("matrix     ", T.mat(size))
    print("flatt seq  ", T.flat(size))
    print("inv rev 11 ", T.invrev11(size-1))
    T11 = Table(T.off(1, 1), "Toffset11")
    print("1-1-based  ", T11.tab(size-1))
    print("summap     ", T.summap(lambda n: n*n, size))  
    print("invmap     ", T.invmap(lambda n: n*n, size))  


def SeqToString(seq: list[int], maxchars: int, maxterms: int, sep: str=' ', offset: int=0) -> str:
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

class Timer:
    def __init__(
        self,
        comment: str
    ) -> None:
        self.start_time = None
        self.text = comment

    def start(self) -> None:
        """Start a new timer"""
        if self.start_time is not None:
            raise RuntimeError("Timer is running. First stop it.")
        self.start_time = time.perf_counter()

    def stop(self) -> float:
        """Stop the timer, and report the elapsed time"""
        if self.start_time is None:
            raise RuntimeError("Timer is not running.")

        elapsed_time = time.perf_counter() - self.start_time
        self.start_time = None

        print(self.text.rjust(16), "{:0.4f}".format(elapsed_time), "sec")

        return elapsed_time


def Benchmark(tabl: Table, size: int = 100) -> None:
    t = Timer(tabl.id)
    t.start()
    tabl.tab(size)
    t.stop()


if __name__ == "__main__":
    from Tables import Tables

    for tabl in Tables: 
        Benchmark(tabl) # type: ignore
