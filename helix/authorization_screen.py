import sqlite3

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
from store import UsersStore, User
from welcome_screen import WelcomeScreen


class AuthorizationScreen(object):
    def setup_ui(self, MainWindow):
        self.connection = sqlite3.connect("database.db")

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
        self.header.setGeometry(QRect(0, 0, 811, 241))
        self.header.setPixmap(QPixmap("./assets/header.png"))

        self.logo = QLabel(self.centralwidget)
        self.logo.setGeometry(QRect(270, 0, 301, 241))
        self.logo.setStyleSheet("background-color: transparent")
        self.logo.setPixmap(QPixmap("./assets/helix-logo.png"))
        self.logo.setScaledContents(False)

        self.choose_user_label = QLabel(self.centralwidget)
        self.choose_user_label.setGeometry(QRect(115, 300, 256, 31))
        font = QFont("Helvetica", 30)
        font.setBold(True)
        self.choose_user_label.setFont(font)
        self.choose_user_label.setStyleSheet("color: #666666")

        self.drop_down = QComboBox(self.centralwidget)
        self.drop_down.setGeometry(QRect(375, 300, 271, 31))
        self.drop_down.setStyleSheet("font-size: 20px; color: #666666; min-width: 100px;")

        image = QPixmap("./assets/plus.png")
        self.add_user_plus_button = QPushButton(QIcon(image), "", self.centralwidget)
        self.add_user_plus_button.setIconSize(QSize(24, 24))
        self.add_user_plus_button.setGeometry(QRect(660, 300, 31, 31))
        self.add_user_plus_button.setStyleSheet("border-radius: 0px")
        self.add_user_plus_button.clicked.connect(self.add_new_user_screen)

        self.submit_button = QPushButton(self.centralwidget)
        self.submit_button.setGeometry(QRect(570, 450, 196, 61))
        self.submit_button.clicked.connect(self.go_to_welcome_page)
        subfont = QFont("Helvetica", 25)
        subfont.setBold(True)
        self.submit_button.setFont(subfont)
        self.submit_button.setStyleSheet("color: #cadbdd; background-color: #666666; border-radius: 5px")
        
        self.add_user_button = QPushButton(self.centralwidget)
        self.add_user_button.setGeometry(QRect(570, 450, 196, 61))
        self.add_user_button.clicked.connect(self.add_user_to_db)
        self.add_user_button.setFont(subfont)
        self.add_user_button.setStyleSheet("color: #cadbdd; background-color: #666666; border-radius: 5px")
        self.add_user_button.hide()
        
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.retranslate_ui_main()

        QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslate_ui_main(self):
        self.MainWindow.setWindowTitle(QCoreApplication.translate("self.MainWindow", "self.MainWindow", None))
        self.choose_user_label.setText(QCoreApplication.translate("self.MainWindow", "Choose user:", None))
        self.choose_user_label.setProperty("color", QCoreApplication.translate("self.MainWindow", "#666666", None))
        self.submit_button.setText(QCoreApplication.translate("self.MainWindow", "SUBMIT", None))
        self.fill_drop_down()

    def retranslate_ui_for_new_user_screen(self):
        self.MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        self.input_username_text_label.setText(QCoreApplication.translate("MainWindow", "Input username:", None))
        self.input_username_text_label.setProperty("color", QCoreApplication.translate("self.MainWindow", "#666666", None))
        self.add_user_button.setText(QCoreApplication.translate("self.MainWindow", "ADD", None))

    def add_new_user_screen(self):
        self.choose_user_label.close()
        self.drop_down.close()
        self.add_user_plus_button.close()
        self.submit_button.close()

        self.input_username_text_label = QLabel(self.centralwidget)
        self.input_username_text_label.setObjectName("input_username")
        self.input_username_text_label.setGeometry(QRect(115, 300, 256, 31))
        self.input_username_text_label.show()
        font = QFont()
        font.setFamily("Helvetica")
        font.setPointSize(30)
        font.setBold(True)
        self.input_username_text_label.setFont(font)
        self.input_username_text_label.setStyleSheet("QLabel {\n" "	color: #666666\n" "}")

        self.username_text = QLineEdit(self.centralwidget)
        self.username_text.setObjectName("username_text")
        self.username_text.setGeometry(QRect(375, 300, 241, 31))
        self.username_text.setStyleSheet("color: #666666; font-size: 20px")
        self.username_text.show()

        self.add_user_button.show()

        self.retranslate_ui_for_new_user_screen()

        QMetaObject.connectSlotsByName(self.MainWindow)

    def fill_drop_down(self):
        connection = sqlite3.connect("database.db")
        self.users = UsersStore(connection).list()
        self.drop_down.clear()  # Clear all existing items in the dropdown
        if len(self.users) == 0:
            self.add_new_user_screen()
            return
        for user in self.users:
            self.drop_down.addItem(user.username)
        connection.close()

    def go_to_welcome_page(self):
        screen = WelcomeScreen()
        username = self.drop_down.currentText()
        user = UsersStore(self.connection).get_by_username(username)
        screen.setup_ui(self.MainWindow, user, self)

    def add_user_to_db(self):
        username = self.username_text.text()
        if username == "":
            return False
        else:
            self.new_user = User(username=username)
            if self.new_user not in self.users:
                UsersStore(self.connection).create(self.new_user)
                self.connection.commit()
            else:
                return False

            self.connection.close()

        self.fill_drop_down()
        self.redirect_back()

    def redirect_back(self):
        self.add_user_button.hide()
        self.input_username_text_label.hide()
        self.username_text.hide()

        self.submit_button.show()
        self.choose_user_label.show()
        self.drop_down.show()
        self.add_user_plus_button.show()
