from functools import cache
from Binomial import Binomial
from _tabltypes import Table

"""Labeled graphs.

[0] 1;
[1] 0,       1;
[2] 0,       1,      1;
[3] 0,       2,      2,     4;
[4] 0,       8,      6,    12,    38;
[5] 0,      64,     32,    48,   152,    728;
[6] 0,    1024,    320,   320,   760,   3640,   26704;
[7] 0,   32768,   6144,  3840,  6080,  21840,  160224,  1866256;
"""


@cache
def labeledgraphs(n: int) -> list[int]:
    if n == 0:
        return [1]

    s = [
        2 ** (((k - n + 1) * (k - n)) // 2)
        * Binomial.val(n - 1, k - 1)
        * labeledgraphs(k)[k]
        for k in range(1, n)
    ]
    b = 2 ** (((n - 1) * n) // 2) - sum(s)

    return [0] + s + [b]


LabeledGraphs = Table(
    labeledgraphs,
    "LabeledGraphs",
    ["A360603"],
    "",
    r"2^{\binom{n-k}{2}} \binom{n-1}{k-1} \text{A001187}(k)",
)


if __name__ == "__main__":
    from _tablutils import PreView

    PreView(LabeledGraphs)
