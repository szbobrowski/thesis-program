import sys
import random
import json

def main():
    num_of_networks, num_of_routers, min_num_of_interfaces, max_num_of_interfaces = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
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

    interfaces = create_interfaces(broadcasted_networks_addresses)
    broadcasted_networks = create_broadcasted_networks(broadcasted_networks_addresses)
    
    router = {
        'id': id,
        'name': name,
        'interfaces': interfaces,
        'broadcastedNetworks': broadcasted_networks
    }

    return router

def create_interfaces(broadcasted_networks_addresses):
    interfaces = []
    for address in broadcasted_networks_addresses:
        last_octet = random.randint(1, 255)
        interface_address = address[:len(address) - 1] + str(last_octet)

        interface = {
            'address': interface_address,
            'mask': 24
        }

        interfaces.append(interface)

    return interfaces

def create_broadcasted_networks(broadcasted_networks_addresses):
    broadcasted_networks = []
    for address in broadcasted_networks_addresses:
        broadcasted_networks.append({
            'address': address,
            'mask': 24
        })

    return broadcasted_networks

def save_results_to_file(routers):
    with open('../data/routers.json', 'w') as fout:
        json.dump(routers , fout)

main()