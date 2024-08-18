import time

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
