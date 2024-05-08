# Description: Định nghĩa hàm giải bài toán Gem Hunter bằng thuật toán Bruteforce

def is_valid(KB, case, empties, bit_masks):
    # Có chứa một clause nào mà không thoả mãn thì trả về True
    # Clause không thoả mãn khi tất cả các literal đều False
    for clause in KB:
        is_clause_true = False
        for literal in clause:
            # Nếu từ KB yêu cầu biến True
            if literal > 0 and case & bit_masks[literal]: # Case này gán True thì clause True
                is_clause_true = True
                break  
            # Nếu từ KB yêu cầu biến False
            elif literal < 0 and not case & bit_masks[-literal]: # Case này gán False thì clause True
                is_clause_true = True
                break 
        if not is_clause_true:
            return False
    return True

# Giải bằng bruteforce
def solve_by_bruteforce(KB, empties):

    # Tạo tất cả các trường hợp có thể của các biến chưa biết
    # => 2^k trường hợp (do mỗi biến có 2 giá trị "T" hoặc "G")
    length = len(empties)

    # Để tối ưu performance, ta sẽ tăng cường sử dụng hash map và bitwise
    empties_list = list(empties)
    bit_masks = {empties_list[i]: 1 << i for i in range(length)}

    start = 0
    end = 1 << length
    # 2^20-1 = 1048575, 2^24-1 = 16777215, 2^27-1 = 134217727

    for c in range(start, end):

        if c & 1048575 == 0:
                print(f"Processing to case {c}...")

        # Nếu num_traps < sum_số/8 thì bỏ qua
        # if c < c.bit_count() < sum_div_8:
        #     continue

        # # Kiểm tra xem trường hợp này có phải là trường hợp đúng không
        if is_valid(KB, c, empties, bit_masks):
            case = [bool(c & (1 << i)) for i in range(length)]
            model = [empties_list[i] if case[i] else -empties_list[i] for i in range(length)]
            return model
    
    return None


