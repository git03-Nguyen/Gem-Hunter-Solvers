# Description: Định nghĩa hàm giải bài toán Gem Hunter bằng các thuật toán khác nhau
#
# Các hàm:
# - solve(matrix, algorithm): Hàm giải bài toán Gem Hunter bằng các thuật toán khác nhau
# - solve_by_pysat(KB): Giải bài toán bằng PySAT
# - solve_by_dpll(KB): Giải bài toán bằng DPLL
# - solve_by_backtracking(KB): Giải bài toán bằng Backtracking
# - solve_by_bruteforce(KB): Giải bài toán bằng Bruteforce

from modules.cnf import get_CNF_clauses
from modules.utils import edit_matrix, padding, to_1D

from modules.pysat_solver import solve_by_pysat
from modules.dpll_solver import solve_by_dpll
from modules.backtrack_solver import solve_by_backtracking
from modules.bruteforce_solver import solve_by_bruteforce

import timeit


# Hàm giải bài toán Gem Hunter
# Input: ma trận Gem Hunter, thuật toán giải
# Output: model của SAT Solver hoặc None nếu không có lời giải
def solve(matrix, algorithm = "pysat", measure_time = False):
    '''
        Giải bài toán Gem Hunter bằng các thuật toán SAT Solvers khác nhau.
        
        Input:
            - matrix: ma trận Gem Hunter
            - algorithm: thuật toán giải (pysat, dpll, backtracking, bruteforce)

        Output:
            - solution: model của SAT Solver hoặc None nếu không có lời giải
            - measured_time: thời gian thực thi (ms)
    '''
    KB = get_CNF_clauses(matrix)
    print(f"CNFs ({len(KB)}): {KB[:min(len(KB), 10)]}...")

    pad_matrix = padding(matrix)
    n, m = len(pad_matrix), len(pad_matrix[0])

    empties = set()
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if pad_matrix[i][j] is None:
                empties.add(to_1D((i - 1, j - 1), m - 2))
    print(f"Empties ({len(empties)}): {empties}")

    numbers = {}
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if type(pad_matrix[i][j]) is int:
                numbers[(i - 1, j - 1)] = pad_matrix[i][j]
    


    func, args = None, None
    if algorithm == "pysat":
        func = solve_by_pysat
        args = [KB]
    elif algorithm == "dpll":
        func = solve_by_dpll
        args = [KB, empties]
    elif algorithm == "backtracking":
        func = solve_by_backtracking
        args = [KB, empties]
    elif algorithm == "bruteforce":
        func = solve_by_bruteforce
        args = [KB, empties, numbers]
    else:
        raise ValueError("Invalid algorithm")

    start, end, measured_time = 0, 0, 0
    
    if measure_time:
        start = timeit.default_timer()
        solution = func(*args)
        end = timeit.default_timer()
        measured_time = (end - start) * 1000
    else:
        solution = func(*args)

    if solution is not None:
        print(f"Solution ({len(solution)}): {solution}")
        return edit_matrix(matrix, solution), measured_time
    
    return None, measured_time




    



