# Description: Định nghĩa hàm giải bài toán Gem Hunter bằng thuật toán DPLL

# Giải bằng DPLL
def solve_by_dpll(KB):

    # Hàm kiểm tra xem KB có chứa mệnh đề đơn hay không
    def has_unit_clause(KB):
        return any([len(clause) == 1 for clause in KB])

    # Hàm chọn mệnh đề đơn
    def choose_unit_clause(KB):
        for clause in KB:
            if len(clause) == 1:
                return clause[0]
        return None
    
    # Hàm lan truyền unit propagation
    def propagate_unit(KB, unit):
        for clause in KB:
            if unit in clause:
                KB.remove(clause)
            elif -unit in clause:
                clause.remove(-unit)
        return KB   

    # Hàm chọn mệnh đề ngẫu nhiên
    def choose_literal(KB):
        for clause in KB:
            for literal in clause:
                return literal
            
    # Hàm kiểm tra xem KB có chứa pure symbol hay không
    def has_pure_symbol(KB):
        literals = set([literal for clause in KB for literal in clause])
        return any([-literal not in literals for literal in literals])
    
    # Hàm chọn pure symbol
    def choose_pure_symbol(KB):
        literals = set([literal for clause in KB for literal in clause])
        for literal in literals:
            if -literal not in literals:
                return literal
        return None

    # Hàm giải bài toán bằng DPLL
    def dpll(KB, model):
        
        # Nếu KB rỗng thì trả về model
        if len(KB) == 0:
            return model
        
        # Nếu KB chứa mệnh đề rỗng thì trả về None
        if any([len(clause) == 0 for clause in KB]):
            return None
        
        # Tìm pure symbol và unit clause để lan truyền
        while has_pure_symbol(KB):
            pure = choose_pure_symbol(KB)
            KB = [clause for clause in KB if pure not in clause]
            model.append(pure)

        while has_unit_clause(KB):
            unit = choose_unit_clause(KB)
            KB = propagate_unit(KB, unit)
            model.append(unit)

        # Chọn mệnh đề ngẫu nhiên
        pure = choose_literal(KB)

        # Thử gán True và False cho mệnh đề ngẫu nhiên
        if dpll(propagate_unit(KB, pure), model + [pure]) is not None:
            return model + [pure]
        return dpll(propagate_unit(KB, -pure), model + [-pure])

    return dpll(KB, [])
    


