# Description: Định nghĩa hàm giải bài toán Gem Hunter bằng thuật toán Backtracking

def is_conflict(KB, solution_bits, bits_length, empties_dict, bit_masks, numbers_sum):

    # Nếu sum_số > 8*num_traps thì conflict
    if numbers_sum > (solution_bits.bit_count() << 3):
        return True

    # Empties_dict: {pos: index} với pos là vị trí ô trống, index là index của ô trống trong solution
    
    for clause in KB:
        
        for literal in clause:
            # Nếu literal không phải là ô trống thì bỏ qua
            if literal not in empties_dict.keys() and -literal not in empties_dict.keys():
                continue

            # Nếu literal là ô trống và chưa được gán giá trị thì bỏ qua
            index = empties_dict[literal] if literal > 0 else empties_dict[-literal]
            if index >= bits_length:
                continue

            # Nếu literal là ô trống và đã được gán giá trị thì kiểm tra xem có conflict không
            # Conflict xảy ra khi literal là dương và bit tương ứng trong solution_bits bằng 0
            # hoặc literal là âm và bit tương ứng trong solution_bits bằng 1
            if (literal > 0 and not (solution_bits & bit_masks[literal])) or (literal < 0 and (solution_bits & bit_masks[-literal])):
                return True               

    return False

# Giải bằng backtracking với DFS: lần lượt gán giá trị cho các ô trống là 0 hoặc 1 (tức là bằng -empties[i] hoặc empties[i]), sau đó kiểm tra xem có conflict không, nếu không thì tiếp tục gán cho ô tiếp theo, nếu có thì quay lui và thử giá trị khác cho ô hiện tại
def solve_by_backtracking(KB, empties, numbers):
    
    # Để tối ưu performance, ta sẽ tăng cường sử dụng hash map và bitwise
    length = len(empties)
    empties_list = list(empties)
    empties_dict = {empties_list[i]: i for i in range(length)}

    # bit_masks[n] = 00010 tức n là ô trống thứ 2; c & bit_masks[n] trả về bit thứ 2 của c
    bit_masks = {empties_list[i]: 1 << i for i in range(length)}

    numbers_sum = sum([numbers[pos] for pos in numbers.keys()])

    # # Hàm đệ quy giải bài toán: sử dụng DFS
    # def backtrack(solution_bits, assigned_len):
        
        






    # solution_bits = backtrack(solution_bits, assigned_len)
    
    # if solution_bits is None:
    #     return None
    
    # solution = [bool(solution_bits & (1 << i)) for i in range(length)]
    # print(f"Backtracking: {solution}")
    # model = [empties_list[i] if solution[i] else -empties_list[i] for i in range(length)]
    # return model

    # test
    a = is_conflict(KB, 0b1010, 4, empties_dict, bit_masks, numbers_sum)
    print(a)
    print(empties_dict)


    return None


            
            
        







