# Description: Định nghĩa các hàm giải bài toán Gem Hunter bằng các thuật toán SAT Solvers khác nhau
#
# Các hàm:
# - solve(matrix, algorithm): Hàm giải bài toán Gem Hunter bằng các thuật toán SAT Solvers khác nhau
# - solve_by_pysat(KB): Giải bài toán bằng PySAT
# - solve_by_dpll(KB): Giải bài toán bằng DPLL
# - solve_by_backtracking(KB): Giải bài toán bằng Backtracking
# - solve_by_bruteforce(KB): Giải bài toán bằng Bruteforce

from cnf import get_CNF_clauses
from utils import edit_matrix, padding, to_1D
import timeit

model = None
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

    model = func(*args)

    if model is not None:
        print(f"Model ({len(model)}): {model}")
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
        solver.solve();
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
# Check
def is_valid(case, numbers_arr, unknowns_dict, unknowns_set, directions, bit_masks_dict):
    for (x, y) in numbers_arr:
        num = numbers_arr[(x, y)]
        count = 0
        for dx, dy in directions:
            xx = x + dx
            yy = y + dy
            if (xx, yy) in unknowns_set:
                if case & bit_masks_dict[(xx, yy)]:
                    count += 1
                    if count > num:
                        return False
        if count != num:
            return False
    return True
# ---------------------------------------------
def loop(unknowns, unknowns_dict, numbers_arr, numbers_sum, start, end):
    length = len(unknowns)
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]
    unknowns_set = set(unknowns_dict.keys())
    bit_masks_dict = {(x, y): 1 << i for i, (x, y) in enumerate(unknowns_dict.keys())}

    for c in range(start, end):

        if (c) % 1000000 == 0:
            print(f"Case {c}")

        # Nếu sum_số > 8*num_traps thì bỏ qua
        if numbers_sum > (c.bit_count() << 3):
            continue

        # Kiểm tra xem trường hợp này có phải là trường hợp đúng không
        if is_valid(c, numbers_arr, unknowns_dict, unknowns_set, directions, bit_masks_dict):
            case = [bool(c & (1 << i)) for i in range(length)]
            print(f"Satisfiable (No.{c}): {case}")
            return [unknowns[i] if case[i] else -unknowns[i] for i in range(length)]

    return None

# Giải bằng bruteforce
def solve_by_bruteforce(matrix):
    # true_case = 3219758312 # for testing

    matrix = padding(matrix)

    # Tìm tất cả các biến không xác định
    n = len(matrix)
    m = len(matrix[0])
    unknowns = []
    unknowns_pos = []
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if matrix[i][j] is None:
                unknowns.append(to_1D((i - 1, j - 1), m - 2))
                unknowns_pos.append((i, j))
    
    unknowns_dict = {unknowns_pos[i]: i for i in range(len(unknowns_pos))}
    print(f"Unknowns ({len(unknowns)}) : {unknowns}")

    numbers_arr = [(i, j) for i in range(n) for j in range(m) if type(matrix[i][j]) == int]
    numbers_arr = {pos: matrix[pos[0]][pos[1]] for pos in numbers_arr}
    numbers_sum = sum([matrix[pos[0]][pos[1]] for pos in numbers_arr])

    # Tạo tất cả các trường hợp có thể của các biến không xác định 
    # => 2^k trường hợp (do mỗi biến có 2 giá trị "T" hoặc "G")
    length = len(unknowns)
    model = loop(unknowns, unknowns_dict, numbers_arr, numbers_sum, 0, 1 << length)
    
    return model

    



