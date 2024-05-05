# Description: File chính chứa hàm main, thực thi chương trình

import sys
from inout import input_matrix, output_matrix
from solvers import solve

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

# In ra thông báo lỗi nếu tham số không hợp lệ: test_case, algorithm
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
        return None, None

    if test_case not in _TEST_CASES:
        print(f"Test case {test_case} not found")
        print(f"Available: {test_cases}")
        return None, None
    
    return algorithm, test_case


# ---------------------------------------------
# --------------- MAIN FUNCTION ---------------
# ---------------------------------------------
def main(argv):
    algorithm, test_case = read_args(argv)
    if test_case is None or algorithm is None: return

    input_file = _TEST_CASES[test_case] + "/input.txt"
    output_file = _TEST_CASES[test_case] + "/output.txt"

    matrix = input_matrix(input_file); 
    print(f"Input matrix:\n {matrix}")

    solution = solve(matrix, algorithm = algorithm)
    
    if solution is not None:
        output_matrix(solution, output_file);
        print(f"Output matrix:\n {solution}\n")
    else:
        print("No solution found")
        output_matrix([["No solution"]], output_file);

# ---------------------------------------------
if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as e:
        print(f"Error: {e}")

    # testing
    # main(["", "5x5", "pysat"])



    





