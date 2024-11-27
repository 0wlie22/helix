import sys
import logging

from start_screen import StartScreen
from PySide6.QtWidgets import QApplication, QMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(name)s - %(levelname)s - %(message)s')

    MainWindow = QMainWindow()
    ui = StartScreen()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
