import sys 
import random
import os
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter
from ui_main import MainWindow  # Make sure MainWindow is defined in ui_main.py

class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color

    def update(self, width, height):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x - self.radius < 0 or self.x + self.radius > width:
            self.speed_x = -self.speed_x
        if self.y - self.radius < 0 or self.y + self.radius > height:
            self.speed_y = -self.speed_y

class AnimatedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bouncing Balls')
        self.setStyleSheet("background-color: black;")
        self.balls = []
        self.num_balls = 50  # More balls for a fuller background
        self.radius = 20
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(30)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Hide window borders
        self.showFullScreen()  # Start in fullscreen mode
        self.create_balls()

    def create_balls(self):
        for _ in range(self.num_balls):
            x = random.randint(self.radius, self.width() - self.radius)
            y = random.randint(self.radius, self.height() - self.radius)
            speed_x = random.choice([-1, 1]) * random.uniform(2, 6)
            speed_y = random.choice([-1, 1]) * random.uniform(2, 6)
            color = QColor(255, 200, 120)  # Soft orange
            self.balls.append(Ball(x, y, self.radius, speed_x, speed_y, color))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        width = self.width()
        height = self.height()
        for ball in self.balls:
            painter.setBrush(ball.color)
            painter.drawEllipse(QPointF(ball.x, ball.y), ball.radius, ball.radius)
        for ball in self.balls:
            ball.update(width, height)
        painter.end()

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("☾ PyApp ☽")
        self.setStyleSheet("background-color: transparent;")  # Set background to transparent
        self.setWindowFlags(Qt.FramelessWindowHint)  # Hide window borders
        self.showFullScreen()  # Display in full screen

        # Create the animated background
        self.animated_window = AnimatedWindow()
        self.animated_window.setParent(self)  # Set the animated background as the parent window
        self.animated_window.show()  # Show the background window

        # Create the central widget
        container = QWidget()
        container_layout = QVBoxLayout()
        container.setLayout(container_layout)
        container_layout.setAlignment(Qt.AlignCenter)

        # "Exit" button in the top-right corner
        exit_button = QPushButton("Exit")
        exit_button.setFixedSize(200, 120)  # Increased size for better visibility
        exit_button.setStyleSheet("""
            font-size: 34px;
            padding: 10px;
            background-color: #F4A261;  /* Soft orange, matching the "Launch" button */
            color: white;
            border: none;
            border-radius: 10px;
        """)
        exit_button.clicked.connect(self.close_application)

        # Add the "Exit" button in a horizontal layout aligned to the right
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(exit_button)

        # Large, stylized title
        title = QLabel("☾ PyApp ☽")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 120px; 
            font-weight: bold; 
            color: #ffffff;
            margin-top: 100px;
        """)

        # Create the grey rectangle around the box
        container_rect = QWidget()
        container_rect.setStyleSheet("""
            background-color: #2F2F2F;  /* Light grey for the border */
            border-radius: 25px;  /* Rounded corners */
            padding: 40px;  /* Margins for the border */
        """)

        # Create the "Maze Resolver" box inside this rectangle
        maze_group_box = QGroupBox("Maze Resolver")
        maze_layout = QVBoxLayout()
        maze_group_box.setLayout(maze_layout)
        maze_group_box.setFixedSize(2200, 1200)  # Significantly increased size of the "Maze Resolver" box
        maze_group_box.setStyleSheet("""
            font-size: 44px; 
            font-weight: bold;
            color: #F4A261;  /* Soft orange */
            border: 3px solid #F4A261;  /* Soft orange border */
            border-radius: 25px;  /* Rounded corners */
            padding: 50px;  /* Spacing around content */
            background-color: rgba(51, 51, 51, 0.7);  /* Dark background with slight transparency for better integration */
            box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.6);  /* Soft yet marked shadow for a better effect */
        """)

        # New title inside the "Maze Resolver" box
        maze_title_label = QLabel("Maze Resolver")  # Changed the phrase here
        maze_title_label.setAlignment(Qt.AlignCenter)
        maze_title_label.setStyleSheet("""
            font-size: 58px;  /* Increased title size inside the box */
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 40px;
        """)

        # Description of the Maze Resolver
        description_label = QLabel("Solve mazes with different search methods.")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("""
            font-size: 40px;  /* Increased description text size */
            color: #ffffff;
            margin-bottom: 40px;
        """)

        # "Launch" button inside the "Maze Resolver" box
        start_button = QPushButton("Launch")
        start_button.setFixedSize(400, 150)  # Larger size for the "Launch" button
        start_button.setStyleSheet("""
            font-size: 40px; 
            padding: 10px;
            background-color: #F4A261;  /* Soft orange */
            color: white;
            border: none;
            border-radius: 10px;
        """)
        start_button.clicked.connect(self.start_application)

        # Add the description and the button to the box
        maze_layout.addWidget(maze_title_label)  # Title added to the top of the box
        maze_layout.addWidget(description_label)
        maze_layout.addWidget(start_button, alignment=Qt.AlignCenter)

        # Add the box in the container with the border
        container_layout.addLayout(top_layout)    # "Exit" button in the top right corner
        container_layout.addWidget(title, alignment=Qt.AlignCenter)  # Centered title
        container_layout.addStretch()             # Flexible space below the title
        container_rect.setLayout(maze_layout)  # Link the box to the grey container
        container_layout.addWidget(container_rect, alignment=Qt.AlignCenter)  # Centered "Maze Resolver" box with border
        container_layout.addStretch()             # Flexible space below the component

        self.setCentralWidget(container)

    def resizeEvent(self, event):
        pass  # No longer need to update the background since we're using the animated background

    def start_application(self):
        # Close this window and open the main window
        self.close()
        self.main_window = MainWindow()
        self.main_window.showFullScreen()  # Display in full screen

    def close_application(self):
        # Close the application
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    sys.exit(app.exec_())
