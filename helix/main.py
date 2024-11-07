import sys

from main_ui import AuthorizationScreen
from PySide6.QtWidgets import QApplication, QMainWindow
from settings import FONT

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = AuthorizationScreen()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
