# Description: File chính chứa hàm main, thực thi chương trình

import sys
from modules.inout import input_matrix, output_matrix, print_2matrix
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
def run(argv, print_matrix = True):
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
    print(f"\n{print_2matrix(original_matrix, solution)}") if print_matrix else None

    # In thông tin ra console
    print(f"Test {test_case.lower()}: {logging_info["CNFs"]} CNFs - {logging_info["empties"]} empty cells.")
    if model is None: print("No solution found!")
    else: print(f"Result hash: #{hash_model(model)} - {len([x for x in model if x > 0])} traps.")
    print(f"Algorithm: {algorithm.upper()} - {elapsed_time:.4f} ms. Terminating...")

    
# ---------------------------------------------
if __name__ == "__main__":
    try:
        run(sys.argv)
    except Exception as e:
        print(f"Error: {e}")

    # TESTING

    # test_case = "5x5"
    # test_case = "9x9"
    # test_case = "11x11"
    # test_case = "15x15"
    # test_case = "20x20"

    # logging = False
    # logging = True

    # run(["", "pysat", test_case], logging)
    # run(["", "dpll", test_case], logging)
    # run(["", "backtracking", test_case], logging)
    # run(["", "bruteforce", test_case], logging)

    # py -m cProfile -s cumtime main.py 
    # py -m cProfile -s ncalls main.py 



    

