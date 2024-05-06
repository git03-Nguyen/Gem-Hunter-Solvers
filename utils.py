# Description: Các hàm tiện ích dùng chung cho các module khác

from itertools import combinations

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

# Lấy các ô xung quanh ô pos mà có điều kiện là 1 lambda function, mặc định không có điều kiện
def get_around(matrix, pos, condition = None):
    [r, c] = pos
    around = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if condition(matrix[r + i][c + j]) or condition is None:
                around.append([r + i, c + j])
    return around

# # Đếm số lượng ô xung quanh ô pos mà thỏa mãn điều kiện condition
# def count_around(matrix, pos, condition):
#     [r, c] = pos
#     count = 0
#     for i in range(-1, 2):
#         for j in range(-1, 2):
#             if condition(matrix[r + i][c + j]):
#                 count += 1
#     return count

# # Đếm tổng các ô chữ số trong ma trận
# def sum_numbers(matrix):
#     return sum([x for row in matrix for x in row if type(x) == int])

# Chuyển từ vị trí (r, c) trong ma trận 2 chiều thành vị trí trong ma trận 1 chiều
def to_1D(pos, num_cols):
    return pos[0]*num_cols + pos[1] + 1

# Lấy tất cả các tập con k phần tử của một tập hợp
def subsets_of(arr, k):
    arr = list(set(arr))
    arr.sort()
    subsets = [list(x) for x in combinations(arr, k)]
    return subsets


# Hàm kiểm tra 2 list true_case và case giống nhau
def is_similar(list_1, list_2): 
    length = len(list_1)
    for i in range(length):
        if list_1[i] != list_2[i]:
            return False
    return True

# ---------------------------------------------
# Hàm chỉnh sửa ma trận kết quả
def edit_matrix(matrix, model):
    '''Chỉnh sửa ma trận kết quả từ model của SAT Solver:\\
          Ô nào False thì là "G", True thì là "T".
    '''
    n_rows = len(matrix)
    n_cols = len(matrix[0])
    for i in range(n_rows):
        for j in range(n_cols):
            if matrix[i][j] is None:
                index = i * n_cols + j + 1
                matrix[i][j] = "T" if index in model else "G"
                
    return matrix

