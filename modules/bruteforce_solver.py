# Description: Định nghĩa hàm giải bài toán Gem Hunter bằng thuật toán Bruteforce

from modules.utils import padding, to_1D

# ---------------------------------------------
# Check
def is_valid(case, numbers_dict, numbers_around_dict, bit_masks_dict):
    for (x, y) in numbers_around_dict.keys():
        num = numbers_dict[(x, y)]
        count = 0
        for xx, yy in numbers_around_dict[(x, y)]: 
            if case & bit_masks_dict[(xx, yy)]:
                count += 1
                if count > num:
                    return False
        if count != num:
            return False
    return True
# ---------------------------------------------
def loop(unknowns, unknowns_dict, numbers_dict, numbers_sum, start, end):
    length = len(unknowns)
    bit_masks_dict = {(x, y): 1 << i for i, (x, y) in enumerate(unknowns_dict.keys())}
    numbers_around_dict = {}
    for (x, y) in numbers_dict.keys():
        numbers_around_dict[(x, y)] = set()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            xx = x + dx
            yy = y + dy
            if (xx, yy) in unknowns_dict.keys():
                numbers_around_dict[(x, y)].add((xx, yy))

    for c in range(start, end):

        if c % 1000000 == 0:
            if c > 0:
                print(f"Case {c}")

        # Nếu sum_số > 8*num_traps thì bỏ qua
        if numbers_sum > (c.bit_count() << 3):
            continue

        # Kiểm tra xem trường hợp này có phải là trường hợp đúng không
        if is_valid(c, numbers_dict, numbers_around_dict, bit_masks_dict):
            case = [bool(c & (1 << i)) for i in range(length)]
            print(f"Satisfiable (No.{c}): {case}")
            return [unknowns[i] if case[i] else -unknowns[i] for i in range(length)]

    return None

# Giải bằng bruteforce
def solve_by_bruteforce(matrix):
    # true_case = 3219758312 # for testing

    matrix = padding(matrix)

    # Tìm tất cả các biến không xác định
    n = len(matrix)
    m = len(matrix[0])
    unknowns = []
    unknowns_pos = []
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if matrix[i][j] is None:
                unknowns.append(to_1D((i - 1, j - 1), m - 2))
                unknowns_pos.append((i, j))
    
    unknowns_dict = {unknowns_pos[i]: i for i in range(len(unknowns_pos))}
    print(f"Unknowns ({len(unknowns)}) : {unknowns}")

    numbers_dict = [(i, j) for i in range(n) for j in range(m) if type(matrix[i][j]) == int]
    numbers_dict = {pos: matrix[pos[0]][pos[1]] for pos in numbers_dict}
    numbers_sum = sum([matrix[pos[0]][pos[1]] for pos in numbers_dict])

    # Tạo tất cả các trường hợp có thể của các biến không xác định 
    # => 2^k trường hợp (do mỗi biến có 2 giá trị "T" hoặc "G")
    length = len(unknowns)
    start = 0
    end = 1 << length
    model = loop(unknowns, unknowns_dict, numbers_dict, numbers_sum, start, end)
    
    return model
