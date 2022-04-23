from random import randint
import math

import matplotlib.pyplot as plt


def choose_random_cities(cities_count: int, plot_size_x: tuple, plot_size_y: tuple):
    points = set()
    while len(points) != cities_count:
        points.add((randint(*plot_size_x), randint(*plot_size_y)))
    return tuple(points)


def create_connections(city_coords: tuple, percentage: float = 1.):
    """Creates tuples of coordinates for plotting roads"""
    count = 0

    num_of_connections = 0
    max_connections = len(city_coords) * (len(city_coords) - 1) // 2
    for p_1 in city_coords:
        count += 1
        for p_2 in city_coords[count:]:
            num_of_connections += 1
            if num_of_connections / max_connections > percentage:
                return None

            axis_x = (p_1[0], p_2[0])
            axis_y = (p_1[1], p_2[1])
            yield tuple(axis_x), tuple(axis_y)


def create_distances_matrix(city_coords: tuple, percentage: float = 1.):
    """Creates matrix of distances"""

    number_of_cities = len(city_coords)

    adjacency_matrix = [[0. for _ in range(number_of_cities)] for _ in range(number_of_cities)]
    max_connections = number_of_cities * (number_of_cities - 1) // 2

    num_of_connections = 0
    for i in range(number_of_cities):
        for j in range(i + 1, number_of_cities):
            num_of_connections += 1
            if num_of_connections / max_connections > percentage:
                adjacency_matrix[i][j] = math.inf
                adjacency_matrix[j][i] = math.inf
                continue

            distance = math.sqrt((city_coords[i][0] - city_coords[j][0]) ** 2
                                 + (city_coords[i][1] - city_coords[j][1]) ** 2)

            adjacency_matrix[i][j] = distance
            adjacency_matrix[j][i] = distance

    return adjacency_matrix


def plot_cities_graph(city_coords: tuple, distances_matrix: list):
    """Plots graphs of cities and roads between them"""

    for i in range(len(city_coords)):
        #  plotting cities and their number
        plt.plot(*city_coords[i], ".", markersize=1)
        plt.annotate(i, city_coords[i], ha="center", color="w", bbox=dict(boxstyle='square', fc='black', alpha=1))

        for j in range(i + 1, len(city_coords)):
            if distances_matrix[i][j] == math.inf:
                break

            #  calculating coordinates for roads between cities
            road_coords_x = (city_coords[i][0], city_coords[j][0])
            road_coords_y = (city_coords[i][1], city_coords[j][1])
            middle_road_coords = (sum(road_coords_x) // 2, sum(road_coords_y) // 2)

            #  plotting road connections and distances
            plt.plot(road_coords_x, road_coords_y, "-y", markersize=1)
            plt.annotate(round(distances_matrix[i][j], 1), middle_road_coords, ha="center", va="bottom")

    plt.show()


def bfs(start_city: int, cities_num: int, cost_matrix_: list):
    """BFS search for the road of the lowest cost"""
    cities_set = set(range(cities_num))

    def bfs_recurrence(paths):
        paths_new = []
        for cost, path in paths:
            cities_left = cities_set - set(path)
            if not len(cities_left):
                return paths
            for city in cities_left:
                paths_new.append((cost + cost_matrix_[path[-1]][city], (*path, city)))
                print(paths_new[-1][-1])  # Shows the steps
        return bfs_recurrence(paths_new)

    #  Adding the cost of returning to the starting city
    paths_completed = []
    print((start_city,))  # Shows the first step
    for cost_last, path_last in bfs_recurrence([(0, (start_city,))]):
        paths_completed.append((cost_last + cost_matrix_[path_last[-1]][start_city], path_last + (start_city,)))
        print(paths_completed[-1][-1])  # Shows the last step

    return paths_completed


def dfs(start_city: int, cities_num: int, cost_matrix_: list):
    """DFS search for the road of the lowest cost"""

    cities_set = set(range(cities_num)) - {start_city}
    full_paths = list()

    def dfs_recurrence(available_roads, current_cost, current_path, current_city, paths_list):
        current_path = (*current_path, current_city)
        print(current_path)  # Shows the steps
        if not len(available_roads):
            paths_list.append((current_cost, current_path))

        available_roads -= {current_city}

        for next_city in available_roads:
            cost = current_cost + cost_matrix_[current_city][next_city]
            dfs_recurrence(available_roads - {next_city}, cost, current_path, next_city, paths_list)

    dfs_recurrence(cities_set, 0, tuple(), start_city, full_paths)

    #  Adding the cost of returning to the starting city
    paths_completed = []
    for cost_last, path_last in full_paths:
        paths_completed.append((cost_last + cost_matrix_[path_last[-1]][start_city],
                                path_last + (start_city,)))
        print(paths_completed[-1][-1])  # Shows the steps
    return paths_completed


def greedy_search(start_city: int, cities_num: int, cost_matrix_: list):
    """Greedy approach of searching for the path of the lowest cost"""

    cities_set = set(range(cities_num)) - {start_city}

    def greedy_recurrence(available_roads, current_cost, current_path, current_city):
        current_path = (*current_path, current_city)
        print(current_path)

        if not len(available_roads):
            cost = cost_matrix_[current_city][start_city]
            if math.isinf(cost):
                return None
            print(current_path + (start_city,))
            return (current_cost + cost,
                    current_path + (start_city,))

        available_roads -= {current_city}

        #  Sorting the paths for the lowest cost
        costs = []
        for city in available_roads:
            costs += [[city, cost_matrix_[current_city][city]]]
        costs.sort(key=lambda x: x[1])

        for next_city, cost in costs:
            if math.isinf(cost):
                continue
            cost += current_cost
            recurrence = greedy_recurrence(available_roads - {next_city}, cost, current_path, next_city)
            if recurrence is not None:
                return recurrence

    return greedy_recurrence(cities_set, 0, tuple(), start_city)


if __name__ == '__main__':
    num_cities = 5
    cities = choose_random_cities(num_cities, (-100, 100), (-100, 100))  # creating the cities
    cost_matrix = create_distances_matrix(cities, 1)  # creating the cost matrix

    print("Paths of DFS:\n")
    paths_taken_dfs = dfs(3, num_cities, cost_matrix)
    print("\nPaths of BFS:\n")
    paths_taken_bfs = bfs(3, num_cities, cost_matrix)
    print("\nPath of greedy search:\n")
    path_taken_greedy = greedy_search(3, num_cities, cost_matrix)

    min_path_dfs = min(paths_taken_dfs, key=lambda x: x[0])
    min_path_bfs = min(paths_taken_bfs, key=lambda x: x[0])

    print("\nDFS min path:\t", min_path_dfs)
    print("BFS min path:\t", min_path_bfs)
    print("greedy path:\t", path_taken_greedy)
    plot_cities_graph(cities, cost_matrix)

