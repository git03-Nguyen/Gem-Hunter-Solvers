# Description: Tạo câu mệnh đề CNF từ ma trận Gem Hunter

from modules.utils import padding, get_around, to_1D, subsets_of

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
                
                traps = get_around(matrix, [i, j], lambda x: x == "T")                        # Những ô bẫy "T" xung quanh ô đó
                matrix[i][j] -= len(traps)                                                    # Trừ đi số lượng bẫy "T" xung quanh ô đó

                unknowns = get_around(matrix, [i, j], lambda x: x is None)                    # Những ô chưa biết xung quanh ô đó  
                unknowns = [to_1D((pos[0] - 1, pos[1] - 1), n_cols - 2) for pos in unknowns]  # Chuyển vị trí 2D sang 1D
                
                cnf = exactly(unknowns, matrix[i][j])                                         # Tạo mệnh đề CNF cho ô đó
                clauses += cnf                                                                # Thêm CNF vào KB: "Có đúng matrix[i][j] ô bẫy trong unknowns"

    # Xoá các mệnh đề trùng lặp và sắp xếp theo độ dài câu mệnh đề
    clauses = set([tuple(clause) for clause in clauses])
    clauses = [list(clause) for clause in clauses]
    clauses.sort(key=lambda x: (len(x), x))
    return clauses
