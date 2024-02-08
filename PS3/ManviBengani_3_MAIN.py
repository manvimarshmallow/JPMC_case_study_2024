def read_matrix(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    matrix = []
    for line in lines[1:]:  # Skip the first line (column labels)
        row = list(
            map(float, line.strip().split(",")[1:])
        )  # Skip the row label and convert to float
        matrix.append(row)

    return matrix


def write_matrix(matrix, clusters, filename):
    N = len(matrix)

    with open(filename, "a") as file:
        # Write column labels
        file.write("#,")
        for i in range(N):
            if len(clusters[i]) > 1:
                file.write("(")
            file.write(",".join(map(str, clusters[i])))
            if len(clusters[i]) > 1:
                file.write(")")
            if i is not N - 1:
                file.write(",")

        file.write("\n")
        # Write rows
        for i in range(N):
            # Write row label
            if len(clusters[i]) > 1:
                file.write("(")
            file.write(",".join(map(str, clusters[i])))
            if len(clusters[i]) > 1:
                file.write("),")
            else:
                file.write(",")
            # Write elements in the row
            # file.write(",".join(map(str, matrix[i])) + "\n")
            rounded_row = [round(element, 3) for element in matrix[i]]
            file.write(",".join(map(str, rounded_row)) + "\n")


def find_min_position(matrix):
    if not matrix:
        return None  # Return None for an empty matrix

    min_value = matrix[0][1]
    min_row, min_col = 0, 1

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] < min_value and i < j:
                min_value = matrix[i][j]
                min_row, min_col = i, j
    return min_row, min_col


def cluster_function( matrix, clusters, merge_history):
    write_matrix(matrix, clusters, "intermediateDistMats.txt")
    if len(matrix[0]) == 1:
        return merge_history
    row_i, row_j = find_min_position(matrix)
    min_values = [
        min(matrix[row_i][col], matrix[row_j][col]) for col in range(len(matrix[0]))
    ]
    matrix[row_i] = min_values
    for i in range(len(matrix)):
        matrix[i][row_i] = min_values[i]
    del matrix[row_j]
    for row in matrix:
        del row[row_j]

    clusters[row_i].extend(clusters[row_j])
    clusters[row_i] = sorted(clusters[row_i])
    clusters.pop(row_j)
    copy_clusters = [sublist[:] for sublist in clusters]
    merge_history.append(copy_clusters)
    cluster_function( matrix, clusters, merge_history)


def part3():
    input_filename = "./inp.txt"
    input_matrix = read_matrix(input_filename)
    
    clusters = []
    merge_history = []
    # Making initial clusters
    for i in range(len(input_matrix[0])):
        clusters.append([i])
    copy_clusters = [sublist[:] for sublist in clusters]
    merge_history.append(copy_clusters)
    
    cluster_function(input_matrix, clusters, merge_history)
    


def main():
    part3()


if __name__ == "__main__":
    main()
