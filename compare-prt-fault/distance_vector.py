from copy import deepcopy
import json
import random
from sys import getsizeof
import time
import bellman_ford

CONVERGENCE_ACHIEVED = False

def main():
    data = read_data_from_file()
    neighbors_list = create_neighbors(data)

    run_distance_vector(neighbors_list)


def run_distance_vector(neighbors_list):
    routing_tables = {}

    for router in neighbors_list:
        neighbors = extract_neighbors(neighbors_list[router])
        nodes = uniquify_list(create_initial_vertices_info(router, neighbors_list[router]))
        connections = (create_initial_connections_info(router, neighbors_list[router]))
        connections = calculate_best_connections(nodes, connections, router)
        next_hops = {}

        convergence = False
        routing_tables[router] = [neighbors, nodes, connections, next_hops, convergence]

    counter = 0
    while (not convergence_reached(routing_tables)):
        counter += 1
        for router in routing_tables:
            if ((len(routing_tables[router][0])) == 0):
                routing_tables[router][4] = True
                continue
            for neighbor in routing_tables[router][0]:
                info_before_update = deepcopy(routing_tables[neighbor[0]])

                update_connections(neighbor[0], neighbor[1], routing_tables[neighbor[0]][2], routing_tables[router][2], routing_tables[neighbor[0]][3])
                routing_tables[neighbor[0]][1] = update_nodes(routing_tables[neighbor[0]][1], routing_tables[router][1])
                routing_tables[neighbor[0]][2] = calculate_best_connections(routing_tables[neighbor[0]][1], routing_tables[neighbor[0]][2], neighbor[0])

                info_after_update = deepcopy(routing_tables[neighbor[0]])
                routing_tables[neighbor[0]][4] = (not (has_routing_table_changed(info_before_update, info_after_update)))

        if (counter >= 30):
            print('endless loop')
            break

    removed_node, neighbors_of_removed_node = remove_random_router(neighbors_list)
    del routing_tables[removed_node]

    for router in neighbors_list:
        routing_tables[router][4] = False
        neighbors = extract_neighbors(neighbors_list[router])
        routing_tables[router][0] = neighbors

    propagation_time = 180
    calculation_time = 0
    overall_time = 0
    overall_data_sent = 0
    mean_calculated_data = 0

    counter = 0
    updated_routers = neighbors_of_removed_node
    while (not convergence_reached(routing_tables)):
        propagation_time += random.randint(1, 5)
        counter += 1
        for router in routing_tables:
            if ((len(routing_tables[router][0])) == 0):
                routing_tables[router][4] = True
                continue
            for neighbor in routing_tables[router][0]:
                info_before_update = deepcopy(routing_tables[neighbor[0]])

                start = time.time()
                update_connections(neighbor[0], neighbor[1], routing_tables[neighbor[0]][2], routing_tables[router][2], routing_tables[neighbor[0]][3])
                routing_tables[neighbor[0]][1] = update_nodes(routing_tables[neighbor[0]][1], routing_tables[router][1])
                routing_tables[neighbor[0]][2] = calculate_best_connections(routing_tables[neighbor[0]][1], routing_tables[neighbor[0]][2], neighbor[0])
                end = time.time()
                calculation_time += (end - start)*30

                if (router in updated_routers):
                    share_fault_info(routing_tables[neighbor[0]],  removed_node)
                    updated_routers.append(neighbor[0])

                info_after_update = deepcopy(routing_tables[neighbor[0]])
                routing_tables[neighbor[0]][4] = (not (has_routing_table_changed(info_before_update, info_after_update)))
                mean_calculated_data += getsizeof(str(routing_tables[neighbor[0]][1])) + getsizeof(str(routing_tables[neighbor[0]][2])) + getsizeof(str(neighbor[0])) 

            overall_data_sent += (getsizeof(str(routing_tables[router][2])) * len(routing_tables[router][0]))

        if (counter >= 30):
            print('endless loop')
            break

    calculation_time = (calculation_time / len(routing_tables))
    overall_time = propagation_time + calculation_time
    mean_calculated_data = mean_calculated_data /  len(routing_tables)

    distance_vector_statistics = [overall_time, overall_data_sent, calculation_time, mean_calculated_data] 
    return distance_vector_statistics


