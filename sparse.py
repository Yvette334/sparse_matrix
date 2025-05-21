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

def size(a, b, operation):
    # size of the matrix
    if operation in ('add', 'subtract'):
        if a.rows != b.rows or a.cols != b.cols:
            raise ValueError("Matrix sizes don't match for this operation")
    elif operation == 'multiply':
        if a.cols != b.rows:
            raise ValueError("Columns of first matrix must match rows of second matrix for multiplication")

def add(a, b):
    size(a, b, 'add')
    result = sparsematrix(a.rows, b.cols)
    
    for (row, col), value in a.ez():
        result.vs(row, col, value)
    
    for (row, col), value in b.ez():
        result.vs(row, col, result.gvalue(row, col) + value)
    
    return result

def sub(a, b):
    size(a, b, 'subtract')
    result = sparsematrix(a.rows, b.cols)
    
    for (row, col), value in a.ez():
        result.vs(row, col, value)
    
    for (row, col), value in b.ez():
        result.vs(row, col, result.gvalue(row, col) - value)
    
    return result

def transpose_matrix(matrix):
    #  transposed of the matrix
    result = sparsematrix(matrix.cols, matrix.rows)
    
    for (row, col), value in matrix.ez():
        result.vs(col, row, value)
    
    return result

def mult(a, b):
    # multiply
    result = sparsematrix(a.rows, b.cols)
    
    # Group b elements by row for faster access
    b_by_row = {}
    for (row, col), value in b.ez():
        if row not in b_by_row:
            b_by_row[row] = []
        b_by_row[row].append((col, value))
    
    # For each non-zero element in a
    for (row1, col1), value1 in a.ez():
        # Any non-zero elements in the corresponding row of b
        if col1 in b_by_row:
            # Non-zero element in that row of b
            for col2, value2 in b_by_row[col1]:
                # Update position (row1, col2)
                current = result.gvalue(row1, col2)
                result.vs(row1, col2, current + value1 * value2)
    
    return result

    # force mult
def force_mult(a, b):
    
    # Do first multi
    try:
        # Check if it is  compatible for multiplication
        if a.cols == b.rows:
            return mult(a, b)
    except:
        pass
    
    # Transpose b for compatiblity
    if a.cols == b.cols:
        print("multiplying take time...")
        transposed_b = transpose_matrix(b)
        return mult(a, transposed_b)
    
    # make dimensions compatible
    elif a.rows == b.rows:
        transposed_a = transpose_matrix(a)
        result = mult(transposed_a, b)
        # Transpose result back to maintain expected dimensions
        return transpose_matrix(result)
    
    else:
        # Use the smaller dimensions for the result
        rows = min(a.rows, b.rows)
        cols = min(a.cols, b.cols)
        result = sparsematrix(rows, cols)
        
        # Multiply data
        for (row1, col1), value1 in a.ez():
            if row1 < rows and col1 < cols:
                value2 = b.gvalue(row1, col1)
                if value2 != 0:
                    result.vs(row1, col1, value1 * value2)
        
        return result
