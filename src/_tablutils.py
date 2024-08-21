from _tabltypes import Table
import time

# #@

def PreView(T:Table, size: int = 6) -> None:
    """
    Args:
        T, table to inspect
        size, number of rows, defaults to 6.
    """
    print()
    print("name       ", T.id)
    print("similars   ", T.sim)
    print("invertible ", T.invQ)
    print("table      ", T.tab(size))
    print("value      ", T.val(size-1, (size-1)//2))
    print("row        ", T.row(size-1))
    print("col        ", T.col(2, size))
    print("diag       ", T.diag(2, size))
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

if __name__ == "__main__":
    from Tables import Table, Tables
        
    def benchmark(tabl: Table) -> None:
        t = Timer(tabl.id)
        t.start()
        tabl.tab(100)
        t.stop()


    for tabl in Tables: 
        benchmark(tabl)
