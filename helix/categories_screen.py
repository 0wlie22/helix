from functools import partial

from dictionary_screen import DictionaryScreen
from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
from store import Store, TermGroup, User
import logging


class CategoriesScreen:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def setup_ui(self, screen, store: Store, user: User, welcome_screen):
        self.logger.debug("Setting up the categories screen UI")

        self.store = store
        self.user = user
        self.welcome_screen = welcome_screen
        self.MainWindow = screen.MainWindow

        # Setting up the Main Window
        self.MainWindow.setEnabled(True)
        sizePolicy = QSizePolicy()
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainWindow.sizePolicy().hasHeightForWidth())
        self.MainWindow.setSizePolicy(sizePolicy)
        self.MainWindow.setMinimumSize(QSize(800, 600))
        self.MainWindow.setMaximumSize(QSize(600, 400))
        self.MainWindow.setFont(QFont("Helvetica", 30))
        self.MainWindow.setIconSize(QSize(48, 48))

        # Configuring the central widget
        self.centralwidget = QWidget(self.MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("background-color: #CADBDD")

        # Header
        self.header = QLabel(self.centralwidget)
        self.header.setGeometry(QRect(1, -3, 813, 136))
        self.header.setFont(QFont("Helvetica", 25))
        self.header.setPixmap(QPixmap("./assets/header.png"))

        # Logo on the header
        self.logo = QLabel(self.centralwidget)
        self.logo.setObjectName("label_2")
        self.logo.setGeometry(QRect(15, 15, 91, 91))
        self.logo.setStyleSheet("background-color: transparent;")
        self.logo.setPixmap(QPixmap("./assets/helix-log-small.png"))
        self.logo.setScaledContents(True)

        # Category scroll area with category buttons
        self.scroll_area = QScrollArea(self.centralwidget)
        self.scroll_area.setGeometry(QRect(30, 200, 750, 300))
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded) #type: ignore
        self.scroll_area.setStyleSheet("border-radius: 0px")

        # Get categories and add a default one
        self.categories_buttons_list = {}
        self.trashcan_buttons_list = {}
        if self.user.id is not None:
            categories = self.store.term_groups.get_by_user_id(self.user.id)
            self.logger.debug(f"Categories: {categories}")
            if not categories:
                self.add_new_category("Default")
                categories = self.store.term_groups.get_by_user_id(self.user.id)
                self.logger.debug(f"Categories: {categories}")
            self.update_category_field(categories)

        # Add category plus button
        image = QPixmap("./assets/plus.png")
        self.add_category_plus_button = QPushButton(QIcon(image), "", self.centralwidget)
        self.add_category_plus_button.setGeometry(QRect(705, 150, 46, 46))
        self.add_category_plus_button.setStyleSheet("border-radius: 0px")
        self.add_category_plus_button.setIconSize(QSize(48, 48))
        self.add_category_plus_button.clicked.connect(self.add_new_category_screen)

        # Add header label
        self.header_label = QLabel(self.centralwidget)
        self.header_label.setGeometry(QRect(135, 45, 271, 46))
        self.header_label.setFont(QFont("Helvetica", 40, QFont.Bold)) #type: ignore
        self.header_label.setStyleSheet("background-color: transparent; color: #666666; font-size: 40px;")

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.retranslate_ui()
        QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslate_ui(self):
        self.logger.debug("Retranslating the categories screen UI")
        self.MainWindow.setWindowTitle(QCoreApplication.translate("self.MainWindow", "self.MainWindow", None))
        self.header_label.setText(QCoreApplication.translate("self.MainWindow", "CATEGORIES", None))

    def update_category_field(self, categories):
        self.logger.debug(f"Updating the category field with {categories}")

        if self.scroll_area_widget_contents.layout() is not None:
            self.clear_layout(self.scroll_area_widget_contents.layout())
            QWidget().setLayout(self.scroll_area_widget_contents.layout())

        layout = QVBoxLayout(self.scroll_area_widget_contents)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.categories_buttons_list = {}
        self.trashcan_buttons_list = {}

        for index, category in enumerate(categories):
            self.logger.debug(f"Adding category {category.name}")
            category_button = QPushButton(self.scroll_area_widget_contents)
            category_button.setFont(QFont("Helvetica", 30))
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
        self.logger.debug(f"Adding new category {category_name} for user {self.user.username}")

        category = TermGroup(name=category_name, user_id=self.user.id)
        self.store.term_groups.create(category)
        if self.user.id is not None:
            self.update_category_field(self.store.term_groups.get_by_user_id(self.user.id))

    def delete_category(self, category: TermGroup):
        self.logger.debug(f"Deleting category {category.name} for user {self.user.username}")

        if category.id is not None:
            self.logger.debug(f"Deleting category {category.name} with id {category.id}")
            self.store.term_groups.delete(category.id)
        if self.user.id is not None:
            self.logger.debug(f"Updating categories for user {self.user.username}")
            self.update_category_field(self.store.term_groups.get_by_user_id(self.user.id))

    def clear_layout(self, layout):
        self.logger.debug("Clearing the layout")
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def add_new_category_screen(self):
        self.logger.debug("Adding new category screen")

        self.add_category_plus_button.close()
        self.scroll_area.close()

        self.input_category_text_label = QLabel(self.centralwidget)
        self.input_category_text_label.setGeometry(QRect(115, 300, 256, 31))
        self.input_category_text_label.setStyleSheet("color: #666666; font-size: 30px")
        self.input_category_text_label.show()
        self.input_category_text_label.setFont(QFont("Helvetica", 30))

        self.category_text = QLineEdit(self.centralwidget)
        self.category_text.setGeometry(QRect(375, 300, 241, 31))
        self.category_text.setStyleSheet("color: #666666; font-size: 20px")
        self.category_text.show()

        self.add_category_button = QPushButton(self.centralwidget)
        self.add_category_button.setGeometry(QRect(570, 450, 196, 61))
        self.add_category_button.clicked.connect(self.redirect_back)
        self.add_category_button.setFont(QFont("Helvetica", 25))
        self.add_category_button.setStyleSheet("color: #cadbdd; background-color: #666666; border-radius: 5px")

        self.retranslate_ui_for_new_category_screen()
        QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslate_ui_for_new_category_screen(self):
        self.logger.debug("Retranslating the new category screen UI")

        self.input_category_text_label.setText(QCoreApplication.translate("self.MainWindow", "Category:", None))
        self.category_text.setPlaceholderText(QCoreApplication.translate("self.MainWindow", "Enter category name", None))
        self.add_category_button.setText(QCoreApplication.translate("self.MainWindow", "ADD", None))
        self.add_category_button.show()

    def redirect_back(self):
        self.logger.debug("Redirecting back to the categories screen")

        self.add_new_category(self.category_text.text())
        self.add_category_button.close()
        self.input_category_text_label.close()
        self.category_text.close()

        self.add_category_plus_button.show()
        self.scroll_area.show()
        if self.user.id is not None:
            self.update_category_field(self.store.term_groups.get_by_user_id(self.user.id))

        self.retranslate_ui()

    def go_to_dictionary_screen(self, category: TermGroup):
        self.logger.debug(f"Going to the dictionary screen with category {category.name}")

        dictionary_screen = DictionaryScreen()
        dictionary_screen.setup_ui(self.MainWindow, self.store, category, self.user, self.welcome_screen)
