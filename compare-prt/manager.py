import link_state
import distance_vector
import network_generator

NUM_OF_NETWORKS = 8
NUM_OF_ROUTERS = 20
MIN_NUM_OF_INTERFACES = 1
MAX_NUM_OF_INTERFACES = 5
NUM_OF_ITERATIONS = 50

def main():
    link_state_statistics = compare()
    print('link-state convergence time', round(link_state_statistics[0]/1000, 4))
    print('link-state overall data sent in megabytes', round(link_state_statistics[1]/1000000))

def compare():
    link_state_execution_time = 0
    link_state_sent_data = 0
    for i in range(NUM_OF_ITERATIONS):
        network_generator.main(NUM_OF_NETWORKS, NUM_OF_ROUTERS, MIN_NUM_OF_INTERFACES, MAX_NUM_OF_INTERFACES)
        data = link_state.read_data_from_file()
        neighbors_list = link_state.create_neighbors(data)
        link_state_statistics = link_state.run_link_state(neighbors_list)
        link_state_execution_time += link_state_statistics[0]
        link_state_sent_data += link_state_statistics[1]

    return link_state_execution_time, link_state_sent_data

main()