from typing import Callable

# #@


def InvertMatrix(L: list[list[int]], check: bool = True) -> list[list[int]]:
    """
    Calculates the inverse of a lower triangular matrix.

    Args:
        The lower triangular matrix to be inverted.

        Check whether the inverse exists as an integer matrix, default is True.

    Returns:
        The integer inverse of the lower triangular matrix if it exists.

        []: If the inverse does not exist.

    """
    n = len(L)
    inv = [[0 for _ in range(n)] for _ in range(n)]  # Identity matrix
    for i in range(n):
        inv[i][i] = 1

    for k in range(n):
        for j in range(n):
            for i in range(k):
                inv[k][j] -= inv[i][j] * L[k][i]
            if check:
                a = inv[k][j]
                b = L[k][k]
                if b == 0:
# print("Warning: Inverse does not exist!")
# raise ValueError("Inverse does not exist!")
                    return []
                a, r = divmod(a, b)  # make sure that a is integer
                if r != 0:
# print("Warning: Integer terms do not exist!")
# raise ValueError("Integer inverse does not exist!")
                    return []
    return [row[0:n + 1] for n, row in enumerate(inv)]


def InvertTriangle(r: Callable[[int], list[int]], dim: int) -> list[list[int]]:
    M = [[r(n)[k] for k in range(n + 1)] for n in range(dim)]
    return InvertMatrix(M, True)


def convtriangle(
        seq: Callable[[int], int], 
        dim: int = 10
    ) -> list[list[int]]:
    """Sometimes called the partition transform of seq.
    See A357368 for more information and some examples.

    Args:
        seq, sequence to be convoluted
        dim, the size of the triangle

    Returns:
        The convolution triangle of seq.
    """
    A = [seq(i) for i in range(1, dim)]  # Cache the input sequence.
    # print("In:", A)
    C = [[0 for _ in range(m + 1)] for m in range(dim)]
    C[0][0] = 1
    for m in range(1, dim):
        C[m][m] = C[m - 1][m - 1] * A[0]
        for k in range(m - 1, 0, -1):
            C[m][k] = sum(A[i] * C[m - i - 1][k - 1] 
                          for i in range(m - k + 1))
    return C


def ConvTriangle(
        T: Callable[[int, int], int],
        seq: Callable[[int], int],
        dim: int = 10
    ) -> list[list[int]]:

    A = [seq(i) for i in range(1, dim)]  # Cache the input sequence.
    # print("In:", A)
    C = [[0 for _ in range(m + 1)] for m in range(dim)]
    C[0][0] = 1
    for m in range(1, dim):
        C[m][m] = T(m - 1, m - 1) * A[0]
        for k in range(m - 1, 0, -1):
            C[m][k] = sum(A[i] * T(m - i - 1, k - 1)
                          for i in range(m - k + 1))
    return C


if __name__ == "__main__":

    def test() -> None:
        m = [[1, 0, 0], [1, 2, 0], [1, 2, 3]]
        v = InvertMatrix(m)
        print(m)
        print("Inverse:", v)

        m = [[1, 0, 0], [1, 2, 0], [1, 2, 0]]
        v = InvertMatrix(m)
        print(m)
        print("Inverse:", v)
        print()

        m = [
            [1,      0,      0,     0,    0,   0,  0, 0],
            [0,      1,      0,     0,    0,   0,  0, 0],
            [0,      2,      1,     0,    0,   0,  0, 0],
            [0,      9,      6,     1,    0,   0,  0, 0],
            [0,     64,     48,    12,    1,   0,  0, 0],
            [0,    625,    500,   150,   20,   1,  0, 0],
            [0,   7776,   6480,  2160,  360,  30,  1, 0],
            [0, 117649, 100842, 36015, 6860, 735, 42, 1],
        ]
        v = InvertMatrix(m, False)
        print(v)

    test()

    from Abel import Abel
    from Bell import Bell
    from StirlingSet import StirlingSet

    dim = 8
    print(InvertMatrix(Abel.tab(dim)))
    print(InvertTriangle(Abel.gen, dim))
    print()
    print(InvertMatrix(StirlingSet.tab(dim)))
    print(InvertTriangle(StirlingSet.gen, dim))
    print()
    print(InvertMatrix(Bell.tab(dim)))
    print(InvertTriangle(Bell.gen, dim))
