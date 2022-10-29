import link_state
import distance_vector
import network_generator

NUM_OF_NETWORKS = 20
NUM_OF_ROUTERS = 45
MIN_NUM_OF_INTERFACES = 1
MAX_NUM_OF_INTERFACES = 3
NUM_OF_ITERATIONS = 30

def main():
    link_state_statistics, distance_vector_statistics = compare()
    print('link-state convergence time', round(link_state_statistics[0], 2))
    print('link-state overall data sent in megabytes', round(link_state_statistics[1]/1000000, 2))

    print('distance-vector convergence time', round(distance_vector_statistics[0], 2))
    print('distance-vector overall data sent in megabytes', round(distance_vector_statistics[1]/1000000, 2))

def compare():
    link_state_convergence_time = 0
    link_state_sent_data = 0
    distance_vector_convergence_time = 0
    distance_vector_sent_data = 0
    for i in range(NUM_OF_ITERATIONS):
        network_generator.main(NUM_OF_NETWORKS, NUM_OF_ROUTERS, MIN_NUM_OF_INTERFACES, MAX_NUM_OF_INTERFACES)
        data = link_state.read_data_from_file()
        
        link_state_neighbors_list = link_state.create_neighbors(data)
        link_state_statistics = link_state.run_link_state(link_state_neighbors_list)
        link_state_convergence_time += link_state_statistics[0]
        link_state_sent_data += link_state_statistics[1]

        distance_vector_neighbors_list = distance_vector.create_neighbors(data)
        distance_vector_statistics = distance_vector.run_distance_vector(distance_vector_neighbors_list)
        distance_vector_convergence_time += distance_vector_statistics[0]
        distance_vector_sent_data += distance_vector_statistics[1]

    link_state_statistics = [link_state_convergence_time, link_state_sent_data]
    distance_vector_statistics = [distance_vector_convergence_time, distance_vector_sent_data]

    return link_state_statistics, distance_vector_statistics

main()