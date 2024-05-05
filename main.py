from inout import input_matrix, output_matrix
from solvers import solve



# ---------------------------------------------
# --------------- MAIN FUNCTION ---------------
# ---------------------------------------------
if __name__ == "__main__":

    input_file = "testcases/input.txt"
    output_file = "testcases/output.txt"

    matrix = input_matrix(input_file); 

    print(f"Input matrix:\n {matrix}")
    solution = solve(matrix, algorithm = "pysat")

    if solution is not None:
        output_matrix(solution, output_file);
        print(f"Output matrix:\n {solution}\n")
    else:
        print("No solution found")
        output_matrix([["No solution"]], output_file);

# ---------------------------------------------

    





