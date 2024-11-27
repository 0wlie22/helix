from authorization_screen import AuthorizationScreen
from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
import logging


class StartScreen(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def setup_ui(self, MainWindow):
        self.logger.debug("Setting up the start screen UI")

        # Setting up the Main Window
        self.MainWindow = MainWindow
        self.MainWindow.setEnabled(True)
        sizePolicy = QSizePolicy()
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainWindow.sizePolicy().hasHeightForWidth())
        self.MainWindow.setSizePolicy(sizePolicy)
        self.MainWindow.setMinimumSize(QSize(800, 600))
        self.MainWindow.setMaximumSize(QSize(600, 400))
        self.MainWindow.setIconSize(QSize(64, 64))

        # Configuring the cental widget
        self.centralwidget = QWidget(self.MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("background-color: #CADBDD")

        # Header
        self.header = QLabel(self.centralwidget)
        self.header.setGeometry(QRect(1, -3, 813, 555))
        self.header.setFont(QFont("Helvetica", 25, QFont.Bold)) #type: ignore
        self.header.setPixmap(QPixmap("./assets/header.png"))

        # Logo on the header
        self.logo = QLabel(self.centralwidget)
        self.logo.setGeometry(QRect(270, 75, 245, 239))
        self.logo.setStyleSheet("background-color: transparent;")
        self.logo.setPixmap(QPixmap("./assets/helix-logo.png"))
        self.logo.show()

        # Let's go button
        self.lets_go_button = QPushButton(self.centralwidget)
        self.lets_go_button.setObjectName("pushButton")
        self.lets_go_button.setGeometry(QRect(285, 345, 226, 61))
        self.lets_go_button.setFont(QFont("Helvetica", 25, QFont.Bold)) #type: ignore
        self.lets_go_button.setStyleSheet("background-color: #666666; border-radius: 5px; color: #cadbdd")
        self.lets_go_button.clicked.connect(self.go_to_authorization_screen)

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.retranslate_ui()
        QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslate_ui(self):
        self.logger.debug("Retranslating the ui")

        self.MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        self.lets_go_button.setText(QCoreApplication.translate("self.MainWindow", "LET'S GO!", None))

    def go_to_authorization_screen(self):
        self.logger.debug("Going to the authorization screen")

        self.AuthorizationScreen = AuthorizationScreen()
        self.AuthorizationScreen.setup_ui(self.MainWindow)