def share_fault_info(routing_table, removed_node):
    nodes = routing_table[1]
    connections = routing_table[2]
    next_hops = routing_table[3]
    if removed_node in nodes:
        nodes.remove(removed_node)

    for i in range(3):
        for connection in connections:
            if removed_node in connection:
                connections.pop(connections.index(connection))

    for hop in list(next_hops):
        if hop == removed_node or next_hops[hop] == removed_node:
            for connection in connections:
                if connection[1] == hop:
                    connections.pop(connections.index(connection))
            del next_hops[hop]


def remove_random_router(neighbors_list):
    routers = []
    for router in neighbors_list:
        routers.append(router)

    router_to_remove = random.choice(routers)
    neighbors = extract_neighbors_names(neighbors_list[router_to_remove])

    del neighbors_list[router_to_remove]

    for i in range(3):
        for router in neighbors:
            for entry in neighbors_list[router]:
                if router_to_remove in entry:
                    neighbors_list[router].pop(neighbors_list[router].index(entry))

    return router_to_remove, neighbors


def extract_neighbors_names(router_neighbors):
    neighbors = []
    for router in router_neighbors:
        neighbors.append(router[0])

    return neighbors


def convergence_reached(routing_tables):
    for router in routing_tables:
        if (not routing_tables[router][4]):
            return False
            
    return True


def has_routing_table_changed(info_before_update, info_after_update):
    info_before_update[2].sort()
    info_after_update[2].sort()

    if len(info_before_update[2]) != len(info_after_update[2]):
        return True

    for i in range(len(info_before_update[2])):
        if (info_before_update[2][i] != info_after_update[2][i]):
            return True

    return False
            

def update_connections(node, cost, existing_connections, offered_connections, next_hops):
    destinations = extract_destinations(existing_connections)
    for offered_connection in offered_connections:
        if offered_connection[1] in destinations:
            for existing_connection in existing_connections:
                if existing_connection[1] == offered_connection[1]:
                    if existing_connection[2] > (offered_connection[2] + cost):
                        existing_connections.append([node, offered_connection[1], (offered_connection[2] + cost)])
                        next_hops[offered_connection[1]] = offered_connection[0]
                    elif (not (existing_connection[1] in next_hops)):
                        next_hops[existing_connection[1]] = existing_connection[0]
        else:
            existing_connections.append([node, offered_connection[1], (offered_connection[2] + cost)])
            next_hops[offered_connection[1]] = offered_connection[0]

def update_nodes(known_nodes, new_nodes):
    return uniquify_list(known_nodes + new_nodes)

def extract_destinations(connections):
    destinations = []
    for connection in connections:
        destinations.append(connection[1])

    return destinations


def calculate_best_connections(vertices, edges, source_vertex):
    connections = []
    data = bellman_ford.main(vertices, edges, source_vertex)
    for router in data:
        connection = [source_vertex, router, data[router]['distance']]
        connections.append(connection)

    return connections


def extract_neighbors(router_initial_info):
    neighbors = []
    for neighbor in router_initial_info:
        neighbors.append([neighbor[0], neighbor[1]])

    return neighbors


def create_initial_connections_info(node, router_initial_info):
    connections = []
    for entry in router_initial_info:
        connections.append([node, entry[0], entry[1]])

    return connections


def create_initial_vertices_info(node, router_initial_info):
    nodes = []
    for entry in router_initial_info:
        nodes += [node, entry[0]]

    return nodes


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


def read_data_from_file():
    with open('../data/sample2.json') as file:
        data = json.load(file)

    return data


def uniquify_list(the_list):
    a_set = set(the_list)
    uniquified_list = list(a_set)

    return uniquified_list