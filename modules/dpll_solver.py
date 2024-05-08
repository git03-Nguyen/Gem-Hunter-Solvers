# Description: Định nghĩa hàm giải bài toán Gem Hunter bằng thuật toán DPLL

# Giải bằng DPLL
def solve_by_dpll(KB):

    # Hàm kiểm tra xem KB có chứa mệnh đề đơn hay không
    def has_unit_clause(KB):
        KB.sort(key=len)
        for clause in KB:
            if len(clause) == 1:
                return True
        return False

    # Hàm chọn mệnh đề đơn
    def choose_unit_clause(KB):
        for clause in KB:
            if len(clause) == 1:
                return clause[0]
        return None
    
    # Hàm lan truyền unit propagation
    def propagate_unit(KB, unit):
        KB_copy = [row.copy() for row in KB]

        for clause in KB_copy:
            if unit in clause:
                KB.remove(clause)
        
        for clause in KB:
            if -unit in clause:
                clause.remove(-unit)
        
        return KB   

    # Hàm chọn mệnh đề ngẫu nhiên
    def choose_literal(KB):
        return KB[0][0]
            
    # # Hàm kiểm tra xem KB có chứa pure symbol hay không
    # def has_pure_symbol(KB):
    #     literals = set([literal for clause in KB for literal in clause])
    #     return any([-literal not in literals for literal in literals])
    
    # # Hàm chọn pure symbol
    # def choose_pure_symbol(KB):
    #     literals = set([literal for clause in KB for literal in clause])
    #     for literal in literals:
    #         if -literal not in literals:
    #             return literal
    #     return None

    # Hàm giải bài toán bằng DPLL
    def dpll(KB, model):
        
        # Nếu KB rỗng thì trả về model
        if len(KB) == 0:
            return model
        
        # Nếu KB chứa mệnh đề rỗng thì trả về None
        if any([len(clause) == 0 for clause in KB]):
            return None
        
        # Tìm pure symbol và unit clause để lan truyền

        # while has_pure_symbol(KB):
        #     pure = choose_pure_symbol(KB)
        #     print("Pure symbol:", pure)
        #     KB = [clause for clause in KB if pure not in clause]
        #     print("KB after pure symbol:", len(KB))
        #     model.append(pure)

        while has_unit_clause(KB):
            unit = choose_unit_clause(KB)
            KB = propagate_unit(KB, unit)

            # Nếu KB chứa mệnh đề rỗng thì trả về None
            if len(KB) == 0:
                return model
        
            if any([len(clause) == 0 for clause in KB]):
                return None
            
            # if unit == 46 or unit == -48:
            #     KB.sort(key=len)
            #     print(KB)
            model.append(unit)



        # Chọn mệnh đề ngẫu nhiên
        literal = choose_literal(KB)

        # Thử gán True và False cho mệnh đề ngẫu nhiên
        
        # KB_reserved = KB.copy(row.copy() for row in KB)
        KB_reserved = [row.copy() for row in KB]

        # if dpll(propagate_unit(KB, literal), model + [literal]) is not None:
        #     return model + [literal]
        # else:
        #     KB = KB_reserved
        #     if dpll(propagate_unit(KB, -literal), model + [-literal]) is not None:
        #         return model + [-literal]
        #     else:
        #         return None

        # Gán True cho mệnh đề ngẫu nhiên
        result = dpll(propagate_unit(KB, literal), model + [literal])
        if result is not None:
            return result
        
        # Gán False cho mệnh đề ngẫu nhiên
        result = dpll(propagate_unit(KB_reserved, -literal), model + [-literal])
        if result is not None:
            return result
        
        # Nếu không tìm được giải pháp thì trả về None, quay lui
        return None

    model = dpll(KB, [])
    return model
    


