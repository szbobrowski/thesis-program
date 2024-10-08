import json
from sys import getsizeof
import dijkstra
import time
import random

def main():
    data = read_data_from_file()
    neighbors_list = create_neighbors(data)

    run_link_state(neighbors_list)


def run_link_state(neighbors_list, num_of_networks):
    databases = {}

    for router in neighbors_list:
        nodes = add_vertices_info_to_database(router, neighbors_list[router])
        database_info = add_edges_info_to_database(router, neighbors_list[router])
        routing_table = dijkstra.main(nodes, database_info, router)

        databases[router] = [nodes, database_info, routing_table]
        databases[router][0] = uniquify_list(databases[router][0])
        databases[router][1] = [list(x) for x in set(tuple(x) for x in databases[router][1])]

    for first_router in neighbors_list:
        nodes = []
        database_info = []
        if (len(neighbors_list[first_router]) == 0):
            continue
        for second_router in neighbors_list:
            if first_router == second_router:
                continue

            nodes = add_vertices_info_to_database(first_router, neighbors_list[first_router])
            database_info = add_edges_info_to_database(first_router, neighbors_list[first_router])

            databases[second_router][0] += nodes
            databases[second_router][1] += database_info
            databases[second_router][0] = uniquify_list(databases[second_router][0])
            databases[second_router][1] = [list(x) for x in set(tuple(x) for x in databases[second_router][1])]
            databases[second_router][2] = dijkstra.main(databases[second_router][0], databases[second_router][1], second_router)

    removed_node, neighbors_of_removed_node = remove_random_router(neighbors_list)
    del neighbors_list[removed_node]

    propagation_time = 40
    calculation_time = 0
    overall_time = 0
    overall_data_sent = 0
    num_of_edges_the_lsa_travels = calculate_number_of_edges_the_lsa_travels(neighbors_list, num_of_networks)
    mean_calculated_data = 0

    for first_router in neighbors_of_removed_node:
        nodes = []
        database_info = []
        if (len(neighbors_list[first_router]) == 0):
            continue
        for second_router in neighbors_list:
            if first_router == second_router:
                continue
            propagation_time += ((find_highest_cost_to_neighbor(neighbors_list[second_router]) / 1000) / len(neighbors_of_removed_node))

            start = time.time()

            nodes = add_vertices_info_to_database(first_router, neighbors_list[first_router])
            database_info = add_edges_info_to_database(first_router, neighbors_list[first_router])

            databases[second_router][0] += nodes
            databases[second_router][1] += database_info
            databases[second_router][0] = uniquify_list(databases[second_router][0])
            databases[second_router][1] = [list(x) for x in set(tuple(x) for x in databases[second_router][1])]
            end = time.time()
            calculation_time += (end - start)*30
            share_fault_info(databases[second_router][0], databases[second_router][1], removed_node)

            start = time.time()
            databases[second_router][2] = dijkstra.main(databases[second_router][0], databases[second_router][1], second_router)
            end = time.time()
            calculation_time += (end - start)*30

            mean_calculated_data += getsizeof(str(databases[second_router][0])) + getsizeof(str(databases[second_router][1])) + getsizeof(str(second_router)) 
        
        overall_data_sent += (getsizeof(str(neighbors_list[first_router])) * num_of_edges_the_lsa_travels)

    calculation_time = (calculation_time / len(databases))
    overall_time = propagation_time + calculation_time
    mean_calculated_data = mean_calculated_data / len(databases)

    link_state_statistics = [overall_time, overall_data_sent, calculation_time, mean_calculated_data]
    return link_state_statistics


def share_fault_info(nodes, database_info, removed_node):
    if removed_node in nodes:
        nodes.remove(removed_node)

    for i in range(3):
        for entry in database_info:
            if removed_node in entry:
                database_info.pop(database_info.index(entry))


def remove_random_router(neighbors_list):
    routers = []
    for router in neighbors_list:
        routers.append(router)

    router_to_remove = random.choice(routers)
    neighbors = extract_neighbors_names(neighbors_list[router_to_remove])

    return router_to_remove, neighbors


def extract_neighbors_names(router_neighbors):
    neighbors = []
    for router in router_neighbors:
        neighbors.append(router[0])

    return neighbors


def calculate_number_of_edges_the_lsa_travels(neighbors_list, num_of_networks=1):
    num_of_edges = 0
    mean_num_of_interfaces = calculate_mean_num_of_interfaces(neighbors_list)
    divider = mean_num_of_interfaces / num_of_networks
    for router in neighbors_list:
        num_of_edges += len(neighbors_list[router])

    num_of_edges = int(num_of_edges / divider)
    num_of_edges /= 2

    return num_of_edges


def calculate_mean_num_of_interfaces(neighbors_list):
    num_of_all_interfaces = 0
    for neighbor in neighbors_list:
        num_of_all_interfaces += len(neighbors_list[neighbor])

    mean_num_of_interfaces = num_of_all_interfaces / len(neighbors_list)

    return mean_num_of_interfaces


def find_highest_cost_to_neighbor(neighbors):
    highest_cost = 0
    for neighbor in neighbors:
        if neighbor[1] > highest_cost:
            highest_cost = neighbor[1]

    return highest_cost


def add_edges_info_to_database(node, router_propagation_info):
    database_info = []
    for entry in router_propagation_info:
        database_info.append([node, entry[0], entry[1]])
        database_info.append([entry[0], node, entry[1]])

    return database_info

def add_vertices_info_to_database(node, router_propagation_info):
    nodes = []
    for entry in router_propagation_info:
        nodes += [node, entry[0]]

    return nodes


def read_data_from_file():
    with open('../data/sample2.json') as file:
        data = json.load(file)

    return data


def create_neighbors(network_data):
    neighbors_list = {}
    for first_router in network_data:
        first_router_neighbors = []
        first_router_networks = first_router['broadcastedNetworks']
        for second_router in network_data:
            if first_router['name'] == second_router['name']:
                continue

            second_router_networks = second_router['broadcastedNetworks']
            
            is_pair, cost = pair_networks(first_router_networks, second_router_networks)
            if is_pair:
                first_router_neighbors.append([second_router['name'], cost])

        neighbors_list[first_router['name']] = first_router_neighbors

    return neighbors_list
            

def pair_networks(first_router_networks, second_router_networks):
    is_pair = False
    cost = 1000
    for first_router_network in first_router_networks:
        for second_router_network in second_router_networks:
            if first_router_network['address'] == second_router_network['address']:
                is_pair = True
                if max(int(first_router_network['bandwidth']), int(second_router_network['bandwidth'])) < cost:
                    cost = max(int(first_router_network['bandwidth']), int(second_router_network['bandwidth']))

    return is_pair, cost


def uniquify_list(the_list):
    a_set = set(the_list)
    uniquified_list = list(a_set)

    return uniquified_list