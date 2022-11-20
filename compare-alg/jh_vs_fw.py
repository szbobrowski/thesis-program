import time
import network_generator
import graph_creator
import floyd_warshall
import johnson
import numpy
from scipy import stats


NUM_OF_NETWORKS = 120
NUM_OF_ROUTERS = 150
MIN_NUM_OF_INTERFACES = 4
MAX_NUM_OF_INTERFACES = 4
UNIT_SCALAR = 1000
NUM_OF_ITERATIONS = 5

def main():
    johnson_execution_time, johnson_precision, floyd_warshall_execution_time, floyd_warshall_precision = compare()

    print('--------------------\n')
    print('johnson [ms]', round(johnson_execution_time*UNIT_SCALAR / NUM_OF_ITERATIONS, 2), \
        '+/-', round(johnson_precision, 2))

    print('floyd-warshall [ms]', round(floyd_warshall_execution_time*UNIT_SCALAR / NUM_OF_ITERATIONS, 2), \
        '+/-', round(floyd_warshall_precision, 2))


def compare():
    johnson_execution_time = 0
    floyd_warshall_execution_time = 0

    johnson_times = []
    floyd_warshall_times = []
    for i in range(NUM_OF_ITERATIONS):
        network_generator.main(NUM_OF_NETWORKS, NUM_OF_ROUTERS, MIN_NUM_OF_INTERFACES, MAX_NUM_OF_INTERFACES)
        johnson_vertices, johnson_edges = prepare_johnson_data()
        floyd_warshall_initial_matrix, floyd_warshall_vertices  = prepare_floyd_warshall_data()

        johnson_iteration_time = measure_time_of_johnson(johnson_vertices, johnson_edges)
        floyd_warshall_iteration_time = measure_time_of_floyd_warshall(floyd_warshall_initial_matrix, floyd_warshall_vertices)

        johnson_execution_time += johnson_iteration_time
        floyd_warshall_execution_time += floyd_warshall_iteration_time

        johnson_times.append(johnson_iteration_time)
        floyd_warshall_times.append(floyd_warshall_iteration_time)

        print('itr', i)

    johnson_precision = calculate_precision(johnson_times)
    floyd_warshall_precision = calculate_precision(floyd_warshall_times)

    return johnson_execution_time, johnson_precision, floyd_warshall_execution_time, floyd_warshall_precision


def calculate_precision(data_array):
    data_array = [value * UNIT_SCALAR / NUM_OF_ITERATIONS for value in data_array]
    multiplier = stats.t.ppf(0.975, len(data_array))
    return numpy.std(data_array)*multiplier


def measure_time_of_johnson(vertices, edges):
    [matrix, execution_time]  = johnson.calculate_distances(vertices, edges)

    return execution_time


def measure_time_of_floyd_warshall(initial_matrix, vertices):
    start = time.time()
    floyd_warshall.calculate_distances(initial_matrix ,vertices)
    end = time.time()

    execution_time = end - start

    return execution_time


def prepare_johnson_data():
    vertices, edges = graph_creator.main()

    return vertices, edges


def prepare_floyd_warshall_data():
    vertices, edges = graph_creator.main()
    empty_matrix = floyd_warshall.create_empty_matrix(vertices)
    initial_matrix = floyd_warshall.create_initial_matrix(empty_matrix, edges, vertices)

    return initial_matrix, vertices

main()