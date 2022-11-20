import json
import numpy
import distance_vector
import link_state
import network_generator
from scipy import stats

NUM_OF_NETWORKS = 80
NUM_OF_ROUTERS = 80
MIN_NUM_OF_INTERFACES = 2
MAX_NUM_OF_INTERFACES = 2
NUM_OF_ITERATIONS = 5

def main():
    link_state_statistics, distance_vector_statistics = compare()

    print('--------------------\n')
    print('link-state convergence time [s]', round(link_state_statistics[0] / NUM_OF_ITERATIONS, 2), \
        '+/-', round(link_state_statistics[6][0], 4))
    print('link-state bandwidth usage [kB]', round(link_state_statistics[1] / 1000 / NUM_OF_ITERATIONS, 2), \
        '+/-', round(link_state_statistics[6][1], 3))
    print('link-state space usage per router [kB]', round(link_state_statistics[2] / 1000 / NUM_OF_ITERATIONS, 2), \
        '+/-', round(link_state_statistics[6][2], 3))
    print('link-state mean packet size [bytes]', round(link_state_statistics[3] / NUM_OF_ITERATIONS, 2), \
        '+/-', round(link_state_statistics[6][3], 3))
    print('link-state calculation time per router [ms]', round(link_state_statistics[4] * 1000 / 20 / NUM_OF_ITERATIONS, 2), \
        '+/-', round(link_state_statistics[6][4], 4))
    print('link-state data calculated per router [kB]', round(link_state_statistics[5] / 1000 / NUM_OF_ITERATIONS, 2), \
        '+/-', round(link_state_statistics[6][5], 3))

    print('--------------------\n')
    print('distance vector convergence time [s]', round(distance_vector_statistics[0] / NUM_OF_ITERATIONS, 2), \
        '+/-', round(distance_vector_statistics[6][0], 4))
    print('distance vector bandwidth usage [kB]', round(distance_vector_statistics[1] / 1000 / NUM_OF_ITERATIONS, 2), \
        '+/-', round(distance_vector_statistics[6][1], 3))
    print('distance vector space usage per router [kB]', round(distance_vector_statistics[2] / 1000 / NUM_OF_ITERATIONS, 2), \
        '+/-', round(distance_vector_statistics[6][2], 3))
    print('distance vector mean packet size [bytes]', round(distance_vector_statistics[3] / NUM_OF_ITERATIONS, 2), \
        '+/-', round(distance_vector_statistics[6][3], 3))
    print('distance vector calculation time per router [ms]', round(distance_vector_statistics[4] * 1000 / 20 / NUM_OF_ITERATIONS, 2), \
        '+/-', round(distance_vector_statistics[6][4], 4))
    print('distance vector data calculated per router [kB]', round(distance_vector_statistics[5] / 1000 / NUM_OF_ITERATIONS, 2), \
        '+/-', round(distance_vector_statistics[6][5], 3))


def compare():
    link_state_convergence_time = 0
    link_state_sent_data = 0
    link_state_mean_memory_usage = 0
    link_state_mean_packet_size = 0
    link_state_mean_calculation_time = 0
    link_state_mean_calculated_data = 0

    distance_vector_convergence_time = 0
    distance_vector_sent_data = 0
    distance_vector_mean_memory_usage = 0
    distance_vector_mean_packet_size = 0
    distance_vector_mean_calculation_time = 0
    distance_vector_mean_calculated_data = 0

    link_state_all_statistics = []
    distance_vector_all_statistics = []

    for i in range(NUM_OF_ITERATIONS):
        print('iter', i)
        network_generator.main(NUM_OF_NETWORKS, NUM_OF_ROUTERS, MIN_NUM_OF_INTERFACES, MAX_NUM_OF_INTERFACES)
        data = read_data_from_file()
        
        link_state_neighbors_list = link_state.create_neighbors(data)
        link_state_statistics = link_state.run_link_state(link_state_neighbors_list, NUM_OF_NETWORKS)
        link_state_all_statistics.append(link_state_statistics)

        link_state_convergence_time += link_state_statistics[0]
        link_state_sent_data += link_state_statistics[1]
        link_state_mean_memory_usage += link_state_statistics[2]
        link_state_mean_packet_size += link_state_statistics[3]
        link_state_mean_calculation_time += link_state_statistics[4]
        link_state_mean_calculated_data += link_state_statistics[5]

        distance_vector_neighbors_list = distance_vector.create_neighbors(data)
        distance_vector_statistics = distance_vector.run_distance_vector(distance_vector_neighbors_list)
        distance_vector_all_statistics.append(distance_vector_statistics)

        distance_vector_convergence_time += distance_vector_statistics[0]
        distance_vector_sent_data += distance_vector_statistics[1]
        distance_vector_mean_memory_usage += distance_vector_statistics[2]
        distance_vector_mean_packet_size += distance_vector_statistics[3]
        distance_vector_mean_calculation_time += distance_vector_statistics[4]
        distance_vector_mean_calculated_data += distance_vector_statistics[5]

    link_state_precision, distance_vector_precision = calculate_precision(link_state_all_statistics, distance_vector_all_statistics)

    link_state_statistics = [
        link_state_convergence_time, 
        link_state_sent_data, 
        link_state_mean_memory_usage, 
        link_state_mean_packet_size,
        link_state_mean_calculation_time,
        link_state_mean_calculated_data,
        link_state_precision
    ]

    distance_vector_statistics = [
        distance_vector_convergence_time, 
        distance_vector_sent_data, 
        distance_vector_mean_memory_usage, 
        distance_vector_mean_packet_size,
        distance_vector_mean_calculation_time,
        distance_vector_mean_calculated_data,
        distance_vector_precision
    ]

    return link_state_statistics, distance_vector_statistics


