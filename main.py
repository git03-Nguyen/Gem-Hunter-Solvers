from itertools import combinations

# ---------------------------------------------
# Đọc ma trân từ file, với None đại diện cho ô chưa biết (tức ô có thể là bẫy hoặc là ngọc)
def input_matrix(file_name = "input.txt"):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        matrix = []
        for line in lines:
            matrix.append([int(x) if x.strip() != "_" else None for x in line.split(",")])
        return matrix

# Ghi ma trận kết quả ra file 
def output_matrix(matrix, file_name = "output.txt"):
    with open(file_name, 'w') as f:
        for row in matrix:
            f.write(", ".join([str(x) if x is not None else "_" for x in row]) + "\n")
    
# ---------------------------------------------
# Mở rộng ma trận bằng cách thêm padding xung quanh (để dễ xử lý các ô ở biên)
def padding(matrix, char = "G"):
    '''
        Add padding to the matrix, i.e: 
                                    G G G G G
            1 2 3                   G 1 2 3 G
            4 5 6   will become     G 4 5 6 G
            7 8 9                   G 7 8 9 G
                                    G G G G G
    '''
    # Bởi vì None đại diện cho ô chưa biết, nên padding character không thể là None
    if char is None: raise ValueError("Padding character mustn't be None")

    m = len(matrix[0])
    padded = [[char for _ in range(m + 2)]]
    for row in matrix:
        padded.append([char] + row + [char])
    padded.append([char for _ in range(m + 2)])
    return padded

# Xoá padding của ma trận
def unpadding(matrix):
    return [row[1:-1] for row in matrix[1:-1]]

# Lấy các ô xung quanh ô pos mà chưa biết (tức là các ô None)
def get_None_around(matrix, pos):
    [r, c] = pos
    around = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if matrix[r + i][c + j] is None:
                around.append([r + i, c + j])
    return around

# Chuyển từ vị trí (r, c) trong ma trận 2 chiều thành vị trí trong ma trận 1 chiều
def to_1D(pos, size):
    num_r, num_c = size
    r, c = pos
    return (r*num_c + c + 1)

# Chuyển từ vị trí trong ma trận 1 chiều thành vị trí trong ma trận 2 chiều
def to_2D(flat, size):
    num_r, num_c = size
    c = (flat-1) % num_c
    r = (flat-1) // num_c
    return r,c

# Lấy tất cả các tập con k phần tử của một tập hợp
def subsets_of(arr, k):
    arr = list(set(arr))
    arr.sort()
    subsets = [list(x) for x in combinations(arr, k)]
    return subsets

# ---------------------------------------------
# "Có ít nhất một ..." <=> A OR B OR C OR ...

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

    # Di chuyển qua từng ô chứa số và thêm các mệnh đề CNF tương ứng vào KB
    for i in range(1, n_rows - 1):
        for j in range(1, n_cols - 1):
            if matrix[i][j] is not None:
                unknowns = get_None_around(matrix, [i, j])
                unknowns = [to_1D(pos, [n_rows, n_cols]) for pos in unknowns]
                clauses += exactly(unknowns, matrix[i][j])

    # Xoá các mệnh đề trùng lặp
    clauses = set([tuple(clause) for clause in clauses])
    clauses = [list(clause) for clause in clauses]
    clauses.sort(key=lambda x: (len(x), x))
    return clauses

# ---------------------------------------------
# ---------------------------------------------
# Giải quyết bài toán Gem Hunter bằng cách sử dụng thư viện PySAT
# PySAT: https://pysathq.github.io/docs/html/index.html
def solve_by_pysat(matrix, KB):
    raise NotImplementedError("This function is not implemented yet")





# ---------------------------------------------
# --------- Main Program of test.py -----------
# ---------------------------------------------
if __name__ == "__main__":

    matrix = input_matrix()
    print(f"Input matrix:\n {matrix}\n")

    KB = get_CNF_clauses(matrix)
    print(f"KB ({len(KB)}):\n {KB}")

    output_matrix(matrix)




