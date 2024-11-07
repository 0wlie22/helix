from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from welcome import WelcomeScreen


class AuthorizationScreen(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow

        if not self.MainWindow.objectName():
            self.MainWindow.setObjectName("self.MainWindow")
        self.MainWindow.setEnabled(True)
        self.MainWindow.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainWindow.sizePolicy().hasHeightForWidth())
        self.MainWindow.setSizePolicy(sizePolicy)
        self.MainWindow.setMinimumSize(QSize(800, 600))
        self.MainWindow.setMaximumSize(QSize(600, 400))
        self.centralwidget = QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("background-color: #CADBDD")
        self.header = QLabel(self.centralwidget)
        self.header.setObjectName("header")
        self.header.setGeometry(QRect(0, 0, 811, 241))
        self.header.setPixmap(QPixmap("./assets/header.png"))
        self.logo = QLabel(self.centralwidget)
        self.logo.setObjectName("logo")
        self.logo.setGeometry(QRect(270, 0, 301, 241))
        self.logo.setStyleSheet("background-color: transparent")
        self.logo.setPixmap(QPixmap("./assets/helix-logo.png"))
        self.logo.setScaledContents(False)
        self.choose_user = QLabel(self.centralwidget)
        self.choose_user.setObjectName("choose_user")
        self.choose_user.setGeometry(QRect(115, 300, 256, 31))
        font = QFont()
        font.setFamily("Helvetica")
        font.setPointSize(30)
        font.setBold(True)
        self.choose_user.setFont(font)
        self.choose_user.setStyleSheet("QLabel {\n" "	color: #666666\n" "}")
        self.drop_down = QComboBox(self.centralwidget)
        self.drop_down.setObjectName("drop_down")
        self.drop_down.setGeometry(QRect(375, 300, 271, 31))
        self.drop_down.setStyleSheet("font-size: 30px; \n" "color: #666666; \n" "min-width: 100px;\n" "")
        self.add_user = QLabel(self.centralwidget)
        self.add_user.setObjectName("add_user")
        self.add_user.setGeometry(QRect(660, 300, 31, 31))
        font1 = QFont()
        font1.setBold(False)
        # self.add_user.setPixmap(QPixmap("./assets/plus.png"))
        # self.add_user.setScaledContents(True)
        # self.add_user.setIndent(100)
        image = QPixmap("./assets/plus.png")
        self.add_user = QPushButton(QIcon(image), "", self.centralwidget)
        self.add_user.setIconSize(QSize(24, 24))  # Set the icon size
        self.add_user.setGeometry(QRect(660, 300, 31, 31))  # Ensure the button size is appropriate
        self.add_user.clicked.connect(self.add_new_user)
        self.add_user.show()

        self.submit_button = QPushButton(self.centralwidget)
        self.submit_button.setObjectName("submit_button")
        self.submit_button.setGeometry(QRect(570, 450, 196, 61))
        self.submit_button.clicked.connect(self.test)
        font2 = QFont()
        font2.setFamily("Helvetica")
        font2.setPointSize(25)
        font2.setBold(True)
        self.submit_button.setFont(font2)
        self.submit_button.setStyleSheet("color: #cadbdd; background-color: #666666; border-radius: 5px")
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self.MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self):
        self.MainWindow.setWindowTitle(QCoreApplication.translate("self.MainWindow", "self.MainWindow", None))
        self.header.setText("")
        self.logo.setText("")
        self.choose_user.setText(QCoreApplication.translate("self.MainWindow", "Choose user:", None))
        self.choose_user.setProperty("color", QCoreApplication.translate("self.MainWindow", "#666666", None))
        self.submit_button.setText(QCoreApplication.translate("self.MainWindow", "SUBMIT", None))

    def retranslateUi2(self):
        self.MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        self.input_username.setText(QCoreApplication.translate("MainWindow", "Input username:", None))
        self.input_username.setProperty("color", QCoreApplication.translate("self.MainWindow", "#666666", None))
        self.submit_button.setText(QCoreApplication.translate("self.MainWindow", "SUBMIT", None))

    def add_new_user(self):
        self.choose_user.close()
        self.drop_down.close()
        self.add_user.close()

        self.input_username = QLabel(self.centralwidget)
        self.input_username.setObjectName("input_username")
        self.input_username.setGeometry(QRect(115, 300, 256, 31))
        self.input_username.show()
        font = QFont()
        font.setFamily("Helvetica")
        font.setPointSize(30)
        font.setBold(True)
        self.input_username.setFont(font)
        self.input_username.setStyleSheet("QLabel {\n" "	color: #666666\n" "}")

        self.username_text = QLineEdit(self.centralwidget)
        self.username_text.setObjectName("username_text")
        self.username_text.setGeometry(QRect(375, 300, 241, 31))
        self.username_text.setStyleSheet("color: #666666; font-size: 20px")
        self.username_text.show()

        self.retranslateUi2()

        QMetaObject.connectSlotsByName(self.MainWindow)

    def test(self):
        screen = WelcomeScreen()
        screen.setupUi(self.MainWindow)
