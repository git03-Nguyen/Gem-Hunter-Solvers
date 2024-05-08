# Description: Định nghĩa hàm giải bài toán Gem Hunter bằng thuật toán Backtracking

def is_conflict(KB, solution_bits, bits_length, empties_dict, empties_set, bit_masks):
    # Có chứa một clause nào mà không thoả mãn thì trả về True
    # Clause không thoả mãn khi tất cả các literal đều False

    # Empties_dict: {pos: index} với pos là vị trí ô trống, index là index của ô trống trong solution
    
    for clause in KB:
        
        is_clause_true = False
        for literal in clause:
            # Nếu literal không phải là ô trống thì bỏ qua

            # Nếu literal là ô trống và chưa tới lượt gán giá trị thì bỏ qua clause
            index = empties_dict[literal] if literal > 0 else empties_dict[-literal]
            if index > bits_length:
                is_clause_true = True
                break

            # Nếu từ KB yêu cầu biến True
            if literal > 0 and solution_bits & bit_masks[literal]: # Case này gán True thì clause True
                is_clause_true = True
                break  
            # Nếu từ KB yêu cầu biến False
            elif literal < 0 and not solution_bits & bit_masks[-literal]: # Case này gán False thì clause True
                is_clause_true = True
                break 

        if not is_clause_true:
            return True

    return False

# Giải bằng backtracking với DFS: lần lượt gán giá trị cho các ô trống là 0 hoặc 1 (tức là bằng -empties[i] hoặc empties[i]), sau đó kiểm tra xem có conflict không, nếu không thì tiếp tục gán cho ô tiếp theo, nếu có thì quay lui và thử giá trị khác cho ô hiện tại
def solve_by_backtracking(KB, empties):
    
    # Để tối ưu performance, ta sẽ tăng cường sử dụng hash map và bitwise
    length = len(empties)
    empties_list = list(empties)
    empties_dict = {empties_list[i]: i for i in range(length)}

    # bit_masks[n] = 00010 tức n là ô trống thứ 2; c & bit_masks[n] trả về bit thứ 2 của c
    bit_masks = {empties_list[i]: 1 << i for i in range(length)}

    # Hàm đệ quy giải bài toán: sử dụng DFS và backtracking
    def backtrack(solution_bits, index):

        if index == length:
            return solution_bits

        # Gán giá trị cho ô trống là 0
        solution_bits = solution_bits & ~bit_masks[empties_list[index]]
        if not is_conflict(KB, solution_bits, index, empties_dict, set(empties_list), bit_masks):
            result = backtrack(solution_bits, index + 1)
            if result is not None:
                return result                     
        
        # Gán giá trị cho ô trống là 1
        solution_bits = solution_bits | bit_masks[empties_list[index]]
        if not is_conflict(KB, solution_bits, index, empties_dict, set(empties_list), bit_masks):
            result = backtrack(solution_bits, index + 1)
            if result is not None:
                return result        
            
        # Nếu không tìm được giá trị thích hợp cho ô trống thứ index thì quay lui
        return None
    
    # Bắt đầu giải bài toán
    solution_bits = backtrack(0, 0)
    if solution_bits is None:
        return None
    
    solution = [bool(solution_bits & (1 << i)) for i in range(length)]
    model = [empties_list[i] if solution[i] else -empties_list[i] for i in range(length)]
    return model

