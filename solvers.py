# Description: Định nghĩa các hàm giải bài toán Gem Hunter bằng các thuật toán SAT Solvers khác nhau
#
# Các hàm:
# - solve(matrix, algorithm): Hàm giải bài toán Gem Hunter bằng các thuật toán SAT Solvers khác nhau
# - solve_by_pysat(KB): Giải bài toán bằng PySAT
# - solve_by_dpll(KB): Giải bài toán bằng DPLL
# - solve_by_backtracking(KB): Giải bài toán bằng Backtracking
# - solve_by_bruteforce(KB): Giải bài toán bằng Bruteforce

from cnf import get_CNF_clauses
from utils import edit_matrix

# Hàm giải bài toán Gem Hunter
# Input: ma trận Gem Hunter, thuật toán giải
# Output: model của SAT Solver hoặc None nếu không có lời giải
def solve(matrix, algorithm = "pysat"):
    '''
        Giải bài toán Gem Hunter bằng các thuật toán SAT Solvers khác nhau.
        
        Input:
            - matrix: ma trận Gem Hunter
            - algorithm: thuật toán giải (pysat, dpll, backtracking, bruteforce)

        Output:
            - solution: ma trận kết quả
    '''

    KB = get_CNF_clauses(matrix)
    print(f"CNFs ({len(KB)}):\n {KB}")
    
    model = None
    if algorithm == "pysat":
        model = solve_by_pysat(KB)
    elif algorithm == "dpll":
        model = solve_by_dpll(KB)
    elif algorithm == "backtracking":
        model = solve_by_backtracking(KB)
    elif algorithm == "bruteforce":
        model = solve_by_bruteforce(KB)
    else:
        raise ValueError("Invalid algorithm")
    
    if model is not None:
        return edit_matrix(matrix, model)
    
    return None

# ---------------------------------------------
# Giải quyết bài toán Gem Hunter bằng cách sử dụng thư viện PySAT
# PySAT: https://pysathq.github.io/docs/html/index.html
def solve_by_pysat(KB):
        
    from pysat.formula import CNF
    from pysat.solvers import Solver

    # Tạo một solver (mặc định là Minisat 2.2) cho các câu mệnh đề CNF
    cnf = CNF(from_clauses=KB)
    with Solver(bootstrap_with=cnf) as solver:
        
        # Giải bài toán
        is_satisfiable = solver.solve()

        # Nếu không có lời giải
        if not is_satisfiable:
            return None
        
        # Nếu có lời giải
        model = solver.get_model()
        print(f"Model: {model}")
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
def solve_by_bruteforce(KB):
    raise NotImplementedError("Bruteforce is not implemented")

