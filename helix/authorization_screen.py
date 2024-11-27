from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
from store import Store, User
from welcome_screen import WelcomeScreen
import logging


class AuthorizationScreen:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.store = Store("database.db")
        self.users = []

    def setup_ui(self, MainWindow):
        self.logger.debug("Setting up the authorization screen UI")

        # Setting up the Main Window
        self.MainWindow = MainWindow
        self.MainWindow.setEnabled(True)
        self.MainWindow.setMinimumSize(QSize(800, 600))
        self.MainWindow.setMaximumSize(QSize(600, 400))

        # Configuring the central widget
        self.centralwidget = QWidget(self.MainWindow)
        self.centralwidget.setStyleSheet("background-color: #CADBDD")

        # Header
        self.header = QLabel(self.centralwidget)
        self.header.setGeometry(QRect(0, 0, 811, 241))
        self.header.setPixmap(QPixmap("./assets/header.png"))

        # Logo on the header
        self.logo = QLabel(self.centralwidget)
        self.logo.setGeometry(QRect(270, 0, 301, 241))
        self.logo.setStyleSheet("background-color: transparent")
        self.logo.setPixmap(QPixmap("./assets/helix-logo.png"))
        self.logo.setScaledContents(False)

        # Choose user label
        self.choose_user_label = QLabel(self.centralwidget)
        self.choose_user_label.setGeometry(QRect(115, 300, 256, 31))
        self.choose_user_label.setFont(QFont("Helvetica", 30, QFont.Bold)) #type: ignore
        self.choose_user_label.setStyleSheet("color: #666666")

        # Users drop-down menu
        self.drop_down = QComboBox(self.centralwidget)
        self.drop_down.setGeometry(QRect(375, 300, 271, 31))
        self.drop_down.setStyleSheet("font-size: 20px; color: #666666; min-width: 100px;")

        # Add user button
        plus_icon = QPixmap("./assets/plus.png")
        self.add_user_plus_button = QPushButton(QIcon(plus_icon), "", self.centralwidget)
        self.add_user_plus_button.setIconSize(QSize(24, 24))
        self.add_user_plus_button.setGeometry(QRect(660, 300, 31, 31))
        self.add_user_plus_button.setStyleSheet("border-radius: 0px")
        self.add_user_plus_button.clicked.connect(self.add_new_user_screen)

        # Submit button
        self.submit_button = QPushButton("SUBMIT", self.centralwidget)
        self.submit_button.setGeometry(QRect(570, 450, 196, 61))
        self.submit_button.setFont(QFont("Helvetica", 25, QFont.Bold)) #type: ignore
        self.submit_button.setStyleSheet("color: #cadbdd; background-color: #666666; border-radius: 5px")
        self.submit_button.clicked.connect(self.go_to_welcome_page)

        # Add user (on another screen) button
        self.add_user_button = QPushButton("ADD", self.centralwidget)
        self.add_user_button.setGeometry(QRect(570, 450, 196, 61))
        self.add_user_button.setFont(QFont("Helvetica", 25, QFont.Bold)) #type: ignore
        self.add_user_button.setStyleSheet("color: #cadbdd; background-color: #666666; border-radius: 5px")
        self.add_user_button.clicked.connect(lambda: self.add_user_to_db())
        self.add_user_button.hide()

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.retranslate_ui_main()
        QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslate_ui_main(self):
        self.logger.debug("Retranslating the authorization screen UI")

        self.MainWindow.setWindowTitle("Authorization Screen")
        self.choose_user_label.setText("Choose user:")
        self.fill_drop_down()

    def add_new_user_screen(self):
        self.logger.debug("Adding new user screen")

        self.choose_user_label.hide()
        self.drop_down.hide()
        self.add_user_plus_button.hide()
        self.submit_button.hide()

        self.input_username_text_label = QLabel("Input username:", self.centralwidget)
        self.input_username_text_label.setGeometry(QRect(115, 300, 256, 31))
        self.input_username_text_label.setFont(QFont("Helvetica", 30, QFont.Bold)) #type: ignore
        self.input_username_text_label.setStyleSheet("color: #666666")
        self.input_username_text_label.show()

        self.username_text = QLineEdit(self.centralwidget)
        self.username_text.setGeometry(QRect(375, 300, 241, 31))
        self.username_text.setStyleSheet("color: #666666; font-size: 20px")
        self.username_text.show()

        self.add_user_button.show()

    def fill_drop_down(self):
        self.logger.debug("Filling the drop down with users")

        self.users = self.store.users.list()
        self.logger.debug(f"Users: {self.users}")

        self.drop_down.clear()
        if not self.users:
            self.logger.debug("No users found")
            self.add_new_user_screen()
            return
        for user in self.users:
            self.drop_down.addItem(user.username)

    def add_user_to_db(self):
        self.logger.debug("Adding user to the database")
        username = self.username_text.text()
        self.logger.debug(f"Username: {username}")

        if not username:
            self.logger.debug("Username is empty")
            return
        new_user = User(username=username)
        if not any(user.username == new_user.username for user in self.users):
            self.logger.debug("User does not exist")
            self.store.users.create(new_user)
            self.fill_drop_down()
            self.redirect_back_to_authorization()

    def redirect_back_to_authorization(self):
        self.logger.debug("Redirecting back to the authorization screen")

        self.add_user_button.hide()
        self.input_username_text_label.hide()
        self.username_text.hide()
        self.add_user_button.close()

        self.choose_user_label.show()
        self.drop_down.show()
        self.add_user_plus_button.show()
        self.submit_button.show()

    def go_to_welcome_page(self):
        self.logger.debug("Going to the welcome screen")

        screen = WelcomeScreen()
        username = self.drop_down.currentText()
        user = self.store.users.get_by_username(username)
        self.logger.debug(f"User: {user}")
        if user:
            screen.setup_ui(self, self.store, user)
