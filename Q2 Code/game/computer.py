from .graph import dfs_path
from .graph import bfs_path

class Computer:
    def __init__(self, start, goal, graph):
        self.position = start
        self.goal = goal
        self.graph = graph
        self.path = bfs_path(graph, start, goal)
        self.next_index = 1

        if self.path is None:
            print("No path found for the computer from", start, "to", goal)

    def move_next(self):
        if self.path is None:
            return
        if self.next_index < len(self.path):
            self.position = self.path[self.next_index]
            self.next_index += 1
