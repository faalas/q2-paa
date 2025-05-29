class Player:
    def __init__(self, start_pos):
        self.position = start_pos

    def move(self, direction, graph):
        x, y = self.position
        moves = {
            "up": (x, y - 1),
            "down": (x, y + 1),
            "left": (x - 1, y),
            "right": (x + 1, y)
        }
        new_pos = moves.get(direction)
        if new_pos in graph[self.position]:
            self.position = new_pos
