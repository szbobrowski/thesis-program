import sys
sys.path.insert(1, '../data')

import graph_creator

def main():
    vertices, edges = graph_creator.main()
    source_vertex = vertices[0]
    vertices_with_distances = set_initial_distances(source_vertex, vertices)
    vertices_with_predecessors = determine_predecessors(vertices, edges)
    full_vertices = merge_distances_and_predecessors(vertices_with_distances, vertices_with_predecessors)
    vertices_with_calculated_distances = calculate_distances(full_vertices)
    vertices_paths = discover_paths(vertices_with_calculated_distances, source_vertex)

def set_initial_distances(source_vertex, vertices):
    vertices_with_distances = []
    vertices_with_distances.append([source_vertex, 0])
    for vertex in vertices:
        if vertex != source_vertex:
            vertices_with_distances.append([vertex, 1000])

    return vertices_with_distances

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

def calculate_distances(full_vertices):
    num_of_iterations = len(full_vertices) - 1
    for vertex in full_vertices:
        full_vertices[vertex]['last_predecessor'] = '-'

    for i in range(num_of_iterations):
        for vertex in full_vertices:
            for predecessor in full_vertices[vertex]['predecessors']:
                if (full_vertices[predecessor['vertex']]['distance'] + predecessor['cost']) < full_vertices[vertex]['distance']:
                    full_vertices[vertex]['distance'] = full_vertices[predecessor['vertex']]['distance'] + predecessor['cost']
                    full_vertices[vertex]['last_predecessor'] = predecessor

    vertices_with_calculated_distances = {}
    for vertex in full_vertices:
        if full_vertices[vertex]['last_predecessor'] != '-':
            last_predecessor = full_vertices[vertex]['last_predecessor']['vertex']
        else:
            last_predecessor = '-'

        vertices_with_calculated_distances[vertex] = {'distance': full_vertices[vertex]['distance'], 'last_predecessor': last_predecessor}

    return vertices_with_calculated_distances

def discover_paths(vertices_with_calculated_distances, source_vertex):
    vertices_paths = []
    for vertex in vertices_with_calculated_distances:
        current_vertex = vertex
        path = [current_vertex]
        while True:
            if current_vertex == source_vertex:
                break
            elif vertices_with_calculated_distances[current_vertex]['last_predecessor'] == '-' and current_vertex != source_vertex:
                path = []
                break
            else:
                current_vertex = vertices_with_calculated_distances[current_vertex]['last_predecessor']
                path.append(current_vertex)

        path.reverse()
        vertices_paths.append({vertex: path})

    return vertices_paths