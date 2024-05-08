# Description: Module này chứa các hàm đọc và ghi input, output

# ---------------------------------------------
# Hàm input_matrix(file_name) đọc ma trận từ file input
def input_matrix(file_name = "./testcases/input.txt"):
    '''Đọc ma trận và ktra input từ file, với:
      - "_" là ô trống
      - "T" là ô có bẫy
      - "G" là ô có ngọc
      - Số từ 0-8 là số lượng bẫy xung quanh ô đó

      Cách nhau bởi dấu phẩy và khoảng trắng.
    '''
    with open(file_name, 'r') as f:
        lines = f.readlines()
        matrix = []
        for line in lines:
            row = []
            for x in line.split(","):
                x = x.strip()
                if x == "_":
                    row.append(None)
                elif x == "T":
                    row.append("T")
                elif x == "G":
                    row.append("G")
                elif x.isnumeric():
                    x = int(x)
                    if x < 0 or x > 8: raise ValueError("Invalid input")
                    row.append(int(x))
                else:
                    raise ValueError("Invalid input")
            matrix.append(row)
        return matrix

# ---------------------------------------------  
# Hàm output_matrix(matrix, file_name) ghi ma trận ra file output
def output_matrix(matrix, file_name = "./testcases/output.txt"):
    '''Ghi ma trận ra file output, với:
      - "_" là ô trống
      - "T" là ô có bẫy
      - "G" là ô có ngọc
      - Số từ 0-8 là số lượng bẫy xung quanh ô đó

      Cách nhau bởi dấu phẩy và khoảng trắng ", ".
    '''
    with open(file_name, 'w') as f:
        for row in matrix:
            f.write(", ".join([str(x) if x is not None else "_" for x in row]) + "\n")

# ---------------------------------------------
# Hàm xuất CNFs ra file
def output_CNFs(KB, file_name = "./testcases/CNFs.txt"):
    '''Ghi CNFs ra file, mỗi dòng là một clause, mỗi literal cách nhau bởi dấu cách " ".
    '''
    with open(file_name, 'w') as f:
        for clause in KB:
            f.write(" ".join([str(x) for x in clause]) + "\n")


# ---------------------------------------------
# Hàm in 2 ma trận cùng kích thước lên 2 cột
def print_2matrix(matrix1, matrix2):
    str_matrix = ""
    if matrix2 is None:
        # In ra ma trận 1, bên cạnh là ma trận 2 với None
        for r1 in matrix1:
            str_matrix += ", ".join([str(x) if x is not None else "_" for x in r1]) + "  |  " + ", ".join(["_" for _ in range(len(r1))]) + "\n"
        return str_matrix
    else:
        for r1, r2 in zip(matrix1, matrix2):
            str_matrix += ", ".join([str(x) if x is not None else "_" for x in r1]) + "  |  " + ", ".join([str(x) if x is not None else "_" for x in r2]) + "\n"
        return str_matrix

        

