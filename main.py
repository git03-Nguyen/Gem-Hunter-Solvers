from itertools import combinations

# ---------------------------------------------
# Đọc ma trận và ktra input từ file, với None đại diện cho ô chưa biết (tức ô có thể là bẫy hoặc là ngọc)
def input_matrix(file_name = "input.txt"):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        matrix = []
        for line in lines:
            row = []
            for x in line.split(","):
                x = x.strip()
                if x == "_":
                    row.append(None)
                elif x == "T":
                    row.append("T")
                elif x == "G":
                    row.append("G")
                elif x.isnumeric():
                    x = int(x)
                    if x < 0 or x > 8: raise ValueError("Invalid input")
                    row.append(int(x))
                else:
                    raise ValueError("Invalid input")
            matrix.append(row)
        return matrix

# Ghi ma trận kết quả ra file 
def output_matrix(matrix, file_name = "output.txt"):
    with open(file_name, 'w') as f:
        for row in matrix:
            f.write(", ".join([str(x) if x is not None else "_" for x in row]) + "\n")
    
# ---------------------------------------------
# Mở rộng ma trận bằng cách thêm padding xung quanh (để dễ xử lý các ô ở biên)
def padding(matrix):
    '''
        Add padding to the matrix, i.e: 
                                    * * * * *
            1 2 3                   * 1 2 3 *
            4 5 6   will become     * 4 5 6 *
            7 8 9                   * 7 8 9 *
                                    * * * * *
    '''
    char = "*"
    m = len(matrix[0])
    padded = [[char for _ in range(m + 2)]]
    for row in matrix:
        padded.append([char] + row + [char])
    padded.append([char for _ in range(m + 2)])
    return padded

# Xoá padding của ma trận
def unpadding(matrix):
    return [row[1:-1] for row in matrix[1:-1]]

# Lấy các ô xung quanh ô pos mà có điều kiện là 1 lambda function, mặc định không có điều kiện
def get_around(matrix, pos, condition = None):
    [r, c] = pos
    around = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if condition(matrix[r + i][c + j]) or condition is None:
                around.append([r + i, c + j])
    return around

# Chuyển từ vị trí (r, c) trong ma trận 2 chiều thành vị trí trong ma trận 1 chiều
def to_1D(pos, size):
    num_r, num_c = size
    r, c = pos
    return (r*num_c + c + 1)

# Chuyển từ vị trí trong ma trận 1 chiều thành vị trí trong ma trận 2 chiều
def to_2D(flat, size):
    signed = 1 if flat > 0 else -1
    num_r, num_c = size
    flat = abs(flat) - 1
    r = flat // num_c
    c = flat % num_c
    return [r, c], signed

# Lấy tất cả các tập con k phần tử của một tập hợp
def subsets_of(arr, k):
    arr = list(set(arr))
    arr.sort()
    subsets = [list(x) for x in combinations(arr, k)]
    return subsets

# ---------------------------------------------
# "Có ít nhất một ..." <=> A OR B OR C OR ...
# ---------------------------------------------

# "Có chính xác k ô bẫy trong n ô" <=> "Có nhiều nhất k ô bẫy trong n ô" AND "Có ít nhất k ô bẫy trong n ô"
# Số lượng mệnh đề = |exactly(n, k)| = |at_most(n, k)| + |at_least(n, k)| = C(n, k+1) + C(n, n−k+1) => Tăng rất nhanh
# => Chỉ dùng cho bài toán nhỏ, như Gem Hunter (n <= 8 nên lớn nhất là exactly(8, 4) = 112, tạm chấp nhận được)
def exactly(cells, k):

    # "Có nhiều nhất k ô bẫy trong n ô" <=> "Với mỗi k + 1 ô trong n ô, có ít nhất một ô KHÔNG phải bẫy"
    at_most = subsets_of(cells, k + 1)
    at_most = [[-x for x in subset] for subset in at_most]

    # "Có ít nhất k ô bẫy trong n ô" <=> "Với mỗi n - (k - 1) ô trong n ô, có ít nhất một ô bẫy"
    n = len(cells)
    at_least = subsets_of(cells, n - k + 1)

    return at_most + at_least

