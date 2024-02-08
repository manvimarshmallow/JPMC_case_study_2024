def graph_formation(merge_history):
    nodes = set(
        tuple(item) for sublist in merge_history for item in sublist
    )  
    # Finding the unqiue nodes (that is all clusters)
    node_mapping = {
        node: i for i, node in enumerate(nodes)
    }  
    # Assigning all clusters a unique number
    graph = [
        [] for _ in range(len(nodes))
    ]  
    # Will contain only pointers from child to parent (unique)
    child_graph = [
        [] for _ in range(len(nodes))
    ]  
    # Will contain only pointers from parent to child

    for level_clusters, level in enumerate(merge_history):
        if level_clusters == 0: 
            # The first level in history (reversed) is already zero
            continue
        for cluster in level:  
            # For all clusters in this level
            if (
                cluster not in merge_history[level_clusters - 1]
            ):  
                # If there is no cluster in above level -> this cluster split from its parent
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
                child_graph[node_mapping[tuple(parent_cluster[0])]].append(
                    node_mapping[tuple(cluster)]
                )
    return child_graph, graph, nodes, node_mapping


def find_lca(graph, u, v):
    # LCA Node is found easily, keep on following the parent pointers
    path_u = []
    path_v = []

    def find_path(node, path):
        ## Till you can't find it anymore, the root node (topmost one) has no parent so it's list parent list is empty which is the breaking criterion
        ## This code does that only
        while True:
            path.append(node)
            node = graph[node]
            if node == []:
                break
            else:
                node = node[0]

    ## Finding the path till the top for both leaf nodes
    find_path(u, path_u)
    find_path(v, path_v)

    common_ancestor = None

    ## Iterating through the lists of paths reversed, and diverging at the point where they don't match
    ## [0, 4, 1, 7] [2, 1, 7] Like in this reversed would go 7(common)->1(common) -> 4 =/= 2 and break at 1 which is the last common node
    for node_u, node_v in zip(reversed(path_u), reversed(path_v)):
        if node_u == node_v:
            common_ancestor = node_u
        else:
            break

    return common_ancestor


def read_matrix(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    matrix = []
    for line in lines[1:]:  
        # Skip the first line (column labels)
        row = list(
            map(float, line.strip().split(",")[1:])
        )  
        # Skip the row label and convert to float
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
    cluster_function( matrix, clusters, merge_history)


def fill_hierarchical_matrix(matrix, cluster1, cluster2):
    # Going through all values in the cluster and finding the min, matrix is the input matrix
    min_distance = float("inf")
    for i in cluster1:
        for j in cluster2:
            min_distance = min(min_distance, matrix[i][j])
    return min_distance

def print_matrix(matrix, filename):
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

def main():
    input_matrix = read_matrix("./inp.txt")
    
    clusters = []
    n = input_matrix[0]
    for i in range(len(n)):
        clusters.append([i])

    merge_history = []
    copy_clusters = [sublist[:] for sublist in clusters]
    merge_history.append(copy_clusters)

    cluster_function( input_matrix, clusters, merge_history)

    merge_history = merge_history[::-1]  # Reversing History

    child_graph, graph, nodes, node_mapping = graph_formation(
        merge_history
    )  
    # Explained in above function
    reversed_mapping = {
        index: node for node, index in node_mapping.items()
    }  
    # Creating a reverse mapping from unique number to each cluster
    # print(graph)
    # print(child_graph)

    # Counting all nodes
    all_nodes = range(len(graph))

    # Rereading input as previous messed up (to be improved)
    input_matrix = read_matrix("./inp.txt")
    hierarchical_matrix = [[0.0] * len(input_matrix) for _ in range(len(input_matrix))]
    for u in all_nodes:
        for v in all_nodes:
            # u, v are the unique identifiers for each cluster in the graph, reversed_mapping gives the actual value of the cluster
            # We find lca only for leaf nodes which have only a single element
            if (
                u < v
                and len(reversed_mapping[u]) == 1
                and len(reversed_mapping[v]) == 1
            ):
                lca = find_lca(graph, u, v)
                # Finding the descendants for the lca node
                child1, child2 = child_graph[lca]
                node1 = reversed_mapping[u][0]
                node2 = reversed_mapping[v][0]

                # Using this child clusters, forming the matrix as explained above and in pdf
                hierarchical_matrix[node1][node2] = fill_hierarchical_matrix(
                    input_matrix, reversed_mapping[child1], reversed_mapping[child2]
                )
                hierarchical_matrix[node2][node1] = hierarchical_matrix[node1][node2]
                # print(f"LCA for {node1} and {node2}: {reversed_mapping[lca]}")

    print_matrix(hierarchical_matrix,'hDist.txt')


if __name__ == "__main__":
    main()
