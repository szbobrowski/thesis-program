from cProfile import run
import json
from operator import ne
from platform import node

def main():
    data = read_data_from_file()
    neighbors_list = create_neighbors(data)

    run_link_state(neighbors_list)


def run_link_state(neighbors_list):
    databases = {}
    for first_router in neighbors_list:
        database_info = []
        for second_router in neighbors_list:
            database_info += add_info_to_database(second_router, neighbors_list[second_router])

        database_info = [list(x) for x in set(tuple(x) for x in database_info)]
        databases[first_router] = database_info

    for router in databases:
        print(router, databases[router])


def add_info_to_database(node, router_propagation_info):
    database_info = []
    for entry in router_propagation_info:
        database_info.append([node, entry[0], entry[1]])
        database_info.append([entry[0], node, entry[1]])

    return database_info


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

main()