from main import run
from modules.utils import hash_model
from tabulate import tabulate

# Hàm ghi kết quả ra file dưới dạng bảng tabulate
def write_result(result, file="benchmark.txt"):
    with open(file, "w") as f:
        f.write(result)

# Đo thời gian chạy của thuật toán
if __name__ == "__main__":

    # Create a table to store the results
    result = []
    test, algorithm, elapsed_time, logging_info, model = None, None, None, None, None

    test_index = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
    test_count = 0

    for test_case in ["5x5", "9x9", "11x11", "15x15", "20x20"]:
        print("--------------------")
        print(f"\n{test_index[test_count]}. RUNNING TEST-CASE {test_case.upper()}")
        test_count += 1

        alg_count = 0
        for algorithm in ["pysat", "dpll", "backtracking", "bruteforce"]:
            print(f"\n{alg_count + 1}. Running algorithm {algorithm}")
            alg_count += 1

            if algorithm == "bruteforce" and hash_model(model) is not None and hash_model(model) >= 4e9:
                print("Bruteforce algorithm is too slow for this model. Skipping...\n")
                result += [[test_case, logging_info['CNFs'], logging_info['empties'], len([x for x in model if x > 0]), algorithm, "N/A", hash_model(model)]]

            else:
                test, algorithm, elapsed_time, logging_info, model = run(["", algorithm, test_case], False)
                result += [[test_case, logging_info['CNFs'], logging_info['empties'], len([x for x in model if x > 0]), algorithm, f"{elapsed_time:.4f} ms", hash_model(model)]]
            
            table = tabulate(result, headers=['Test case', 'CNFs', 'Empty cells', 'Traps', 'Algorithm', 'Time', 'Model hash (binary)'], tablefmt='orgtbl')
            write_result(table, "benchmark.txt")
        
        # Draw a horizontal line to separate test cases
        result += [["-" for _ in range(7)]]

    print("--------------------")
    print("\nBenchmarking completed. Results are saved in benchmark.txt")
    print(table)

    