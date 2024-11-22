from PyQt5.QtWidgets import QApplication
from welcome import WelcomeWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    welcome_window = WelcomeWindow()
    welcome_window.show()
    
    sys.exit(app.exec_())
