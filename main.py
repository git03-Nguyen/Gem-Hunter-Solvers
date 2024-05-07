# Description: File chính chứa hàm main, thực thi chương trình

import sys
from modules.inout import input_matrix, output_matrix, print_matrix
from modules.solvers import solve

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
        print("\nUsage: python main.py <algorithm> <test_case> [measure_time]")
        print(f"- algorithm: {algorithms}")
        print(f"- test_case: {test_cases}")
        print("- measure_time: True/False (default: False)")
        return None, None

    algorithm = argv[1]
    test_case = argv[2]
    measure_time = len(argv) > 3 and argv[3].lower().strip() == "true"
    
    if algorithm not in _ALGORITHMS:
        print(f"Algorithm {algorithm} not found")
        print(f"Available: {algorithms}")
        return None, None, None

    if test_case not in _TEST_CASES:
        print(f"Test case {test_case} not found")
        print(f"Available: {test_cases}")
        return None, None, None
    
    if len(argv) > 3 and measure_time not in [True, False]:
        print(f"Invalid measure_time: {argv[3]}")
        print("Available: True/False")
        return None, None, None
    
    return algorithm, test_case, measure_time


# ---------------------------------------------
# --------------- MAIN FUNCTION ---------------
# ---------------------------------------------
def run(argv):
    algorithm, test_case, measure_time = read_args(argv)
    if test_case is None or algorithm is None: return

    input_file = _TEST_CASES[test_case] + "/input.txt"
    output_file = _TEST_CASES[test_case] + "/output.txt"

    matrix = input_matrix(input_file); 
    print(f"PROBLEM:\n{print_matrix(matrix)}")

    solution, elapsed_time = solve(matrix, algorithm, measure_time)
    
    if solution is not None:
        output_matrix(solution, output_file);
        print(f"\nSOLUTION:\n{print_matrix(solution)}")
    else:
        output_matrix([["Unsolvable"]], output_file);
        print("NO SOLUTION FOUND!")

    if measure_time:
        print(f"Elapsed time: {elapsed_time:.4f} ms")


# ---------------------------------------------
# --------------- PROFILING FUNCTION ----------
# ---------------------------------------------
def profile():
    raise NotImplementedError("Not implemented yet")

# ---------------------------------------------
if __name__ == "__main__":
    # try:
    #     run(sys.argv)
    # except Exception as e:
    #     print(f"Error: {e}")

    # Testing
    # run(["", "pysat", "4x4", "True"])
    # run(["", "pysat", "9x9", "True"])

    # run(["", "bruteforce", "9x9", "True"])
    # run(["", "bruteforce", "5x5", "True"])
    # run(["", "bruteforce", "4x4", "True"])

    run(["", "backtracking", "4x4", "True"])
    # run(["", "backtrack", "5x5", "True"])
    # run(["", "backtrack", "9x9", "True"])

    # Profiling
    # profile()

    # py -m cProfile -s cumtime main.py 
    # py -m cProfile -s ncalls main.py 



    





