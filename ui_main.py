from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QSizePolicy, QRadioButton, QGroupBox, QFormLayout, QSpacerItem, QFileDialog
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from maze_solver import MazeSolver
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Maze Solver")
        self.setStyleSheet("background-color: #1e1e1e;")

        layout = QVBoxLayout()

        self.view = QGraphicsView()
        self.view.setMinimumSize(800, 600)
        self.view.setScene(QGraphicsScene(self))
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.view)

        button_layout = QHBoxLayout()

        self.load_button = QPushButton("Load Maze")
        self.load_button.setStyleSheet("""
            font-size: 40px;
            padding: 25px;
            background-color: #A3C8FC;
            color: black;
            border: none;
            border-radius: 15px;
        """)
        button_layout.addWidget(self.load_button)

        self.solve_button = QPushButton("Solve")
        self.solve_button.setStyleSheet("""
            font-size: 40px;
            padding: 25px;
            background-color: #A1E1A1;
            color: black;
            border: none;
            border-radius: 15px;
        """)
        button_layout.addWidget(self.solve_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setStyleSheet("""
            font-size: 40px;
            padding: 25px;
            background-color: #F4A3A3;
            color: black;
            border: none;
            border-radius: 15px;
        """)
        button_layout.addWidget(self.reset_button)

        layout.addLayout(button_layout)

        self.info_label = QLabel("Information:")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("""
            font-size: 48px;
            color: #ffffff;
        """)
        layout.addWidget(self.info_label)

        self.radio_layout = QHBoxLayout()
        self.radio_group = QGroupBox("Select Search Method:")
        self.radio_group.setStyleSheet("color: white;")
        self.dfs_radio = QRadioButton("Depth-First-Search: Expands the deepest node in the frontier.")
        self.dfs_radio.setStyleSheet("""
            font-size: 20px;
            padding: 10px;
            color: white;
        """)
        self.bfs_radio = QRadioButton("Breadth-First-Search: Expands the shallowest node in the frontier.")
        self.bfs_radio.setStyleSheet("""
            font-size: 20px;
            padding: 10px;
            color: white;
        """)

        self.dfs_radio.setChecked(True)

        self.radio_layout.addWidget(self.dfs_radio)
        self.radio_layout.addWidget(self.bfs_radio)
        self.radio_group.setLayout(self.radio_layout)

        layout.addWidget(self.radio_group)

        self.return_button = QPushButton("Return to Home")
        self.return_button.setStyleSheet("""
            font-size: 26px;
            padding: 20px;
            background-color: #FFB14C;
            color: black;
            border: none;
            border-radius: 15px;
        """)
        self.return_button.clicked.connect(self.return_to_home)

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.return_button)
        layout.addLayout(top_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_button.clicked.connect(self.load_maze)
        self.solve_button.clicked.connect(self.solve_maze)
        self.reset_button.clicked.connect(self.reset_maze)

        self.solver = None

        self.dfs_radio.toggled.connect(self.update_method_info)
        self.bfs_radio.toggled.connect(self.update_method_info)

    def load_maze(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Maze File", "", "Text Files (*.txt)")
        if filename:
            try:
                self.solver = MazeSolver(filename)
                self.info_label.setText("Maze loaded.")
                self.draw_maze()
                self.update_method_info()  
            except Exception as e:
                self.info_label.setText(f"Error: {str(e)}")

    def solve_maze(self):
        if self.solver is not None:
            search_method = "DFS" if self.dfs_radio.isChecked() else "BFS"
            solution = self.solver.solve_with_dfs() if search_method == "DFS" else self.solver.solve_with_bfs()
            if solution:
                self.info_label.setText(f"Solution found with {len(solution)} steps (method: {search_method}, {self.solver.num_explored} nodes explored).")
                self.draw_solution(solution)
            else:
                self.info_label.setText("No solution found.")
        else:
            self.info_label.setText("Please load a maze first.")

    def reset_maze(self):
        if self.solver:
            self.draw_maze()
            self.info_label.setText("Maze reset.")

    def draw_maze(self):
        scene = self.view.scene()
        scene.clear()

        if self.solver is None:
            return

        maze_width = self.solver.width
        maze_height = self.solver.height
        view_width = self.view.size().width()
        view_height = self.view.size().height()

        cell_size = min(view_width // maze_width, view_height // maze_height)

        for row, line in enumerate(self.solver.maze):
            for col, cell in enumerate(line):
                color = QColor("black") if cell else QColor("white")
                rect = scene.addRect(col * cell_size, row * cell_size, cell_size, cell_size)
                rect.setBrush(color)

        start_x = self.solver.start[1] * cell_size
        start_y = self.solver.start[0] * cell_size
        scene.addRect(start_x, start_y, cell_size, cell_size).setBrush(QColor("red"))
        scene.addText("A").setPos(start_x + (cell_size // 4), start_y + (cell_size // 4))

        goal_x = self.solver.goal[1] * cell_size
        goal_y = self.solver.goal[0] * cell_size
        scene.addRect(goal_x, goal_y, cell_size, cell_size).setBrush(QColor("green"))
        scene.addText("B").setPos(goal_x + (cell_size // 4), goal_y + (cell_size // 4))

    def draw_solution(self, solution):
        scene = self.view.scene()

        if self.solver is None:
            return

        maze_width = self.solver.width
        maze_height = self.solver.height
        view_width = self.view.size().width()
        view_height = self.view.size().height()

        cell_size = min(view_width // maze_width, view_height // maze_height)

        for pos in solution:
            scene.addRect(pos[1] * cell_size, pos[0] * cell_size, cell_size, cell_size).setBrush(QColor("yellow"))

    def return_to_home(self):
        self.close()
        from welcome import WelcomeWindow
        self.welcome_window = WelcomeWindow()
        self.welcome_window.showFullScreen()

    def update_method_info(self):
        self.draw_maze()

        if self.dfs_radio.isChecked():
            self.info_label.setText("DFS: Expands the deepest node in the frontier.")
        elif self.bfs_radio.isChecked():
            self.info_label.setText("BFS: Expands the shallowest node in the frontier.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()  
    sys.exit(app.exec_())
