# Description: Định nghĩa hàm giải bài toán Gem Hunter bằng thuật toán Bruteforce

def is_valid(KB, case, empties, bit_masks):
    for clause in KB:
        is_clause_true = False
        for literal in clause:
            if literal in empties:
                if case & bit_masks[literal]:
                    is_clause_true = True
                    break
            elif -literal in empties:
                if not case & bit_masks[-literal]:
                    is_clause_true = True
                    break
        if not is_clause_true:
            return False
    return True

# Giải bằng bruteforce
def solve_by_bruteforce(KB, empties, numbers):

    numbers_sum = sum([numbers[pos] for pos in numbers.keys()])

    # Tạo tất cả các trường hợp có thể của các biến chưa biết
    # => 2^k trường hợp (do mỗi biến có 2 giá trị "T" hoặc "G")
    length = len(empties)

    # Để tối ưu performance, ta sẽ tăng cường sử dụng hash map và bitwise
    empties_list = list(empties)
    bit_masks = {empties_list[i]: 1 << i for i in range(length)}

    start = 0
    end = 1 << length # 2^length
    for c in range(start, end):

        if c % 10000000 == 0 and c > 0:
                print(f"Processing to case {c}...")

        # Nếu sum_số > 8*num_traps thì bỏ qua
        if numbers_sum > (c.bit_count() << 3):
            continue

        # Kiểm tra xem trường hợp này có phải là trường hợp đúng không
        if is_valid(KB, c, empties, bit_masks):
            case = [bool(c & (1 << i)) for i in range(length)]
            model = [empties_list[i] if case[i] else -empties_list[i] for i in range(length)]
            return model
    
    return None
