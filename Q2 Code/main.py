import tkinter as tk
from game.graph import generate_valid_graph
from game.player import Player
from game.computer import Computer

class RaceToTheGoalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Race to the Goal")

        self.node_radius = 15
        self.start = (0, 0)
        self.goal = (4, 4)

        # Create graph
        self.graph = generate_valid_graph()

        # Initialize players
        self.player = Player(self.start)
        self.computer = Computer(self.start, self.goal, self.graph)

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.redraw)

        # Keyboard control
        self.root.bind("<Key>", self.handle_keypress)

        self.restart_button = None

    def redraw(self, event=None):
        self.canvas.delete("all")

        # Draw computer's path (debug/visual aid)
        if self.computer.path:
            for i in range(len(self.computer.path) - 1):
                x1, y1 = self.node_to_canvas_coords(self.computer.path[i])
                x2, y2 = self.node_to_canvas_coords(self.computer.path[i + 1])
                self.canvas.create_line(x1, y1, x2, y2, fill="lightgray", dash=(4, 2))

        # Draw edges
        for node, neighbors in self.graph.items():
            x1, y1 = self.node_to_canvas_coords(node)
            for n in neighbors:
                x2, y2 = self.node_to_canvas_coords(n)
                self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

        # Draw nodes
        for node in self.graph.keys():
            if node == self.start:
                self.draw_node(node, "blue")
            elif node == self.goal:
                self.draw_node(node, "green")
            else:
                self.draw_node(node, "white")

        # Draw players
        if self.player.position == self.computer.position:
            self.draw_half_colored_circle(self.player.position, "red", "yellow")
        else:
            self.draw_player(self.player.position, "red", "player")
            self.draw_player(self.computer.position, "yellow", "computer")

    def draw_half_colored_circle(self, node, color1, color2):
        cx, cy = self.node_to_canvas_coords(node)
        r = self.node_radius
        # Setengah lingkaran merah (dari 90° ke 270°)
        self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                               start=90, extent=180, fill=color1, outline="black")
        # Setengah lingkaran kuning (dari 270° ke 450° atau 90°)
        self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                               start=270, extent=180, fill=color2, outline="black")

    def node_to_canvas_coords(self, node):
        max_x = max(n[0] for n in self.graph.keys())
        max_y = max(n[1] for n in self.graph.keys())
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        padding = self.node_radius * 3

        spacing_x = (width - 2 * padding) / max_x if max_x != 0 else 0
        spacing_y = (height - 2 * padding) / max_y if max_y != 0 else 0

        cx = node[0] * spacing_x + padding
        cy = node[1] * spacing_y + padding
        return cx, cy

    def draw_node(self, node, color):
        cx, cy = self.node_to_canvas_coords(node)
        r = self.node_radius
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=color, outline="black")

    def draw_player(self, node, color, tag):
        cx, cy = self.node_to_canvas_coords(node)
        r = self.node_radius * 0.6
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=color, tags=tag)

    def handle_keypress(self, event):
        move_map = {
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0)
        }
        
        move = move_map.get(event.char.lower())
        if move:
            new_pos = (self.player.position[0] + move[0], self.player.position[1] + move[1])
            if new_pos in self.graph.get(self.player.position, []):
                self.player.position = new_pos
                self.redraw()
                if self.check_winner():
                    return
                self.computer.move_next()
                self.redraw()
                self.check_winner()

    def check_winner(self):
        if self.player.position == self.goal:
            self.display_winner("You Win!")
            return True
        elif self.computer.position == self.goal:
            self.display_winner("You Lose:(")
            return True
        return False

    def display_winner(self, message):
        self.canvas.create_rectangle(
            0, 0,
            self.canvas.winfo_width(), self.canvas.winfo_height(),
            fill="black",
            stipple="gray50",
            tags="overlay"
        )

        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2 - 30,
            text=message,
            font=("Helvetica", 32, "bold"),
            fill="white",
            tags="winner"
        )

        self.root.unbind("<Key>")

        self.restart_button = tk.Button(self.root, text="Play Again", font=("Helvetica", 14), command=self.restart_game)
        self.canvas.create_window(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2 + 30,
            window=self.restart_button,
            tags="winner"
        )

    def restart_game(self):
        if self.restart_button:
            self.restart_button.destroy()
        self.canvas.delete("overlay")
        self.canvas.delete("winner")
        self.graph = generate_valid_graph()
        self.player = Player(self.start)
        self.computer = Computer(self.start, self.goal, self.graph)
        self.root.bind("<Key>", self.handle_keypress)
        self.redraw()

if __name__ == "__main__":
    root = tk.Tk()
    app = RaceToTheGoalApp(root)
    root.mainloop()
