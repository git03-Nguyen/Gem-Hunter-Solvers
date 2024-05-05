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
