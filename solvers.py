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

from pysat.formula import CNF
from pysat.solvers import Solver

model = None
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
            - solution: ma trận kết quả
    '''
    KB = get_CNF_clauses(matrix)
    print(f"CNFs length: {len(KB)}")

    func, args = None, None
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

    start, end, measured_time = 0, 0, 0
    
    if measure_time:
        start = timeit.default_timer()
        model = func(*args)
        end = timeit.default_timer()
        measured_time = (end - start) * 1000
    else:
        model = func(*args)

    if model is not None:
        print(f"Model ({len(model)}): {model}")
        return edit_matrix(matrix, model), measured_time
    
    return None, measured_time

# ---------------------------------------------
# Giải quyết bài toán Gem Hunter bằng cách sử dụng thư viện PySAT
# PySAT: https://pysathq.github.io/docs/html/index.html
def solve_by_pysat(KB):
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
def is_valid(case, numbers_dict, numbers_around_dict, bit_masks_dict):
    for (x, y) in numbers_around_dict.keys():
        num = numbers_dict[(x, y)]
        count = 0
        for xx, yy in numbers_around_dict[(x, y)]: 
            if case & bit_masks_dict[(xx, yy)]:
                count += 1
                if count > num:
                    return False
        if count != num:
            return False
    return True
# ---------------------------------------------
def loop(unknowns, unknowns_dict, numbers_dict, numbers_sum, start, end):
    length = len(unknowns)
    bit_masks_dict = {(x, y): 1 << i for i, (x, y) in enumerate(unknowns_dict.keys())}
    numbers_around_dict = {}
    for (x, y) in numbers_dict.keys():
        numbers_around_dict[(x, y)] = set()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            xx = x + dx
            yy = y + dy
            if (xx, yy) in unknowns_dict.keys():
                numbers_around_dict[(x, y)].add((xx, yy))

    for c in range(start, end):

        if c % 100000000 == 0:
            if c > 0:
                print(f"Case {c}")

        # Nếu sum_số > 8*num_traps thì bỏ qua
        if numbers_sum > (c.bit_count() << 3):
            continue

        # Kiểm tra xem trường hợp này có phải là trường hợp đúng không
        if is_valid(c, numbers_dict, numbers_around_dict, bit_masks_dict):
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

    numbers_dict = [(i, j) for i in range(n) for j in range(m) if type(matrix[i][j]) == int]
    numbers_dict = {pos: matrix[pos[0]][pos[1]] for pos in numbers_dict}
    numbers_sum = sum([matrix[pos[0]][pos[1]] for pos in numbers_dict])

    # Tạo tất cả các trường hợp có thể của các biến không xác định 
    # => 2^k trường hợp (do mỗi biến có 2 giá trị "T" hoặc "G")
    length = len(unknowns)
    start = 0
    end = 1 << length
    model = loop(unknowns, unknowns_dict, numbers_dict, numbers_sum, start, end)
    
    return model

    



