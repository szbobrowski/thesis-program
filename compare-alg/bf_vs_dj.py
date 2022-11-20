import time
import network_generator
import graph_creator
import bellman_ford
import dijkstra
import numpy
from scipy import stats

NUM_OF_NETWORKS = 100
NUM_OF_ROUTERS = 120
MIN_NUM_OF_INTERFACES = 4
MAX_NUM_OF_INTERFACES = 4
UNIT_SCALAR = 1000000
NUM_OF_ITERATIONS = 5

def main():
    bellman_ford_execution_time, bellman_ford_precision, dijkstra_execution_time, dijkstra_precision = compare()

    print('--------------------\n')
    print('bellman-ford [us]', round(bellman_ford_execution_time*UNIT_SCALAR / NUM_OF_ITERATIONS, 2), \
        '+/-', round(bellman_ford_precision, 2))

    print('dijkstra [us]', round(dijkstra_execution_time*UNIT_SCALAR / NUM_OF_ITERATIONS, 2), \
        '+/-', round(dijkstra_precision, 2))
        

def compare():
    bellman_ford_execution_time = 0
    dijkstra_execution_time = 0

    bellman_ford_times = []
    dijkstra_times = []
    for i in range(NUM_OF_ITERATIONS):
        network_generator.main(NUM_OF_NETWORKS, NUM_OF_ROUTERS, MIN_NUM_OF_INTERFACES, MAX_NUM_OF_INTERFACES)
        bellman_ford_full_vertices = prepare_bellman_ford_data()
        dijkstra_full_vertices = prepare_dijkstra_data()

        bellman_ford_iteration_time = measure_time_of_bellman_ford(bellman_ford_full_vertices)
        dijkstra_iteration_time = measure_time_of_dijkstra(dijkstra_full_vertices)

        bellman_ford_execution_time += bellman_ford_iteration_time
        dijkstra_execution_time += dijkstra_iteration_time

        bellman_ford_times.append(bellman_ford_iteration_time)
        dijkstra_times.append(dijkstra_iteration_time)

    bellman_ford_precision = calculate_precision(bellman_ford_times)
    dijkstra_precision = calculate_precision(dijkstra_times)

    return bellman_ford_execution_time, bellman_ford_precision, dijkstra_execution_time, dijkstra_precision


def calculate_precision(data_array):
    data_array = [value * UNIT_SCALAR / NUM_OF_ITERATIONS for value in data_array]
    multiplier = stats.t.ppf(0.975, len(data_array))
    return numpy.std(data_array)*multiplier


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