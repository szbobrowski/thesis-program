import time
import network_generator
import graph_creator
import floyd_warshall
import johnson

NUM_OF_NETWORKS = 12
NUM_OF_ROUTERS = 50
MIN_NUM_OF_INTERFACES = 2
MAX_NUM_OF_INTERFACES = 3
NUM_OF_ITERATIONS = 200

def main():
    floyd_warshall_execution_time, johnson_execution_time = compare()

    print('floyd-warshall', round(floyd_warshall_execution_time*100, 4))
    print('johnson', round(johnson_execution_time*100, 4))

    print('floyd-warshall is faster', round(johnson_execution_time/floyd_warshall_execution_time, 2), ' times')


def compare():
    floyd_warshall_execution_time = 0
    johnson_execution_time = 0
    for i in range(NUM_OF_ITERATIONS):
        network_generator.main(NUM_OF_NETWORKS, NUM_OF_ROUTERS, MIN_NUM_OF_INTERFACES, MAX_NUM_OF_INTERFACES)
        floyd_warshall_initial_matrix, floyd_warshall_vertices  = prepare_floyd_warshall_data()
        johnson_vertices, johnson_edges = prepare_johnson_data()

        floyd_warshall_execution_time += measure_time_of_floyd_warshall(floyd_warshall_initial_matrix, floyd_warshall_vertices)
        johnson_execution_time += measure_time_of_johnson(johnson_vertices, johnson_edges) 

    return floyd_warshall_execution_time, johnson_execution_time

def measure_time_of_floyd_warshall(initial_matrix, vertices):
    start = time.time()
    floyd_warshall.calculate_distances(initial_matrix ,vertices)
    end = time.time()

    execution_time = end - start

    return execution_time

def measure_time_of_johnson(vertices, edges):
    [matrix, execution_time]  = johnson.calculate_distances(vertices, edges)

    return execution_time

def prepare_floyd_warshall_data():
    vertices, edges = graph_creator.main()
    empty_matrix = floyd_warshall.create_empty_matrix(vertices)
    initial_matrix = floyd_warshall.create_initial_matrix(empty_matrix, edges, vertices)

    return initial_matrix, vertices

def prepare_johnson_data():
    vertices, edges = graph_creator.main()

    return vertices, edges

main()