def calculate_precision(link_state_statistics, distance_vector_statistics):
    link_state_convergence_time = []
    link_state_sent_data = []
    link_state_mean_memory_usage = []
    link_state_mean_packet_size = []
    link_state_mean_calculation_time = []
    link_state_mean_calculated_data = []

    distance_vector_convergence_time = []
    distance_vector_sent_data = []
    distance_vector_mean_memory_usage = []
    distance_vector_mean_packet_size = []
    distance_vector_mean_calculation_time = []
    distance_vector_mean_calculated_data = []
    
    for i in range(len(link_state_statistics)):
        link_state_convergence_time.append(link_state_statistics[i][0])
        link_state_sent_data.append(link_state_statistics[i][1])
        link_state_mean_memory_usage.append(link_state_statistics[i][2])
        link_state_mean_packet_size.append(link_state_statistics[i][3])
        link_state_mean_calculation_time.append(link_state_statistics[i][4])
        link_state_mean_calculated_data.append(link_state_statistics[i][5])

        distance_vector_convergence_time.append(distance_vector_statistics[i][0])
        distance_vector_sent_data.append(distance_vector_statistics[i][1])
        distance_vector_mean_memory_usage.append(distance_vector_statistics[i][2])
        distance_vector_mean_packet_size.append(distance_vector_statistics[i][3])
        distance_vector_mean_calculation_time.append(distance_vector_statistics[i][4])
        distance_vector_mean_calculated_data.append(distance_vector_statistics[i][5])

    link_state_precision = [
        calculate_precision_of_single_array(link_state_convergence_time), \
        calculate_precision_of_single_array(link_state_sent_data, 1/1000), \
        calculate_precision_of_single_array(link_state_mean_memory_usage, 1/1000), \
        calculate_precision_of_single_array(link_state_mean_packet_size), \
        calculate_precision_of_single_array(link_state_mean_calculation_time, 1000/20), \
        calculate_precision_of_single_array(link_state_mean_calculated_data, 1/1000) \
    ]

    distance_vector_precision = [
        calculate_precision_of_single_array(distance_vector_convergence_time), \
        calculate_precision_of_single_array(distance_vector_sent_data, 1/1000), \
        calculate_precision_of_single_array(distance_vector_mean_memory_usage, 1/1000), \
        calculate_precision_of_single_array(distance_vector_mean_packet_size), \
        calculate_precision_of_single_array(distance_vector_mean_calculation_time, 1000/20), \
        calculate_precision_of_single_array(distance_vector_mean_calculated_data, 1/1000) \
    ]

    return link_state_precision, distance_vector_precision


def calculate_precision_of_single_array(data_array, scalar=1):
    data_array = [value * scalar / NUM_OF_ITERATIONS for value in data_array]
    multiplier = stats.t.ppf(0.975, len(data_array))
    return numpy.std(data_array)*multiplier


def read_data_from_file():
    with open('../data/routers.json') as file:
        data = json.load(file)

    return data

main()