# ---------------------------------------------
# Lấy tất cả các câu mệnh đề từ ma trận Gem Hunter dưới dạng CNF
def get_CNF_clauses(matrix):

    clauses = []
    matrix = padding(matrix)

    n_rows = len(matrix)
    n_cols = len(matrix[0])

    # Di chuyển qua từng ô chứa số đếm 
    # Với mỗi ô bẫy "T" sẵn xung quanh, trừ số của ô đó đi 1
    # Tạo mệnh đề CNF cho mỗi ô chứa số đếm
    for i in range(1, n_rows - 1):
        for j in range(1, n_cols - 1):
            if type(matrix[i][j]) == int:
                
                traps = get_around(matrix, [i, j], lambda x: x == "T")              # Những ô bẫy "T" xung quanh ô đó
                matrix[i][j] -= len(traps)                                          # Trừ đi số lượng bẫy "T" xung quanh ô đó

                unknowns = get_around(matrix, [i, j], lambda x: x is None)          # Những ô chưa biết xung quanh ô đó       
                print(f"Unknowns for [{i}, {j}]: {unknowns}") 
                unknowns = [to_1D(pos, [n_rows - 2, n_cols - 2]) for pos in unknowns]       # Chuyển vị trí 2D sang 1D
                
                clauses += exactly(unknowns, matrix[i][j])                          # Thêm CNF vào KB: "Có đúng matrix[i][j] ô bẫy trong unknowns"

    # Xoá các mệnh đề trùng lặp và sắp xếp theo độ dài câu mệnh đề
    clauses = set([tuple(clause) for clause in clauses])
    clauses = [list(clause) for clause in clauses]
    clauses.sort(key=lambda x: (len(x), x))
    return clauses

# ---------------------------------------------
# ---------------------------------------------
# Giải quyết bài toán Gem Hunter bằng cách sử dụng thư viện PySAT
# PySAT: https://pysathq.github.io/docs/html/index.html
def solve_by_pysat(KB):
        
    from pysat.formula import CNF
    from pysat.solvers import Solver

    # create a satisfiable CNF formula "(-x1 ∨ x2) ∧ (-x1 ∨ -x2)":
    cnf = CNF(from_clauses=KB)

    # create a SAT solver for this formula:
    with Solver(bootstrap_with=cnf) as solver:
        # 1.1 call the solver for this formula:
        print('formula is', f'{"s" if solver.solve() else "uns"}atisfiable')

        # 1.2 the formula is satisfiable and so has a model:
        print('and the model is:', solver.get_model())

        # 2.1 apply the MiniSat-like assumption interface:
        print('formula is',
            f'{"s" if solver.solve(assumptions=[1, 2]) else "uns"}atisfiable',
            'assuming x1 and x2')

        # 2.2 the formula is unsatisfiable,
        # i.e. an unsatisfiable core can be extracted:
        print('and the unsatisfiable core is:', solver.get_core())






# ---------------------------------------------
# --------- Main Program of test.py -----------
# ---------------------------------------------
if __name__ == "__main__":

    matrix = input_matrix()
    print(f"Input matrix:\n {matrix}\n")

    KB = get_CNF_clauses(matrix)
    print(f"KB ({len(KB)}):\n {KB}")

    print("\nSolving...\n")
    result = solve_by_pysat(KB)
    # print(result)

    # if result is not None:
    #     result = [to_2D(flat, [len(matrix), len(matrix[0])]) for flat in result]
    #     for pos, sign in result:
    #         [r, c] = pos
    #         if r >= 0 and r < len(matrix) and c >= 0 and c < len(matrix[0]):
    #             matrix[r-1][c-1] = "T" if sign == 1 else "G"
    # else:
    #     print("No solution")

    # print(f"\nOutput matrix:\n {matrix}\n")





