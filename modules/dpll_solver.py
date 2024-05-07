# Description: Định nghĩa hàm giải bài toán Gem Hunter bằng thuật toán DPLL

# Hàm lan truyền unit propagation
def propagate_unit(KB, unit):
    for clause in KB:
        if unit in clause:
            KB.remove(clause)
        elif -unit in clause:
            clause.remove(-unit)
    return KB


# Giải bằng DPLL
def solve_by_dpll(KB, empties):

    # Hàm kiểm tra xem KB có rỗng hay không
    def is_empty(KB):
        return len(KB) == 0

    # Hàm kiểm tra xem KB có chứa mệnh đề rỗng hay không
    def has_empty_clause(KB):
        return any([len(clause) == 0 for clause in KB])

    # Hàm kiểm tra xem KB có chứa mệnh đề đơn hay không
    def has_unit_clause(KB):
        return any([len(clause) == 1 for clause in KB])

    # Hàm chọn mệnh đề đơn
    def choose_unit_clause(KB):
        for clause in KB:
            if len(clause) == 1:
                return clause[0]
        return None

    # Hàm chọn mệnh đề ngẫu nhiên
    def choose_literal(KB):
        for clause in KB:
            for literal in clause:
                return literal

    # Hàm giải bài toán bằng DPLL
    def dpll(KB, model):
        if is_empty(KB):
            return model
        if has_empty_clause(KB):
            return None

        while has_unit_clause(KB):
            unit = choose_unit_clause(KB)
            KB = propagate_unit(KB, unit)
            model.append(unit)

        literal = choose_literal(KB)
        if dpll(propagate_unit(KB, literal), model + [literal]) is not None:
            return model + [literal]
        return dpll(propagate_unit(KB, -literal), model + [-literal])

    return dpll(KB, [])


