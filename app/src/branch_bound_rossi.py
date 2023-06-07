import sys
from itertools import permutations


def truck_delivery_branch_and_bound(locations, max_weight):
    num_locations = len(locations)
    min_cost = sys.maxsize
    best_path = []

    def calculate_distance(p1, p2):
        return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

    def calculate_cost(path):
        cost = 0
        for i in range(num_locations - 1):
            cost += calculate_distance(locations[path[i]]['coordenadas'], locations[path[i + 1]]['coordenadas'])
        return cost

    def is_valid_path(path):
        weight = 0
        for i in range(num_locations - 1):
            loc_index = path[i]
            dest_index = path[i + 1]
            weight += locations[loc_index]['produtos']
            if weight > max_weight:
                return False
            if dest_index not in locations[loc_index]['destinos']:
                return False
        return True

    def branch_and_bound(path, visited, curr_cost):
        nonlocal min_cost, best_path

        if len(path) == num_locations:
            if is_valid_path(path):
                if curr_cost < min_cost:
                    min_cost = curr_cost
                    best_path = path[:]
            return

        for i in range(num_locations):
            if i not in visited:
                new_cost = curr_cost + calculate_distance(locations[path[-1]]['coordenadas'], locations[i]['coordenadas'])
                if new_cost < min_cost:
                    branch_and_bound(path + [i], visited.union({i}), new_cost)

    for i in range(num_locations):
        branch_and_bound([i], {i}, 0)

    return best_path, min_cost


# Exemplo de uso
locations = [
    {'numero_loja': 0, 'coordenadas': (1, 0), 'produtos': 0, 'destinos': []},
    {'numero_loja': 1, 'coordenadas': (1, 3), 'produtos': 2, 'destinos': [2, 3]},
    {'numero_loja': 2, 'coordenadas': (3, 3), 'produtos': 0, 'destinos': [0]},
    {'numero_loja': 3, 'coordenadas': (4, 4), 'produtos': 1, 'destinos': [4]},
    {'numero_loja': 4, 'coordenadas': (5, 4), 'produtos': 0, 'destinos': [0]}
]
max_weight = 10

path, cost = truck_delivery_branch_and_bound(locations, max_weight)

print("Melhor caminho encontrado:", path)
print("Custo mínimo:", cost)
