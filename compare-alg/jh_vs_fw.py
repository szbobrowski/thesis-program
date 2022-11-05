import time
import network_generator
import graph_creator
import floyd_warshall
import johnson

NUM_OF_NETWORKS = 55
NUM_OF_ROUTERS = 120
MIN_NUM_OF_INTERFACES = 3
MAX_NUM_OF_INTERFACES = 6
NUM_OF_ITERATIONS = 10

def main():
    johnson_execution_time, floyd_warshall_execution_time = compare()

    print('--------------------\n')
    print('johnson', round(johnson_execution_time*100, 2))
    print('floyd-warshall', round(floyd_warshall_execution_time*100, 2))

    print('floyd-warshall is faster', round(johnson_execution_time/floyd_warshall_execution_time, 2), ' times')


def compare():
    johnson_execution_time = 0
    floyd_warshall_execution_time = 0
    for i in range(NUM_OF_ITERATIONS):
        network_generator.main(NUM_OF_NETWORKS, NUM_OF_ROUTERS, MIN_NUM_OF_INTERFACES, MAX_NUM_OF_INTERFACES)
        johnson_vertices, johnson_edges = prepare_johnson_data()
        floyd_warshall_initial_matrix, floyd_warshall_vertices  = prepare_floyd_warshall_data()

        johnson_execution_time += measure_time_of_johnson(johnson_vertices, johnson_edges)
        floyd_warshall_execution_time += measure_time_of_floyd_warshall(floyd_warshall_initial_matrix, floyd_warshall_vertices) 

        print('inter', i)

    return johnson_execution_time, floyd_warshall_execution_time


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