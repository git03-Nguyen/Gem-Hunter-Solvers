# Description: Định nghĩa hàm giải bài toán SAT bằng thư viện PySAT
from pysat.formula import CNF
from pysat.solvers import Solver

# ---------------------------------------------
# Giải quyết bài toán Gem Hunter bằng cách sử dụng thư viện PySAT
# PySAT: https://pysathq.github.io/docs/html/index.html
def solve_by_pysat(KB):
    '''
        Giải bài toán SAT bằng thư viện PySAT
        Input: KB - tập các mệnh đề CNF
        Output: model - một phán định của các biến trong KB
    '''
    # Tạo một solver (mặc định là Minisat 2.2) cho các câu mệnh đề CNF
    cnf = CNF(from_clauses=KB)
    with Solver(bootstrap_with=cnf) as solver:
        solver.solve();
        model = solver.get_model()
        return model
        