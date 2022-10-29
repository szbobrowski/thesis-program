import sys
sys.path.insert(1, '../data')

# import graph_creator
import graphs_example_data

def main():
    # vertices, edges = graph_creator.main()
    vertices, edges = graphs_example_data.main()
    empty_matrix = create_empty_matrix(vertices)
    initial_matrix = create_initial_matrix(empty_matrix, edges, vertices)
    final_matrix = calculate_distances(initial_matrix, vertices)

    for vertex in vertices:
        print(vertex, final_matrix[vertex])

def create_empty_matrix(vertices):
    empty_matrix = {}
    for vertex in vertices:
        empty_matrix[vertex] = {}
        for subvertex in vertices:
            empty_matrix[vertex][subvertex] = {'distance': 0, 'intermediator': '-'}

    return empty_matrix

def create_initial_matrix(empty_matrix, edges, vertices):
    initial_matrix = empty_matrix
    for vertex in vertices:
        for edge in edges:
            if edge[0] == vertex:
                initial_matrix[vertex][edge[1]] = {'distance': 1, 'intermediator': vertex}

    for row in initial_matrix:
        for column in initial_matrix[row]:
            if initial_matrix[row][column]['distance'] == 0 and row != column:
                initial_matrix[row][column] = {'distance': 1000, 'intermediator': '-'}

    return initial_matrix

def calculate_distances(initial_matrix, vertices):
    previous_matrix = initial_matrix
    for vertex in vertices:
        new_matrix = previous_matrix
        for row in previous_matrix:
            for column in previous_matrix[row]:
                if row == vertex or column == vertex or row == column:
                    pass
                else:
                    if previous_matrix[row][column]['distance'] > previous_matrix[row][vertex]['distance'] + previous_matrix[vertex][column]['distance']:
                        new_matrix[row][column]['distance'] = previous_matrix[row][vertex]['distance'] + previous_matrix[vertex][column]['distance']
                        new_matrix[row][column]['intermediator'] = vertex

        previous_matrix = new_matrix

    return new_matrix

main()