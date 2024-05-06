# Description: Định nghĩa các hàm giải bài toán Gem Hunter bằng các thuật toán SAT Solvers khác nhau
#
# Các hàm:
# - solve(matrix, algorithm): Hàm giải bài toán Gem Hunter bằng các thuật toán SAT Solvers khác nhau
# - solve_by_pysat(KB): Giải bài toán bằng PySAT
# - solve_by_dpll(KB): Giải bài toán bằng DPLL
# - solve_by_backtracking(KB): Giải bài toán bằng Backtracking
# - solve_by_bruteforce(KB): Giải bài toán bằng Bruteforce

from cnf import get_CNF_clauses
from utils import count_around, edit_matrix, padding, to_1D, sum_numbers
import timeit
from itertools import product

model = None
# Hàm giải bài toán Gem Hunter
# Input: ma trận Gem Hunter, thuật toán giải
# Output: model của SAT Solver hoặc None nếu không có lời giải
def solve(matrix, algorithm = "pysat", measure_time = True, repeat = 1):
    '''
        Giải bài toán Gem Hunter bằng các thuật toán SAT Solvers khác nhau.
        
        Input:
            - matrix: ma trận Gem Hunter
            - algorithm: thuật toán giải (pysat, dpll, backtracking, bruteforce)

        Output:
            - solution: ma trận kết quả
    '''

    KB = get_CNF_clauses(matrix)
    print(f"CNFs length: {len(KB)}")

    func = None
    args = None
    if algorithm == "pysat":
        func = solve_by_pysat
        args = [KB]
    elif algorithm == "dpll":
        func = solve_by_dpll
        args = [KB]
    elif algorithm == "backtracking":
        func = solve_by_backtracking
        args = [KB]
    elif algorithm == "bruteforce":
        func = solve_by_bruteforce
        args = [matrix]
    else:
        raise ValueError("Invalid algorithm")

    loop = 1
    elapsed_time = 0

    if measure_time:
        elapsed_time = min(timeit.repeat(lambda: func(*args), number=loop, repeat=repeat)) / loop
    else:
        func(*args)

    global model
    if model is not None:
        print(f"Model: {model}")
        return edit_matrix(matrix, model), elapsed_time
    
    return None, elapsed_time

# ---------------------------------------------
# Giải quyết bài toán Gem Hunter bằng cách sử dụng thư viện PySAT
# PySAT: https://pysathq.github.io/docs/html/index.html
def solve_by_pysat(KB):
    from pysat.formula import CNF
    from pysat.solvers import Solver

    # Tạo một solver (mặc định là Minisat 2.2) cho các câu mệnh đề CNF
    cnf = CNF(from_clauses=KB)
    with Solver(bootstrap_with=cnf) as solver:
        solver.solve();
        global model
        model = solver.get_model()
        return model
        
# ---------------------------------------------
# Giải bằng DPLL
def solve_by_dpll(KB):
    raise NotImplementedError("DPLL is not implemented")

# ---------------------------------------------
# Giải bằng backtracking
def solve_by_backtracking(KB):
    raise NotImplementedError("Backtracking is not implemented")

# ---------------------------------------------
# Giải bằng bruteforce
def solve_by_bruteforce(matrix):
    global model
    is_trap = lambda x: x == "T"
    sum_num = sum_numbers(matrix)

    matrix = padding(matrix)
    n = len(matrix)
    m = len(matrix[0])

    num_arr = []
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if type(matrix[i][j]) == int:
                num_arr.append((i, j))

    # Hàm kiểm tra ma trận có hợp lệ không
    def is_valid(matrix, count_T):

        if count_T > sum_num:
            return False
        
        for num in num_arr:
            i, j = num
            count = count_around(matrix, (i, j), is_trap)
            if count != matrix[i][j]:
                return False
        return True

    

    # Tìm tất cả các biến không xác định
    unknowns = []
    unknowns_2 = []
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if matrix[i][j] is None:
                unknowns.append(to_1D((i - 1, j - 1), m - 2))
                unknowns_2.append((i, j))
    print(f"Unknowns: {len(unknowns)} : {unknowns}")
    
    # Tạo tất cả các trường hợp có thể của các biến không xác định => 2^k trường hợp (do mỗi biến có 2 giá trị "T" hoặc "G")
    c = 0
    prev_case = [None] * len(unknowns_2)
    for case in product([True, False], repeat=len(unknowns_2)):

        c+=1
        if c % 1000000 == 0:
            print(f"Case {c}: {case}")

        # Tìm số lượng vị trí thay đổi
        # for i, (prev, curr) in enumerate(zip(prev_case, case)):
        #     # if prev != curr:
        #     #     x, y = unknowns_2[i]
        #     #     matrix[x][y] = "T" if curr else "G"
        #     x, y = unknowns_2[i]
        
        prev_case = case

        # Tìm số lượng "T" trong trường hợp hiện tại
        count_T = case.count("T")

        # Kiểm tra ma trận có hợp lệ không, nếu có thì trả về trường hợp đó
        # if is_valid(matrix, count_T):
        #     print(f"Case {c}: {case}")
        #     model = []
        #     for i in range(len(unknowns_2)):
        #         value = unknowns[i] if case[i] == "T" else -unknowns[i]
        #         model.append(value)

        #     return model
        
    # Sau khi vét cạn tất cả các trường hợp mà không có trường hợp nào hợp lệ thì trả về None
    model = None
    return model


