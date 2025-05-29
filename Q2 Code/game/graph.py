import random
from collections import deque

SIZE = 5
START = (0, 0)
GOAL = (SIZE - 1, SIZE - 1)

def generate_random_graph(size=SIZE, block_prob=0.5):
    graph = { (x, y): [] for x in range(size) for y in range(size) }  # Inisialisasi semua node

    for x in range(size):
        for y in range(size):
            node = (x, y)
            potential_neighbors = [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1)
            ]
            for nx, ny in potential_neighbors:
                if 0 <= nx < size and 0 <= ny < size:
                    if random.random() > block_prob:
                        # Tambahkan edge dua arah
                        if (nx, ny) not in graph[node]:
                            graph[node].append((nx, ny))
                        if node not in graph[(nx, ny)]:
                            graph[(nx, ny)].append(node)

    # Pastikan START dan GOAL punya minimal satu tetangga
    if not graph[START]:
        fallback_neighbors = [(START[0] + 1, START[1]), (START[0], START[1] + 1)]
        for neighbor in fallback_neighbors:
            if 0 <= neighbor[0] < size and 0 <= neighbor[1] < size:
                graph[START].append(neighbor)
                graph[neighbor].append(START)

    if not graph[GOAL]:
        fallback_neighbors = [(GOAL[0] - 1, GOAL[1]), (GOAL[0], GOAL[1] - 1)]
        for neighbor in fallback_neighbors:
            if 0 <= neighbor[0] < size and 0 <= neighbor[1] < size:
                graph[GOAL].append(neighbor)
                graph[neighbor].append(GOAL)

    return graph

def dfs_path(graph, start, goal, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    if start == goal:
        return [start]
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            path = dfs_path(graph, neighbor, goal, visited)
            if path:
                return [start] + path
    return None

def bfs_path(graph, start, goal):
    queue = deque([[start]])
    visited = set([start])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None

def generate_valid_graph():
    while True:
        g = generate_random_graph()
        path_dfs = dfs_path(g, START, GOAL)
        path_bfs = bfs_path(g, START, GOAL)
        if path_dfs and path_bfs:
            return g
