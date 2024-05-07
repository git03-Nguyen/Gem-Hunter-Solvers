# Description: Định nghĩa hàm giải bài toán Gem Hunter bằng thuật toán Backtracking

def is_conflict(KB, solution_bits, bits_length, empties_dict, empties_set, bit_masks):

    # Empties_dict: {pos: index} với pos là vị trí ô trống, index là index của ô trống trong solution
    
    for clause in KB:
        
        is_clause_true = False
        for literal in clause:
            # Nếu literal không phải là ô trống thì bỏ qua
            if literal not in empties_set and -literal not in empties_set:
                is_clause_true = True
                continue

            # Nếu literal là ô trống và chưa tới lượt gán giá trị thì bỏ qua
            index = empties_dict[literal] if literal > 0 else empties_dict[-literal]
            if index > bits_length:
                is_clause_true = True
                continue

            # Nếu literal là ô trống và đã được gán giá trị thì kiểm tra xem có conflict không
            # Conflict xảy ra khi literal là dương và bit tương ứng trong solution_bits bằng 0
            # hoặc literal là âm và bit tương ứng trong solution_bits bằng 1
            if (literal > 0 and not (solution_bits & bit_masks[literal])) or (literal < 0 and (solution_bits & bit_masks[-literal])):
                is_clause_true = is_clause_true or False
            else:
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
    values = {0, 1}

    # bit_masks[n] = 00010 tức n là ô trống thứ 2; c & bit_masks[n] trả về bit thứ 2 của c
    bit_masks = {empties_list[i]: 1 << i for i in range(length)}

    # Hàm đệ quy giải bài toán: sử dụng DFS và backtracking
    def backtrack(solution_bits, index):
        if index == length:
            return solution_bits

        # Gán giá trị cho ô trống thứ index là 0 hoặc 1            
        for i in values:
            if i: # Gán giá trị cho ô trống là 1
                solution_bits |= 1 << index
                if is_conflict(KB, solution_bits, index, empties_dict, empties, bit_masks):
                    continue
            else: # Gán giá trị cho ô trống là 0
                if is_conflict(KB, solution_bits, index, empties_dict, empties, bit_masks):
                    continue                
            
            # Nếu không conflict thì tiếp tục gán giá trị cho ô trống tiếp theo
            solution_bits = backtrack(solution_bits, index + 1)
            if solution_bits is not None:
                return solution_bits
            
        # Nếu không tìm được giá trị thích hợp cho ô trống thứ index thì quay lui
        return None
    
    # Bắt đầu giải bài toán
    solution_bits = backtrack(0, 0)
    if solution_bits is None:
        return None
    
    solution = [bool(solution_bits & (1 << i)) for i in range(length)]
    model = [empties_list[i] if solution[i] else -empties_list[i] for i in range(length)]
    return model



            
            
        







