import sys
from traceback import print_tb
sys.path.insert(1, '../data')

def main(vertices, edges, source_vertex):
    # print(vertices)
    # print(edges)
    # print(source_vertex)
    vertices_with_distances = set_initial_distances(source_vertex, vertices)
    vertices_with_successors = determine_successors(vertices, edges)
    full_vertices = merge_distances_and_successors(vertices_with_distances, vertices_with_successors)
    vertices_with_calculated_distances = calculate_distances(full_vertices)
    vertices_paths = discover_paths(vertices_with_calculated_distances, source_vertex)

    print('source', source_vertex)
    print('distances', vertices_with_calculated_distances)
    print('paths', vertices_paths)
    print('------------------------------------------------------------------\n')

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

# def merge_distances_and_successors(vertices_with_distances, vertices_with_successors):
#     full_vertices = {}
#     for dist_vertex, suc_vertex in zip(vertices_with_distances, vertices_with_successors):
#         full_vertices[dist_vertex[0]] = {'distance': dist_vertex[1], 'successors': suc_vertex[1]}
    
#     return full_vertices

def merge_distances_and_successors(vertices_with_distances, vertices_with_successors):
    full_vertices = {}
    for dist_vertex in vertices_with_distances:
        for suc_vertex in vertices_with_successors:
            if dist_vertex[0] == suc_vertex[0]:
                full_vertices[dist_vertex[0]] = {'distance': dist_vertex[1], 'successors': suc_vertex[1]}
    
    return full_vertices

def calculate_distances(full_vertices):
    visited, unvisited = prepare_initial_lists(full_vertices)

    for vertex in full_vertices:
        full_vertices[vertex]['last_predecessor'] = '-'

    for i in range(len(full_vertices)):
        current_vertex = find_vertex_with_min_dist(full_vertices, visited)
        for successor in full_vertices[current_vertex]['successors']:
            if successor in visited:
                pass
            else:
                if full_vertices[current_vertex]['distance'] + successor['cost'] < full_vertices[successor['vertex']]['distance']:
                    full_vertices[successor['vertex']]['distance'] = full_vertices[current_vertex]['distance'] + successor['cost']
                    full_vertices[successor['vertex']]['last_predecessor'] = current_vertex

        visited.append(current_vertex)
        unvisited.remove(current_vertex)

    vertices_with_calculated_distances = {}
    for vertex in full_vertices:
        vertices_with_calculated_distances[vertex] = {'distance': full_vertices[vertex]['distance'], 'last_predecessor': full_vertices[vertex]['last_predecessor']}

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