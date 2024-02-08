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
    if len(matrix[0]) == 1:
        return  merge_history
    
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
    cluster_function(matrix, clusters, merge_history)

def print_dendrogram(sorted_node_levels):
    curr_level = 0
    all_nodes = []
    with open("dendrogram.txt", "w") as file:
        ## Printing the dendogram based on the level and the bs pattern they want
        for node, level in sorted_node_levels.items():
            if level == curr_level:
                all_nodes.append(node)
            else:
                all_nodes = sorted(all_nodes)
                file.write(
                    " ".join(
                        [
                            str(i[0]) if len(i) == 1 else str(tuple(i)).replace(" ", "")
                            for i in all_nodes
                        ]
                    )
                )
                file.write("\n")
                curr_level = level
                all_nodes = [node]
        all_nodes = sorted(all_nodes)
        # PRINT REMAINING NODES
        file.write(
            " ".join(
                [
                    str(i[0]) if len(i) == 1 else str(tuple(i)).replace(" ", "")
                    for i in all_nodes
                ]
            )
        )

def find_levels(nodes, graph, node_mapping):
    ## As explained, reversed mapping reverses the unique number back to its cluster
    reversed_mapping = {index: node for node, index in node_mapping.items()}

    ## Finding the node levels of each cluster, by going to the parent, parent would not have any parent and break the loop
    node_levels = {}
    for node in nodes:
        level = 0
        curr_node = node
        while True:
            parent = graph[node_mapping[tuple(curr_node)]]
            if parent:
                curr_node_index = parent[0]
                # print(curr_node_index)
                curr_node = reversed_mapping[curr_node_index]
                # print(curr_node)
                level += 1
            else:
                break
        node_levels[node] = level

    ## Sorting all clusters based on their levels
    sorted_node_levels = dict(sorted(node_levels.items(), key=lambda x: x[1]))
    return sorted_node_levels


def graph_formation(merge_history):
    nodes = set(
        tuple(item) for sublist in merge_history for item in sublist
    )  # Finding the unqiue nodes (that is all clusters)
    node_mapping = {
        node: i for i, node in enumerate(nodes)
    } 
    print(node_mapping)
    # Assigning all clusters a unique number
    graph = [
        [] for _ in range(len(nodes))
    ]  # Will contain only pointers from child to parent (unique)

    for level_clusters, level in enumerate(merge_history):
        if level_clusters == 0:  # The first level in history (reversed) is already zero
            continue
        for cluster in level:  # For all clusters in this level
            if (
                cluster not in merge_history[level_clusters - 1]
            ):  # If there is no cluster in above level -> this cluster split from its parent
                # Find the parent by going through all clusters in above level and checking for one single common element
                parent_cluster = [
                    parent_cluster
                    for parent_cluster in merge_history[level_clusters - 1]
                    if any(item in parent_cluster for item in cluster)
                ]

                # Forming the child to parent link
                graph[node_mapping[tuple(cluster)]].append(
                    node_mapping[tuple(parent_cluster[0])]
                )
                # Forming the parent to child link
                print(graph)
    return graph, nodes, node_mapping


def part4():
    input_matrix = read_matrix("./inp.txt")
    clusters = []
    for i in range(len(input_matrix[0])):
        clusters.append([i])
    merge_history = []
    copy_clusters = [sublist[:] for sublist in clusters]
    merge_history.append(copy_clusters)
    cluster_function(input_matrix, clusters, merge_history)
    merge_history = merge_history[::-1]  ## Reversing history
    for i in merge_history:
        print(i)
    ## Forming graph, read above
    graph, nodes, node_mapping = graph_formation(merge_history)

    sorted_node_levels = find_levels(nodes, graph, node_mapping)
    print_dendrogram(sorted_node_levels)


def main():
    part4()


if __name__ == "__main__":
    main()
