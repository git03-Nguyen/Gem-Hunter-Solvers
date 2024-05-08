# Description: Định nghĩa hàm giải bài toán Gem Hunter bằng các thuật toán khác nhau
#
# Các hàm:
# - solve(matrix, algorithm): Hàm giải bài toán Gem Hunter bằng các thuật toán khác nhau
# - solve_by_pysat(KB): Giải bài toán bằng PySAT
# - solve_by_dpll(KB): Giải bài toán bằng DPLL
# - solve_by_backtracking(KB): Giải bài toán bằng Backtracking
# - solve_by_bruteforce(KB): Giải bài toán bằng Bruteforce

from modules.cnf import get_CNF_clauses
from modules.utils import padding, to_1D

from modules.pysat_solver import solve_by_pysat
from modules.dpll_solver import solve_by_dpll
from modules.backtrack_solver import solve_by_backtracking
from modules.bruteforce_solver import solve_by_bruteforce

import timeit


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
            - solution: model của SAT Solver hoặc None nếu không có lời giải
            - measured_time: thời gian thực thi (ms)
    '''
    
    # Tạo KB gồm các CNF từ ma trận
    KB = get_CNF_clauses(matrix)
    print(f"\n- {len(KB)} CNFs: {KB[:min(len(KB), 8)]}...")

    pad_matrix = padding(matrix)
    n, m = len(pad_matrix), len(pad_matrix[0])

    # Tìm các ô trống
    empties = set()
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if pad_matrix[i][j] is None:
                empties.add(to_1D((i - 1, j - 1), m - 2))
    print(f"- {len(empties)} empty cells: {list(empties)[:min(len(empties), 15)]}...\n")

    # Tìm các ô chứa số
    numbers = {}
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if type(pad_matrix[i][j]) is int:
                numbers[(i - 1, j - 1)] = pad_matrix[i][j]
    
    # Chọn thuật toán giải
    func, args = None, None
    if algorithm == "pysat":
        func = solve_by_pysat
        args = [KB]
    elif algorithm == "dpll":
        func = solve_by_dpll
        args = [KB]
    elif algorithm == "backtracking":
        func = solve_by_backtracking
        args = [KB, empties]
    elif algorithm == "bruteforce":
        func = solve_by_bruteforce
        args = [KB, empties, numbers]
    else:
        raise ValueError("Invalid algorithm")

    start, end, measured_time = 0, 0, 0
    
    # Thực thi thuật toán
    if measure_time:
        start = timeit.default_timer()
        model = func(*args)
        end = timeit.default_timer()
        measured_time = (end - start) * 1000
    else:
        model = func(*args)

    # Nếu có lời giải, thêm các ô trống còn thiếu vào model
    # Những ô trống này thực chất mang giá trị nào cũng được, vì không ảnh hưởng đến lời giải
    # Ở đây ta chọn mặc định là False - "G"
    if model is not None:
        for empty in empties:
            if empty not in model:
                model.append(-empty)
        model = list(set(model))
        model.sort(key = lambda x: abs(x))
        return model, measured_time
    
    return None, measured_time




    



