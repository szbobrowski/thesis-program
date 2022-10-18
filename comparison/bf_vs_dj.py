import time
import network_generator
import graph_creator
import bellman_ford
import dijkstra

NUM_OF_NETWORKS = 12
NUM_OF_ROUTERS = 50
MIN_NUM_OF_INTERFACES = 1
MAX_NUM_OF_INTERFACES = 2
NUM_OF_ITERATIONS = 500

def main():
    bellman_ford_execution_time, dijkstra_execution_time = compare()

    print('bellman-ford', round(bellman_ford_execution_time*100, 4))
    print('dijkstra', round(dijkstra_execution_time*100, 4))

    print('dijkstra is faster', round(bellman_ford_execution_time/dijkstra_execution_time, 2), ' times')

def compare():
    bellman_ford_execution_time = 0
    dijkstra_execution_time = 0
    for i in range(NUM_OF_ITERATIONS):
        network_generator.main(NUM_OF_NETWORKS, NUM_OF_ROUTERS, MIN_NUM_OF_INTERFACES, MAX_NUM_OF_INTERFACES)
        bellman_ford_full_vertices = prepare_bellman_ford_data()
        dijkstra_full_vertices = prepare_dijkstra_data()

        bellman_ford_execution_time += measure_time_of_bellman_ford(bellman_ford_full_vertices)
        dijkstra_execution_time += measure_time_of_dijkstra(dijkstra_full_vertices)

    return bellman_ford_execution_time, dijkstra_execution_time

def measure_time_of_bellman_ford(full_vertices):
    start = time.time()
    bellman_ford.calculate_distances(full_vertices)
    end = time.time()

    execution_time = end - start

    return execution_time

def measure_time_of_dijkstra(full_vertices):
    start = time.time()
    dijkstra.calculate_distances(full_vertices)
    end = time.time()

    execution_time = end - start

    return execution_time

def prepare_bellman_ford_data():
    vertices, edges = graph_creator.main()
    source_vertex = vertices[0]
    vertices_with_distances = bellman_ford.set_initial_distances(source_vertex, vertices)
    vertices_with_predecessors = bellman_ford.determine_predecessors(vertices, edges)
    full_vertices = bellman_ford.merge_distances_and_predecessors(vertices_with_distances, vertices_with_predecessors)

    return full_vertices

def prepare_dijkstra_data():
    vertices, edges = graph_creator.main()
    source_vertex = vertices[0]
    vertices_with_distances = dijkstra.set_initial_distances(source_vertex, vertices)
    vertices_with_successors = dijkstra.determine_successors(vertices, edges)
    full_vertices = dijkstra.merge_distances_and_successors(vertices_with_distances, vertices_with_successors)

    return full_vertices

main()