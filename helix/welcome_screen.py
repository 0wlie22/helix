from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
from store import User, Store
from categories_screen import CategoriesScreen
import logging


class WelcomeScreen:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def setup_ui(self, screen, store: Store, user: User):
        self.logger.debug("Setting up the welcome screen UI")

        self.user = user
        self.store = store
        self.authorization_screen = screen
        self.MainWindow = screen.MainWindow

        # Configure MainWindow
        self.MainWindow.setEnabled(True)
        sizePolicy = QSizePolicy()
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainWindow.sizePolicy().hasHeightForWidth())
        self.MainWindow.setSizePolicy(sizePolicy)
        self.MainWindow.setMinimumSize(QSize(800, 600))
        self.MainWindow.setMaximumSize(QSize(800, 600))
        self.MainWindow.setCentralWidget(QWidget(self.MainWindow))

        # Central widget
        self.centralwidget = QWidget(self.MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("background-color: #CADBDD")

        # Header
        self.header = QLabel(self.centralwidget)
        self.header.setGeometry(QRect(0, 0, 811, 331))
        self.header.setPixmap(QPixmap("./assets/header.png"))

        # Logo
        self.logo = QLabel(self.centralwidget)
        self.logo.setGeometry(QRect(30, 30, 241, 241))
        self.logo.setStyleSheet("background-color: transparent")
        self.logo.setPixmap(QPixmap("./assets/helix-logo.png"))
        self.logo.setScaledContents(False)

        # Welcome label
        self.welcome_user_label = QLabel(self.centralwidget)
        self.welcome_user_label.setGeometry(QRect(75, 360, 391, 61))
        self.welcome_user_label.setFont(QFont("Helvetica", 20, QFont.Bold))  # type: ignore
        self.welcome_user_label.setStyleSheet("background-color: transparent; color: #666666; font-size: 40px;")

        # Dictionary button
        self.dictionary_button = QPushButton("Dictionary", self.centralwidget)
        self.dictionary_button.setGeometry(QRect(75, 450, 196, 61))
        self.dictionary_button.setFont(QFont("Helvetica", 25))
        self.dictionary_button.setStyleSheet("color: #cadbdd; background-color: #666666; border-radius: 5px")
        self.dictionary_button.clicked.connect(lambda: self.go_to_categories_screen())

        # Log out button
        self.log_out_button = QPushButton("Log Out", self.centralwidget)
        self.log_out_button.setGeometry(QRect(300, 450, 196, 61))
        self.log_out_button.setFont(QFont("Helvetica", 25))
        self.log_out_button.setStyleSheet("color: #666666; border-radius: 5px; border-style: solid; border-width: 1px")
        self.log_out_button.clicked.connect(lambda: self.go_to_authorization_screen())

        # Set central widget
        self.MainWindow.setCentralWidget(self.centralwidget)

        # Update text
        self.retranslateUi()

    def retranslateUi(self):
        self.logger.debug("Retranslating the ui")

        self.MainWindow.setWindowTitle("Welcome Screen")
        welcome_text = f"Welcome, {self.user.username.upper()}!"
        self.welcome_user_label.setText(welcome_text)

    def go_to_authorization_screen(self):
        self.logger.debug("Going back to the authorization screen")
        self.authorization_screen.setup_ui(self.authorization_screen.MainWindow)

    def go_to_categories_screen(self):
        self.logger.debug(f"Going to the categories screen with user {self.user.username}")

        categories_screen = CategoriesScreen()
        categories_screen.setup_ui(self, self.store, self.user, self)
