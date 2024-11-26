from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
# from authorization_screen import AuthorizationScreen
from dictionary_screen import DictionaryScreen
from store import TermGroup


class StartScreen(object):
    def setup_ui(self, MainWindow):
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
        self.centralwidget = QWidget(self.MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("background-color: #CADBDD")
        self.header = QLabel(self.centralwidget)
        self.header.setGeometry(QRect(1, -3, 813, 555))
        font = QFont()
        font.setFamily("Helvetica")
        font.setPointSize(25)
        font.setBold(True)
        self.header.setFont(font)
        self.header.setPixmap(QPixmap("./assets/header.png"))

        self.logo = QLabel(self.centralwidget)
        self.logo.setObjectName("label_2")
        self.logo.setGeometry(QRect(270, 75, 245, 239))
        self.logo.setStyleSheet("background-color: transparent;")
        self.logo.setPixmap(QPixmap("./assets/helix-logo.png"))
        self.logo.show()

        self.lets_go_button = QPushButton(self.centralwidget)
        self.lets_go_button.setObjectName("pushButton")
        self.lets_go_button.setGeometry(QRect(285, 345, 226, 61))
        self.lets_go_button.setFont(font)
        self.lets_go_button.setStyleSheet("background-color: #666666; border-radius: 5px; color: #cadbdd")
        self.lets_go_button.clicked.connect(self.go_to_authorization_screen)
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self.MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslate_ui()

        QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslate_ui(self):
        self.MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        self.lets_go_button.setText(QCoreApplication.translate("self.MainWindow", "LET'S GO!", None))

    def go_to_authorization_screen(self):
        # self.AuthorizationScreen = AuthorizationScreen()
        # self.AuthorizationScreen.setup_ui(self.MainWindow)
        categories = DictionaryScreen()
        categories.setup_ui(self.MainWindow, TermGroup(1, "Default"))

