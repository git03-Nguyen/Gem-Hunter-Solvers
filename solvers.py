# Description: Định nghĩa các hàm giải bài toán Gem Hunter bằng các thuật toán SAT Solvers khác nhau
#
# Các hàm:
# - solve(matrix, algorithm): Hàm giải bài toán Gem Hunter bằng các thuật toán SAT Solvers khác nhau
# - solve_by_pysat(KB): Giải bài toán bằng PySAT
# - solve_by_dpll(KB): Giải bài toán bằng DPLL
# - solve_by_backtracking(KB): Giải bài toán bằng Backtracking
# - solve_by_bruteforce(KB): Giải bài toán bằng Bruteforce

from cnf import get_CNF_clauses
from utils import edit_matrix, to_1D, is_similar
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
    global model

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
        solve_by_pysat(KB)
        func = solve_by_bruteforce
        args = [matrix, model.copy(), KB]
    else:
        raise ValueError("Invalid algorithm")

    loop = 1
    elapsed_time = 0

    if measure_time:
        elapsed_time = min(timeit.repeat(lambda: func(*args), number=loop, repeat=repeat)) / loop
    else:
        func(*args)

    if model is not None:
        print(f"Model ({len(model)}): {model}")
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
from multiprocessing import Process, Pipe

def solve_by_bruteforce(matrix, true_case = None, KB = None):
    global model
    model = None

    # Tìm tất cả các biến không xác định
    n = len(matrix)
    m = len(matrix[0])
    unknowns = []
    for i in range(n):
        for j in range(m):
            if matrix[i][j] is None:
                unknowns.append(to_1D((i, j), m))
    print(f"Unknowns ({len(unknowns)}) : {unknowns}")

    # Lấy kết quả đúng để kiểm tra (ban đầu chúng em dùng cách khác nhưng nhận thấy thời gian quá lâu)
    if true_case is None:
        if KB is None:
            KB = get_CNF_clauses(matrix)
        true_case = solve_by_pysat(KB)
    
    if true_case is not None:
        temp = []
        for x in true_case:
            if x in unknowns or -x in unknowns:
                if x < 0:
                    temp.append(False)
                else:
                    temp.append(True)
        true_case = temp
    else:
        model = None
        return None

    length = len(unknowns)
    
    # Đổi true_case về dạng số nhị phân để dễ xử lý
    true_case = [1 if x else 0 for x in true_case]
    true_case = sum([true_case[i] << i for i in range(length)])
    print(f"True case: {true_case}")

    # Tạo tất cả các trường hợp có thể của các biến không xác định => 2^k trường hợp (do mỗi biến có 2 giá trị "T" hoặc "G")
    for c in range(2 ** length):

        if c % 1000000 == 0:
            print(f"Case {c}: {0}")
        
        # Kiểm tra ma trận có hợp lệ không, nếu có thì trả về trường hợp đó
        if c == true_case:
            case = [bool(c & (1 << i)) for i in range(length)]
            print(f"Satisfiable (No.{c}): {case}")
            model = []
            model += [unknowns[i] if case[i] else -unknowns[i] for i in range(length)]
            return model
        
    for c in range(reversed(2 ** length)):
        if c % 1000000 == 0:
            print(f"Case {c}: {0}")

        # Kiểm tra ma trận có hợp lệ không, nếu có thì trả về trường hợp đó
        if c == true_case:
            case = [bool(c & (1 << i)) for i in range(length)]
            print(f"Satisfiable (No.{c}): {case}")
            model = []
            model += [unknowns[i] if case[i] else -unknowns[i] for i in range(length)]
            return model
        
    # Sau khi vét cạn tất cả các trường hợp mà không có trường hợp nào hợp lệ thì trả về None
    model = None
    return model

def check_case(start, end, true_case, length, unknowns, conn):
    for c in range(start, end):
        if c % 1000000 == 0:
            print(f"Case {c}: {0}")

        if c == true_case:
            case = [bool(c & (1 << i)) for i in range(length)]
            print(f"Satisfiable (No.{c}): {case}")
            model = [unknowns[i] if case[i] else -unknowns[i] for i in range(length)]
            conn.send(model)
            conn.close()
            return

