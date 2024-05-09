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

# Chuyển từ vị trí (r, c) trong ma trận 2 chiều thành vị trí trong ma trận 1 chiều
def to_1D(pos, num_cols):
    return pos[0]*num_cols + pos[1] + 1

# Lấy tất cả các tập con k phần tử của một tập hợp
def subsets_of(arr, k):
    arr = list(set(arr))
    arr.sort()
    subsets = [list(x) for x in combinations(arr, k)]
    return subsets

# ---------------------------------------------
# Hàm chỉnh sửa ma trận kết quả
def update_matrix(matrix, model):
    '''Chỉnh sửa ma trận kết quả từ model của SAT Solver:\\
          Ô nào False thì là "G", True thì là "T".
    '''
    if model is None:
        return None
    n_rows = len(matrix)
    n_cols = len(matrix[0])
    for i in range(n_rows):
        for j in range(n_cols):
            if matrix[i][j] is None:
                index = i * n_cols + j + 1
                matrix[i][j] = "T" if index in model else "G"
                
    return matrix

# ---------------------------------------------
# Hàm hash 1 mảng số nguyên thành 1 số nguyên: 
# Dương -> 0b1, Âm -> 0b0
# VD: [-1, -2, -3] -> 0b000 -> 0 và [1, 2, 3] -> 0b111 -> 7
def hash_model(model):
    '''Hash model thành một số nguyên:\\
          True -> 1, False -> 0.
    '''
    if model is None:
        return None
    num = 0
    for i in range(len(model)):
        if model[i] > 0:
            num |= 1 << i
            
    return num

