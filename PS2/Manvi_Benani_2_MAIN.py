import numpy as np

def read_matrix(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    matrix = []
    for line in lines[1:]:  # Skip the first line (column labels)
        row = list(map(float, line.strip().split(',')[1:]))  # Skip the row label and convert to float
        matrix.append(row)

    return matrix

def write_inverse_matrix(matrix, filename):
    N = len(matrix)
    
    with open(filename, 'w') as file:
        # Write column labels
        file.write("#,")
        file.write(','.join(map(str, range(N))) + '\n')
        
        # Write rows
        for i in range(N):
            # Write row label
            file.write(str(i) + ',')
            
            # Write elements in the row
            file.write(','.join(map(str, matrix[i])) + '\n')

def inverter():
    # Read matrix from inp.txt
    input_matrix = np.array(read_matrix('inp.txt'))

    # Calculate the inverse matrix
    try:
        inverse_matrix = np.linalg.inv(input_matrix)
        inverse_matrix = np.round(inverse_matrix, 3)
    except np.linalg.LinAlgError:
        print("The matrix is singular and cannot be inverted.")
        return

    # Write the inverse matrix to inv.txt
    write_inverse_matrix(inverse_matrix, 'inv.txt')

def main():
    inverter()

if __name__ == "__main__":
    main()

