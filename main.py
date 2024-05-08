# Description: File chính chứa hàm main, thực thi chương trình

import sys
from modules.inout import input_matrix, output_matrix, print_matrix, print_2matrix
from modules.solvers import solve
from modules.utils import hash_model, update_matrix

# Danh sách thuật toán
_ALGORITHMS = {
    "pysat": "pysat",
    "dpll": "dpll",
    "backtracking": "backtracking",
    "bruteforce": "bruteforce",
}

# Danh sách test case
_TEST_CASES = {
    "4x4": "testcases/4x4", 
    "5x5": "testcases/5x5",
    "9x9": "testcases/9x9",
    "11x11": "testcases/11x11",
    "15x15": "testcases/15x15",
    "20x20": "testcases/20x20",
}

# In ra thông báo lỗi nếu tham số không hợp lệ: test_case, algorithm, measure_time
def read_args(argv):
    algorithms = ", ".join(_ALGORITHMS.keys())
    test_cases = ", ".join(_TEST_CASES.keys())

    if len(argv) < 3:
        print("\nUsage: python main.py <algorithm> <test_case>")
        print(f"- algorithm: {algorithms}")
        print(f"- test_case: {test_cases}")
        return None, None

    algorithm = argv[1]
    test_case = argv[2]
    
    if algorithm not in _ALGORITHMS:
        print(f"Algorithm {algorithm} not found")
        print(f"Available: {algorithms}")
        return None, None, None

    if test_case not in _TEST_CASES:
        print(f"Test case {test_case} not found")
        print(f"Available: {test_cases}")
        return None, None, None
    
    return algorithm, test_case


# ---------------------------------------------
# --------------- MAIN FUNCTION ---------------
# ---------------------------------------------
def run(argv, print_matrix = False):
    algorithm, test_case = read_args(argv)
    if test_case is None or algorithm is None: return

    # Đọc file input và output
    input_file = _TEST_CASES[test_case] + "/input.txt"
    output_file = _TEST_CASES[test_case] + "/output.txt"

    matrix = input_matrix(input_file); 
    original_matrix = [row.copy() for row in matrix]

    # Giải bài toán
    model, logging_info, elapsed_time = solve(matrix, algorithm)
    solution = update_matrix(matrix, model)
    
    # Xuất kết quả
    if solution is not None:
        output_matrix(solution, output_file);
    else:
        output_matrix([[""]], output_file);

    # In input và output ra console
    print(f"{print_2matrix(original_matrix, solution)}") if print_matrix else None

    # In thông tin ra console
    print(f"Test {test_case.lower()}: {logging_info["CNFs"]} CNFs, {logging_info["empties"]} empty cells.")
    if model is None: print("No solution found!")
    else: print(f"Result hash: #{hash_model(model)} - {len([x for x in model if x > 0])} traps.")
    print(f"Algorithm: {algorithm.upper()} - {elapsed_time:.4f} ms.")
    print(f"Terminating...\n")

    
# ---------------------------------------------
if __name__ == "__main__":
    # try:
    #     run(sys.argv)
    # except Exception as e:
    #     print(f"Error: {e}")

    # TESTING

    # run(["", "pysat", "4x4"])
    # run(["", "dpll", "4x4"])
    run(["", "backtracking", "4x4"])
    # run(["", "bruteforce", "4x4"])

    # run(["", "pysat", "5x5"])
    # run(["", "dpll", "5x5"])
    # run(["", "backtracking", "5x5"])
    # run(["", "bruteforce", "5x5"])

    # run(["", "pysat", "9x9"])
    # run(["", "dpll", "9x9"])
    # run(["", "backtracking", "9x9"])
    # run(["", "bruteforce", "9x9"])

    # run(["", "pysat", "11x11"])
    # run(["", "dpll", "11x11"])
    # run(["", "backtracking", "11x11"])
    # run(["", "bruteforce", "11x11"])

    # run(["", "pysat", "15x15"])
    # run(["", "dpll", "15x15"])
    # run(["", "backtracking", "15x15"])
    # run(["", "bruteforce", "15x15"])

    # run(["", "pysat", "20x20"])
    # run(["", "dpll", "20x20"])
    # run(["", "backtracking", "20x20"])
    # run(["", "bruteforce", "20x20"])



    # py -m cProfile -s cumtime main.py 
    # py -m cProfile -s ncalls main.py 



    

