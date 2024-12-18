from functools import cache
from _tabltypes import Table

"""Bell (Peirce/Aitken) triangle, (see also A182930).

[0]     1;
[1]     1,     2;
[2]     2,     3,     5;
[3]     5,     7,    10,    15;
[4]    15,    20,    27,    37,    52;
[5]    52,    67,    87,   114,   151,   203;
[6]   203,   255,   322,   409,   523,   674,   877;
[7]   877,  1080,  1335,  1657,  2066,  2589,  3263,  4140;
[8]  4140,  5017,  6097,  7432,  9089, 11155, 13744, 17007, 21147;
[9] 21147, 25287, 30304, 36401, 43833, 52922, 64077, 77821, 94828, 115975;
"""


@cache
def bell(n: int) -> list[int]:
    if n == 0:
        return [1]

    row = [bell(n - 1)[n - 1]] + bell(n - 1)
    for k in range(1, n + 1):
        row[k] += row[k - 1]
    return row


Bell = Table(
    bell, 
    "Bell", 
    ["A011971", "A011972", "A123346"], 
    "",
    r"\sum_{j=0}^{k} \binom{k}{j} Bell(n - k + j)"
)

# No inverse!

if __name__ == "__main__":
    from _tablutils import PreView

    PreView(Bell)
