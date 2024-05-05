# Description: Định nghĩa các hàm giải bài toán Gem Hunter bằng các thuật toán SAT Solvers khác nhau
#
# Các hàm:
# - solve(matrix, algorithm): Hàm giải bài toán Gem Hunter bằng các thuật toán SAT Solvers khác nhau
# - solve_by_pysat(KB): Giải bài toán bằng PySAT
# - solve_by_dpll(KB): Giải bài toán bằng DPLL
# - solve_by_backtracking(KB): Giải bài toán bằng Backtracking
# - solve_by_bruteforce(KB): Giải bài toán bằng Bruteforce

from cnf import get_CNF_clauses
from utils import edit_matrix, get_around, padding, to_1D
import timeit
from itertools import product

# Hàm giải bài toán Gem Hunter
# Input: ma trận Gem Hunter, thuật toán giải
# Output: model của SAT Solver hoặc None nếu không có lời giải
def solve(matrix, algorithm = "pysat", measure_time = True):
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
    repeat = 5
    elapsed_time = None
    if measure_time:
        elapsed_time = min(timeit.repeat(lambda: func(*args), number=loop, repeat=repeat)) / loop
    
    model = func(*args)

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
        return solver.get_model()
        
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

    # Hàm kiểm tra ma trận có hợp lệ không
    def is_valid(matrix):
        for i in range(1, n - 1):
            for j in range(1, m - 1):
                if type(matrix[i][j]) == int:
                    count = len(get_around(matrix, (i, j), lambda x: x == "T"))
                    if count != matrix[i][j]:
                        return False
        return True

    matrix = padding(matrix)
    n = len(matrix)
    m = len(matrix[0])

    # Tìm tất cả các biến không xác định
    unknowns = []
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if matrix[i][j] is None:
                unknowns.append(to_1D((i - 1, j - 1), m - 2))
    
    # Tạo tất cả các trường hợp có thể của các biến không xác định => 2^k trường hợp (do mỗi biến có 2 giá trị "T" hoặc "G")
    for p in product(["T", "G"], repeat=len(unknowns)):
        case = dict(zip(unknowns, p))
        
        # Gán giá trị "T" và "G" vào ma trận
        for key in case:
            i = (key - 1) // (m - 2)
            j = (key - 1) % (m - 2)  
            matrix[i + 1][j + 1] = case[key]

        # Kiểm tra ma trận có hợp lệ không, nếu có thì trả về trường hợp đó
        if is_valid(matrix):
            for key in case:
                case[key] = key if case[key] == "T" else -key
            return list(case.values())
        
    # Sau khi vét cạn tất cả các trường hợp mà không có trường hợp nào hợp lệ thì trả về None
    return None


