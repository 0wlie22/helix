from PySide6.QtCore import * #type: ignore
from PySide6.QtGui import * #type: ignore
from PySide6.QtWidgets import * #type: ignore
from store import User

from categories_screen import CategoriesScreen


class WelcomeScreen(object):
    def setup_ui(self, MainWindow, user: User, screen):
        self.user = user
        self.authorization_screen = screen
        self.MainWindow = MainWindow
        self.MainWindow.setEnabled(True)
        sizePolicy = QSizePolicy()
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainWindow.sizePolicy().hasHeightForWidth())
        self.MainWindow.setSizePolicy(sizePolicy)
        self.MainWindow.setMinimumSize(QSize(800, 600))
        self.MainWindow.setMaximumSize(QSize(600, 400))
        
        self.centralwidget = QWidget(self.MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("background-color: #CADBDD")

        self.header = QLabel(self.centralwidget)
        self.header.setGeometry(QRect(0, 0, 811, 331))
        self.header.setPixmap(QPixmap("./assets/header.png"))

        self.logo = QLabel(self.centralwidget)
        self.logo.setGeometry(QRect(30, 30, 241, 241))
        self.logo.setStyleSheet("background-color: transparent")
        self.logo.setPixmap(QPixmap("./assets/helix-logo.png"))
        self.logo.setScaledContents(False)

        self.welcome_user_label = QLabel(self.centralwidget)
        self.welcome_user_label.setGeometry(QRect(75, 360, 391, 61))
        font = QFont("Helvetica")
        font.setBold(True)
        self.welcome_user_label.setFont(font)
        self.welcome_user_label.setStyleSheet("background-color: transparent; color: #666666; font-size: 40px;")

        self.dictionary_button = QPushButton(self.centralwidget)
        self.dictionary_button.setGeometry(QRect(75, 450, 196, 61))
        self.dictionary_button.clicked.connect(lambda: self.go_to_categories_screen())
        self.dictionary_button.show()
        font = QFont("Helvetica", 25)
        self.dictionary_button.setFont(font)
        self.dictionary_button.setStyleSheet("color: #cadbdd; background-color: #666666; border-radius: 5px")
        self.log_out_button = QPushButton(self.centralwidget)
        self.log_out_button.setGeometry(QRect(570, 450, 196, 61))
        self.log_out_button.setFont(font)
        self.log_out_button.setStyleSheet("color: #666666; border-radius: 5px")
        self.log_out_button.clicked.connect(self.go_to_authorization_screen)

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self):
        self.MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        welcome_text = f"Welcome, {self.user.username.upper()}!"
        self.welcome_user_label.setText(QCoreApplication.translate("self.MainWindow", welcome_text, None))
        self.dictionary_button.setText(QCoreApplication.translate("self.MainWindow", "Dictionary", None))
        self.log_out_button.setText(QCoreApplication.translate("self.MainWindow", "log out", None))

    def go_to_categories_screen(self):
        categories_screen = CategoriesScreen()
        categories_screen.setup_ui(self.MainWindow, self.user)

    def go_to_authorization_screen(self):
        self.authorization_screen.setup_ui(self.MainWindow)
