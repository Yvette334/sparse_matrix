class sparsematrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.elements = {}  # Stores elements

    def vs(self, row, col, value):
        #value set
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            
            del self.elements[(row, col)]  

    def gvalue(self, row, col):
        # get value from its position
        return self.elements.get((row, col), 0)

    def ez(self):
        # Get all non-zero elements
        return self.elements.items()

def read(filename):
    # Read matrix from file
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    
    rows = int(lines[0].split('=')[1])
    cols = int(lines[1].split('=')[1])
    matrix = sparsematrix(rows, cols)
    
    for line in lines[2:]:
        row, col, value = map(int, line[1:-1].split(','))
        matrix.vs(row, col, value)
    
    return matrix

def save(matrix, filename):
    # Save file
    with open(filename, 'w') as file:
        file.write(f"rows={matrix.rows}\n")
        file.write(f"cols={matrix.cols}\n")
        for (row, col), value in sorted(matrix.ez()):
            file.write(f"({row},{col},{value})\n")

def size(matrix1, matrix2, operation):
    # size of the matrix
    if operation in ('add', 'subtract'):
        if matrix1.rows != matrix2.rows or matrix1.cols != matrix2.cols:
            raise ValueError("Matrix sizes don't match for this operation")
    elif operation == 'multiply':
        if matrix1.cols != matrix2.rows:
            raise ValueError("Columns of first matrix must match rows of second matrix for multiplication")

def add(matrix1, matrix2):
    size(matrix1, matrix2, 'add')
    result = sparsematrix(matrix1.rows, matrix1.cols)
    
    for (row, col), value in matrix1.ez():
        result.vs(row, col, value)
    
    for (row, col), value in matrix2.ez():
        result.vs(row, col, result.gvalue(row, col) + value)
    
    return result

def sub(matrix1, matrix2):
    size(matrix1, matrix2, 'subtract')
    result = sparsematrix(matrix1.rows, matrix1.cols)
    
    for (row, col), value in matrix1.ez():
        result.vs(row, col, value)
    
    for (row, col), value in matrix2.ez():
        result.vs(row, col, result.gvalue(row, col) - value)
    
    return result

def transpose_matrix(matrix):
    #  transposed of the matrix
    result = sparsematrix(matrix.cols, matrix.rows)
    
    for (row, col), value in matrix.ez():
        result.vs(col, row, value)
    
    return result

def mult(matrix1, matrix2):
    # multiply
    result = sparsematrix(matrix1.rows, matrix2.cols)
    
    # Group matrix2 elements by row for faster access
    matrix2_by_row = {}
    for (row, col), value in matrix2.ez():
        if row not in matrix2_by_row:
            matrix2_by_row[row] = []
        matrix2_by_row[row].append((col, value))
    
    # For each non-zero element in matrix1
    for (row1, col1), value1 in matrix1.ez():
        # Any non-zero elements in the corresponding row of matrix2
        if col1 in matrix2_by_row:
            # Non-zero element in that row of matrix2
            for col2, value2 in matrix2_by_row[col1]:
                # Update position (row1, col2)
                current = result.gvalue(row1, col2)
                result.vs(row1, col2, current + value1 * value2)
    
    return result

    # force mult
def force_mult(matrix1, matrix2):
    
    # Do first multi
    try:
        # Check if it is  compatible for multiplication
        if matrix1.cols == matrix2.rows:
            return mult(matrix1, matrix2)
    except:
        pass
    
    # If the dimensions don't match
    print(f"Note: Matrix dimensions don't match for standard multiplication.")
    print(f"Matrix 1: {matrix1.rows}x{matrix1.cols}, Matrix 2: {matrix2.rows}x{matrix2.cols}")
    
    # Transpose matrix2 for compatiblity
    if matrix1.cols == matrix2.cols:
        print("Transposing second matrix to make multiplication possible...")
        transposed_matrix2 = transpose_matrix(matrix2)
        return mult(matrix1, transposed_matrix2)
    
    # make dimensions compatible
    elif matrix1.rows == matrix2.rows:
        print("Transposing first matrix to make multiplication possible...")
        transposed_matrix1 = transpose_matrix(matrix1)
        result = mult(transposed_matrix1, matrix2)
        # Transpose result back to maintain expected dimensions
        return transpose_matrix(result)
    
    else:
        print("Using element-wise multiplication (Hadamard product)...")
        # Use the smaller dimensions for the result
        rows = min(matrix1.rows, matrix2.rows)
        cols = min(matrix1.cols, matrix2.cols)
        result = sparsematrix(rows, cols)
        
        # Multiply data
        for (row1, col1), value1 in matrix1.ez():
            if row1 < rows and col1 < cols:
                value2 = matrix2.gvalue(row1, col1)
                if value2 != 0:
                    result.vs(row1, col1, value1 * value2)
        
        return result
