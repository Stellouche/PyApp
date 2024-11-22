import os

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            return self.frontier.pop()

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            return self.frontier.pop(0)

class MazeSolver:
    def __init__(self, filename):
        print(f"Attempting to load maze file: {filename}")
        self.load_maze(filename)
        print("Maze loaded successfully.")
        self.solution = None

    def load_maze(self, filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"The file {filename} was not found.")
        
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1 or contents.count("B") != 1:
            raise Exception("The maze must contain one start point (A) and one goal point (B).")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        self.maze = []  # Initialize maze attribute

        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.maze.append(row)
        print(f"Maze loaded successfully: {self.maze}")

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.maze[r][c]:
                result.append((action, (r, c)))
        return result

    def solve_with_dfs(self):
        self.num_explored = 0  # Initialize the counter for explored nodes
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)
        self.explored = set()

        while True:
            if frontier.empty():
                return None

            node = frontier.remove()
            self.num_explored += 1  # Increment the explored count for each node

            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return cells

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def solve_with_bfs(self):
        self.num_explored = 0  # Initialize the counter for explored nodes
        start = Node(state=self.start, parent=None, action=None)
        frontier = QueueFrontier()
        frontier.add(start)
        self.explored = set()

        while True:
            if frontier.empty():
                return None

            node = frontier.remove()
            self.num_explored += 1  # Increment the explored count for each node

            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return cells

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
