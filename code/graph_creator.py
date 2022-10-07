import json
import itertools

def main():
    routers = read_data_from_file()
    network_addresses = extract_network_addresses(routers)
    subnetwork_collections, routers_sets = create_subnetwork_collections(routers, network_addresses)
    directed_edges = define_graph_edges(routers_sets)
    vertices = extract_vertices(routers)
    weighted_edges = add_weights(directed_edges)

    return vertices, weighted_edges

def read_data_from_file():
    with open('../data/routers.json') as file:
        data = json.load(file)

    return data

def extract_vertices(routers):
    vertices = []
    for router in routers:
        vertices.append(router['name'])

    return vertices

def extract_network_addresses(routers):
    addresses = []
    for router in routers:
        broadcastedNetworks = router['broadcastedNetworks']
        for network in broadcastedNetworks:
            addresses.append(network['address'])

    addresses = list(dict.fromkeys(addresses))
    return addresses

def create_subnetwork_collections(routers, network_addresses):
    subnetwork_collections = []
    routers_sets = []
    for network_address in network_addresses:
        routers_set = []
        for router in routers:
            broadcasted_addresses = []
            for network in router['broadcastedNetworks']:
                broadcasted_addresses.append(network['address'])

            if network_address in broadcasted_addresses:
                routers_set.append(router['name'])

        subnetwork_collections.append({network_address: routers_set})
        routers_sets.append(routers_set)

    return subnetwork_collections, routers_sets

def define_graph_edges(routers_sets):
    edges = []
    for routers_set in routers_sets:
        for pair in itertools.combinations(routers_set, 2):
            edges.append(pair)

    edges = list(dict.fromkeys(edges))
    directed_edges = []
    
    for edge in edges:
        edge = list(edge)
        directed_edges.append(edge)
        directed_edges.append(swap_edge_nodes(edge))

    return directed_edges

def swap_edge_nodes(edge):
    edge = [edge[1], edge[0]]

    return edge

def add_weights(edges):
    weighted_edges = []
    for edge in edges:
        edge.append(1)
        weighted_edges.append(edge)

    return weighted_edges