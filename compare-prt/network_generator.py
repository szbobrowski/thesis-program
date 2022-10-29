import sys
import random
import json

def main(num_of_networks=1, num_of_routers=1, min_num_of_interfaces=1, max_num_of_interfaces=1):
    network_addresses = select_network_addresses(num_of_networks)
    routers = create_routers(num_of_routers, min_num_of_interfaces, max_num_of_interfaces, network_addresses)
    save_results_to_file(routers)

def select_network_addresses(num_of_networks):
    network_addresses = []
    for i in range(num_of_networks):
        network_addresses.append(create_single_network())

    return network_addresses

def create_single_network():
    octet1 = random.randint(1, 255)
    octet2 = random.randint(0, 255)
    octet3 = random.randint(0, 255)

    network = str(octet1) + '.' + str(octet2) + '.' + str(octet3) + '.0'
    return network

def create_routers(num_of_routers, min_num_of_interfaces, max_num_of_interfaces, network_addresses):
    routers = []
    for i in range(num_of_routers):
        routers.append(create_single_router(min_num_of_interfaces, max_num_of_interfaces, network_addresses))

    return routers

def create_single_router(min_num_of_interfaces, max_num_of_interfaces, network_addresses):
    id = random.randint(1, 100000000)
    name = 'router' + str(id)
    number_of_interfaces = random.randint(min_num_of_interfaces, max_num_of_interfaces)
    broadcasted_networks_addresses = random.sample(network_addresses, number_of_interfaces)

    broadcasted_networks = create_broadcasted_networks(broadcasted_networks_addresses)
    
    router = {
        'id': id,
        'name': name,
        'broadcastedNetworks': broadcasted_networks
    }

    return router

def create_broadcasted_networks(broadcasted_networks_addresses):
    broadcasted_networks = []
    bandwidth = random.randint(1, 10)
    for address in broadcasted_networks_addresses:
        broadcasted_networks.append({
            'address': address,
            'bandwidth': bandwidth
        })

    return broadcasted_networks

def save_results_to_file(routers):
    with open('../data/routers.json', 'w') as fout:
        json.dump(routers , fout)