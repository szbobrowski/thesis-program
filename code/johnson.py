import sys
sys.path.insert(1, '../data')

import graph_creator
import graphs_example_data

def main():
    vertices, edges = graph_creator.main()
    vertices, edges = graphs_example_data.main()
    vertices_with_dummy, edges_with_dummy = add_new_vertex(vertices, edges)
    reweighted_values = run_bellman_ford(vertices_with_dummy, edges_with_dummy, vertices_with_dummy[0])
    reweighted_edges = reweight_edges(edges, reweighted_values)
    matrix_before_reweight = run_dijkstra(vertices, reweighted_edges)
    final_matrix = reweight_edges_back(matrix_before_reweight, reweighted_values)
    
    for vertex in vertices:
        print(vertex, final_matrix[vertex])
    
def add_new_vertex(vertices, edges):
    vertices_with_dummy = vertices[:]
    edges_with_dummy = edges[:]
    dummy_vertex = 'DUMMY_VERTEX'
    for vertex in vertices_with_dummy:
        edges_with_dummy.append([dummy_vertex, vertex, 0])

    vertices_with_dummy.insert(0, dummy_vertex)

    return vertices_with_dummy, edges_with_dummy

def reweight_edges(edges, reweighted_values):
    reweighted_edges = []
    for edge in edges:
        new_cost = edge[2] + reweighted_values[edge[0]] - reweighted_values[edge[1]]
        reweighted_edges.append([edge[0], edge[1], new_cost])

    return reweighted_edges

def reweight_edges_back(matrix_before_reweight, reweighted_values):
    final_matrix = matrix_before_reweight
    for row in matrix_before_reweight:
        for column in matrix_before_reweight[row]:
            if final_matrix[row][column]['distance'] != 1000:
                final_matrix[row][column]['distance'] = matrix_before_reweight[row][column]['distance'] + reweighted_values[column] - reweighted_values[row]

    return final_matrix

def run_bellman_ford(vertices_with_dummy, edges_with_dummy, source_vertex):
    vertices_with_distances = set_initial_distances(source_vertex, vertices_with_dummy)
    vertices_with_predecessors = determine_predecessors(vertices_with_dummy, edges_with_dummy)
    full_vertices = merge_distances_and_predecessors(vertices_with_distances, vertices_with_predecessors)
    vertices_with_calculated_distances = calculate_distances_with_bellman_ford(full_vertices)
    del vertices_with_calculated_distances['DUMMY_VERTEX']
    return vertices_with_calculated_distances

def determine_predecessors(vertices, edges):
    vertices_with_predecessors = []
    for vertex in vertices:
        predecessors = []
        for edge in edges:
            if edge[1] == vertex:
                predecessors.append({'vertex': edge[0], 'cost': edge[2]})

        vertices_with_predecessors.append([vertex, predecessors])

    return vertices_with_predecessors

def merge_distances_and_predecessors(vertices_with_distances, vertices_with_predecessors):
    full_vertices = {}
    for dist_vertex, pre_vertex in zip(vertices_with_distances, vertices_with_predecessors):
        full_vertices[dist_vertex[0]] = {'distance': dist_vertex[1], 'predecessors': pre_vertex[1]}
    
    return full_vertices

def calculate_distances_with_bellman_ford(full_vertices):
    num_of_iterations = len(full_vertices) - 1

    for i in range(num_of_iterations):
        for vertex in full_vertices:
            for predecessor in full_vertices[vertex]['predecessors']:
                if (full_vertices[predecessor['vertex']]['distance'] + predecessor['cost']) < full_vertices[vertex]['distance']:
                    full_vertices[vertex]['distance'] = full_vertices[predecessor['vertex']]['distance'] + predecessor['cost']

    vertices_with_calculated_distances = {}
    for vertex in full_vertices:
        vertices_with_calculated_distances[vertex] = full_vertices[vertex]['distance']

    return vertices_with_calculated_distances

def run_dijkstra(vertices, reweighted_edges):
    matrix_before_reweight = {}
    vertices_copy = vertices[:]

    for i in range(len(vertices)):
        vertices_copy[0], vertices_copy[i] = vertices_copy[i], vertices_copy[0]
        source_vertex = vertices_copy[0]
        vertices_with_distances = set_initial_distances(source_vertex, vertices_copy)
        vertices_with_successors = determine_successors(vertices_copy, reweighted_edges)
        full_vertices = merge_distances_and_successors(vertices_with_distances, vertices_with_successors)
        vertices_with_calculated_distances = calculate_distances_with_dijkstra(full_vertices)
        matrix_before_reweight[source_vertex] = vertices_with_calculated_distances

    return matrix_before_reweight
        

def set_initial_distances(source_vertex, vertices):
    vertices_with_distances = []
    vertices_with_distances.append([source_vertex, 0])
    for vertex in vertices:
        if vertex != source_vertex:
            vertices_with_distances.append([vertex, 1000])

    return vertices_with_distances

def determine_successors(vertices, edges):
    vertices_with_successors = []
    for vertex in vertices:
        successors = []
        for edge in edges:
            if edge[0] == vertex:
                successors.append({'vertex': edge[1], 'cost': edge[2]})

        vertices_with_successors.append([vertex, successors])

    return vertices_with_successors

def merge_distances_and_successors(vertices_with_distances, vertices_with_successors):
    full_vertices = {}
    for dist_vertex, suc_vertex in zip(vertices_with_distances, vertices_with_successors):
        full_vertices[dist_vertex[0]] = {'distance': dist_vertex[1], 'successors': suc_vertex[1]}
    
    return full_vertices

def calculate_distances_with_dijkstra(full_vertices):
    visited, unvisited = prepare_initial_lists(full_vertices)

    for vertex in full_vertices:
        full_vertices[vertex]['intermediator'] = '-'

    for i in range(len(full_vertices)):
        current_vertex = find_vertex_with_min_dist(full_vertices, visited)
        for successor in full_vertices[current_vertex]['successors']:
            if successor in visited:
                pass
            else:
                if full_vertices[current_vertex]['distance'] + successor['cost'] < full_vertices[successor['vertex']]['distance']:
                    full_vertices[successor['vertex']]['distance'] = full_vertices[current_vertex]['distance'] + successor['cost']
                    full_vertices[successor['vertex']]['intermediator'] = current_vertex

        visited.append(current_vertex)
        unvisited.remove(current_vertex)

    vertices_with_calculated_distances = {}
    for vertex in full_vertices:
        # vertices_with_calculated_distances[vertex] = full_vertices[vertex]['distance']
        vertices_with_calculated_distances[vertex] = {'distance': full_vertices[vertex]['distance'], 'intermediator': full_vertices[vertex]['intermediator']}

    return vertices_with_calculated_distances

def prepare_initial_lists(full_vertices):
    visited = []
    unvisited = []
    for vertex in full_vertices:
        unvisited.append(vertex)

    return visited, unvisited

def find_vertex_with_min_dist(full_vertices, visited):
    min_dist = 2000
    for vertex in full_vertices:
        if vertex in visited:
            pass
        elif full_vertices[vertex]['distance'] < min_dist:
            min_dist = full_vertices[vertex]['distance']
            min_vertex = vertex

    return min_vertex

main()