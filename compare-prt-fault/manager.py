import json
import link_state
import distance_vector
import network_generator

NUM_OF_NETWORKS = 45
NUM_OF_ROUTERS = 70
MIN_NUM_OF_INTERFACES = 2
MAX_NUM_OF_INTERFACES = 3
NUM_OF_ITERATIONS = 1

def main():
    link_state_statistics, distance_vector_statistics = compare()

    print('--------------------\n')
    print('link-state convergence time', round(link_state_statistics[0] / NUM_OF_ITERATIONS, 2))
    print('link-state bandwidth usage in kilobytes', round((link_state_statistics[1] / NUM_OF_ITERATIONS) / 1000, 2))
    print('link-state calculation time per router', round((link_state_statistics[2]*100 / NUM_OF_ITERATIONS), 2))
    print('link-state data calculated per router in kilobytes', round((link_state_statistics[3] / NUM_OF_ITERATIONS) / 1000, 2))
    print('--------------------\n')
    print('distance-vector convergence time', round(distance_vector_statistics[0] / NUM_OF_ITERATIONS, 2))
    print('distance-vector bandwidth usage in kilobytes', round((distance_vector_statistics[1] / NUM_OF_ITERATIONS) / 1000, 2))
    print('distance-vector calculation time per router', round((distance_vector_statistics[2]*100 / NUM_OF_ITERATIONS), 2))
    print('distance-vector data calculated per router in kilobytes', round((distance_vector_statistics[3] / NUM_OF_ITERATIONS) / 1000, 2))

def compare():
    link_state_convergence_time = 0
    link_state_sent_data = 0
    link_state_mean_calculation_time = 0
    link_state_mean_calculated_data = 0

    distance_vector_convergence_time = 0
    distance_vector_sent_data = 0
    distance_vector_mean_calculation_time = 0
    distance_vector_mean_calculated_data = 0 

    for i in range(NUM_OF_ITERATIONS):
        print('iteration', i)
        network_generator.main(NUM_OF_NETWORKS, NUM_OF_ROUTERS, MIN_NUM_OF_INTERFACES, MAX_NUM_OF_INTERFACES)
        data = read_data_from_file()
        
        print('link-state')
        link_state_neighbors_list = link_state.create_neighbors(data)
        link_state_statistics = link_state.run_link_state(link_state_neighbors_list, NUM_OF_NETWORKS)
        link_state_convergence_time += link_state_statistics[0]
        link_state_sent_data += link_state_statistics[1]
        link_state_mean_calculation_time += link_state_statistics[2]
        link_state_mean_calculated_data += link_state_statistics[3]

        print('distance-vector')
        distance_vector_neighbors_list = distance_vector.create_neighbors(data)
        distance_vector_statistics = distance_vector.run_distance_vector(distance_vector_neighbors_list)
        distance_vector_convergence_time += distance_vector_statistics[0]
        distance_vector_sent_data += distance_vector_statistics[1]
        distance_vector_mean_calculation_time += distance_vector_statistics[2]
        distance_vector_mean_calculated_data += distance_vector_statistics[3]

    link_state_statistics = [
        link_state_convergence_time, 
        link_state_sent_data,
        link_state_mean_calculation_time,
        link_state_mean_calculated_data
    ]

    distance_vector_statistics = [
        distance_vector_convergence_time, 
        distance_vector_sent_data,
        distance_vector_mean_calculation_time,
        distance_vector_mean_calculated_data
    ]

    return link_state_statistics, distance_vector_statistics
        

def read_data_from_file():
    with open('../data/routers.json') as file:
        data = json.load(file)

    return data

main()