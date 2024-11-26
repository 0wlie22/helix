import sqlite3
from functools import partial

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
from store import TermGroup, TermGroupsStore, User
from dictionary_screen import DictionaryScreen


class CategoriesScreen(object):
    def setup_ui(self, MainWindow, user: User):
        self.user = user
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

        font = QFont()
        font.setPointSize(30)
        self.MainWindow.setFont(font)
        self.MainWindow.setIconSize(QSize(48, 48))
        self.centralwidget = QWidget(self.MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("background-color: #CADBDD")

        self.header = QLabel(self.centralwidget)
        self.header.setGeometry(QRect(1, -3, 813, 136))
        font = QFont()
        font.setFamily("Helvetica")
        font.setPointSize(25)
        self.header.setFont(font)
        self.header.setPixmap(QPixmap("./assets/header.png"))

        self.logo = QLabel(self.centralwidget)
        self.logo.setObjectName("label_2")
        self.logo.setGeometry(QRect(15, 15, 91, 91))
        self.logo.setStyleSheet("background-color: transparent;")
        self.logo.setPixmap(QPixmap("./assets/helix-log-small.png"))
        self.logo.setScaledContents(True)

        self.scroll_area = QScrollArea(self.centralwidget)
        self.scroll_area.setGeometry(QRect(30, 200, 750, 300))
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setStyleSheet("border-radius: 0px")

        self.categories_buttons_list = {}
        self.trashcan_buttons_list = {}
        categories = TermGroupsStore(self.connection).list()
        if len(categories) == 0:
            print("none")
            self.add_new_category("Default")
            categories = TermGroupsStore(self.connection).list()
        self.update_category_field(categories)

        image = QPixmap("./assets/plus.png")
        self.add_category_plus_button = QPushButton(QIcon(image), "", self.centralwidget)
        self.add_category_plus_button.setGeometry(QRect(705, 150, 46, 46))
        self.add_category_plus_button.setStyleSheet("border-radius: 0px")
        self.add_category_plus_button.setIconSize(QSize(48, 48))
        self.add_category_plus_button.clicked.connect(self.add_new_category_screen)

        self.header_label = QLabel(self.centralwidget)
        self.header_label.setGeometry(QRect(135, 45, 271, 46))
        font = QFont("Helvetica")
        font.setBold(True)
        self.header_label.setFont(font)
        self.header_label.setStyleSheet("background-color: transparent; color: #666666; font-size: 40px;")

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.retranslate_ui()
        QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslate_ui(self):
        self.MainWindow.setWindowTitle(QCoreApplication.translate("self.MainWindow", "self.MainWindow", None))
        self.header_label.setText(QCoreApplication.translate("self.MainWindow", "CATEGORIES", None))

    def update_category_field(self, categories):
        # Clear the existing layout
        if self.scroll_area_widget_contents.layout() is not None:
            self.clear_layout(self.scroll_area_widget_contents.layout())
            QWidget().setLayout(self.scroll_area_widget_contents.layout())

        # Create a new layout for the scroll area
        layout = QVBoxLayout(self.scroll_area_widget_contents)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        font = QFont("Helvetica", 30)
        self.categories_buttons_list = {}
        self.trashcan_buttons_list = {}

        for index, category in enumerate(categories):
            category_button = QPushButton(self.scroll_area_widget_contents)
            category_button.setFont(font)
            category_button.setStyleSheet("background-color: #666666; border-radius: 5px; color: #cadbdd")
            category_button.setFixedHeight(50)
            category_button.clicked.connect(partial(self.go_to_dictionary_screen, category))
            category_button.setText(QCoreApplication.translate("self.MainWindow", category.name.upper(), None))
            self.categories_buttons_list[category.name] = category_button

            trashcan_button = QPushButton(self.scroll_area_widget_contents)
            trashcan_button.setStyleSheet("border-radius: 0px")
            icon = QIcon()
            icon.addFile("./assets/trashcan.png", QSize())
            trashcan_button.setIcon(icon)
            trashcan_button.setIconSize(QSize(48, 48))
            trashcan_button.clicked.connect(partial(self.delete_category, category))
            self.trashcan_buttons_list[category.name] = trashcan_button, index

            h_layout = QHBoxLayout()
            h_layout.addWidget(category_button)
            h_layout.addWidget(trashcan_button)

            h_layout.setStretch(0, 10)
            h_layout.setStretch(1, 1)

            layout.addLayout(h_layout)

        self.scroll_area_widget_contents.setLayout(layout)

    def add_new_category(self, category_name: str):
        category = TermGroup(category_name, self.user.id)
        TermGroupsStore(self.connection).create(category)
        self.connection.commit()
        self.update_category_field(TermGroupsStore(self.connection).list())

    def delete_category(self, category: TermGroup):
        print(f"Deleting category {category.name}")
        if category.id is not None:
            TermGroupsStore(self.connection).delete(category.id)

        self.connection.commit()
        self.update_category_field(TermGroupsStore(self.connection).list())

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def add_new_category_screen(self):
        self.add_category_plus_button.close()
        self.scroll_area.close()

        self.input_category_text_label = QLabel(self.centralwidget)
        self.input_category_text_label.setGeometry(QRect(115, 300, 256, 31))
        self.input_category_text_label.setStyleSheet("color: #666666; font-size: 30px")
        self.input_category_text_label.show()
        font = QFont("Helvetica", 30)
        font.setBold(True)
        self.input_category_text_label.setFont(font)

        self.category_text = QLineEdit(self.centralwidget)
        self.category_text.setGeometry(QRect(375, 300, 241, 31))
        self.category_text.setStyleSheet("color: #666666; font-size: 20px")
        self.category_text.show()

        subfont = QFont("Helvetica", 25)
        subfont.setBold(True)
        self.add_category_button = QPushButton(self.centralwidget)
        self.add_category_button.setGeometry(QRect(570, 450, 196, 61))
        self.add_category_button.clicked.connect(self.redirect_back)
        self.add_category_button.setFont(subfont)
        self.add_category_button.setStyleSheet("color: #cadbdd; background-color: #666666; border-radius: 5px")

        self.retranslate_ui_for_new_category_screen()
        QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslate_ui_for_new_category_screen(self):
        self.input_category_text_label.setText(QCoreApplication.translate("self.MainWindow", "Category:", None))
        self.category_text.setPlaceholderText(QCoreApplication.translate("self.MainWindow", "Enter category name", None))
        self.add_category_button.setText(QCoreApplication.translate("self.MainWindow", "ADD", None))
        self.add_category_button.show()

    def redirect_back(self):
        self.add_new_category(self.category_text.text())
        self.add_category_button.close()
        self.input_category_text_label.close()
        self.category_text.close()

        self.add_category_plus_button.show()
        self.scroll_area.show()
        self.update_category_field(TermGroupsStore(self.connection).list())
        self.retranslate_ui()

    def go_to_dictionary_screen(self, category: TermGroup):
        print(f"Going to dictionary screen {category.name}")
        dictionary_screen = DictionaryScreen()
        dictionary_screen.setup_ui(self.MainWindow, category)
