import logging
from functools import partial

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
from quiz_screen import QuizScreen
from store import Store, Term, TermGroup, User


class DictionaryScreen(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def setup_ui(self, MainWindow, store: Store, category: TermGroup, user: User, welcome_screen):
        self.category = category
        self.store = store
        self.user = user
        self.welcome_screen = welcome_screen
        self.MainWindow = MainWindow

        MainWindow.setEnabled(True)
        MainWindow.setMinimumSize(QSize(800, 600))
        MainWindow.setMaximumSize(QSize(800, 600))
        MainWindow.setFont(QFont("Helvetica", 12))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: #CADBDD")

        # Header setup
        self.header = QLabel(self.centralwidget)
        self.header.setGeometry(QRect(1, -3, 813, 136))
        self.header.setPixmap(QPixmap("./assets/header.png"))
        self.logo = QLabel(self.centralwidget)
        self.logo.setGeometry(QRect(15, 15, 91, 91))
        self.logo.setPixmap(QPixmap("./assets/helix-log-small.png"))
        self.logo.setScaledContents(True)
        self.logo.setStyleSheet("background-color: transparent;")

        # Header Label
        self.header_label = QLabel(self.centralwidget)
        self.header_label.setGeometry(QRect(135, 45, 271, 46))
        self.header_label.setFont(QFont("Helvetica", 40, QFont.Bold))  # type: ignore
        self.header_label.setStyleSheet("background-color: transparent; color: #666666;")
        self.header_label.setText("DICTIONARY")

        # Scroll Area for Terms
        self.scroll_menu = QScrollArea(self.centralwidget)
        self.scroll_menu.setGeometry(QRect(30, 200, 736, 300))
        self.scroll_menu.setWidgetResizable(True)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_menu.setWidget(self.scroll_area_widget_contents)
        self.scroll_menu.setStyleSheet("border-color: transparent")

        self.terms_buttons_list = {}
        self.trashcan_buttons_list = {}
        self.load_terms()

        # Add New Term Button
        image = QPixmap("./assets/plus.png")
        self.add_new_term_button = QPushButton(QIcon(image), "", self.centralwidget)
        self.add_new_term_button.setGeometry(QRect(720, 150, 46, 46))
        self.add_new_term_button.setStyleSheet("border-radius: 0px")
        self.add_new_term_button.setIconSize(QSize(48, 48))
        self.add_new_term_button.clicked.connect(lambda: self.add_new_term_screen())

        self.start_quiz_button = QPushButton("START QUIZ", self.centralwidget)
        self.start_quiz_button.setGeometry(QRect(30, 520, 736, 61))
        self.start_quiz_button.setFont(QFont("Helvetica", 25, QFont.Bold))  # type: ignore
        self.start_quiz_button.setStyleSheet(
            "background-color: transparent; color: #666666; border-radius: 5px; border-style: solid; border-width: 1px;"
        )
        self.start_quiz_button.clicked.connect(lambda: self.go_to_quiz_screen())

        MainWindow.setCentralWidget(self.centralwidget)

    def load_terms(self):
        """Loads terms for the current category and updates the scroll area."""
        self.logger.debug("Loading terms")
        # Clear existing layout
        if self.scroll_area_widget_contents.layout() is not None:
            self.clear_layout(self.scroll_area_widget_contents.layout())
            QWidget().setLayout(self.scroll_area_widget_contents.layout())

        # Create new layout
        layout = QVBoxLayout(self.scroll_area_widget_contents)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        if self.category.id:
            terms = self.store.terms.get_by_group_id(self.category.id)
            if terms:
                for term in terms:
                    term_button = QPushButton(term.term, self.scroll_area_widget_contents)
                    term_button.setFont(QFont("Helvetica", 20))
                    term_button.setStyleSheet("background-color: #666666; color: #CADBDD; border-radius: 5px;")
                    term_button.setFixedHeight(50)
                    term_button.clicked.connect(partial(self.edit_term_screen, term))

                    trashcan_button = QPushButton(self.scroll_area_widget_contents)
                    trashcan_button.setStyleSheet("border-radius: 0px")
                    icon = QIcon("./assets/trashcan.png")
                    trashcan_button.setIcon(icon)
                    trashcan_button.setIconSize(QSize(48, 48))
                    trashcan_button.clicked.connect(partial(self.delete_term, term))

                    h_layout = QHBoxLayout()
                    h_layout.addWidget(term_button)
                    h_layout.addWidget(trashcan_button)
                    h_layout.setStretch(0, 10)
                    h_layout.setStretch(1, 1)
                    layout.addLayout(h_layout)
            else:
                self.placeholder = QLabel("No terms found, press '+' to add a new one", self.scroll_area_widget_contents)
                self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.placeholder.setStyleSheet("color: #666666;")
                self.placeholder.setFont(QFont("Helvetica", 20))
                self.placeholder.setGeometry(QRect(0, 0, 736, 300))

        self.scroll_area_widget_contents.setLayout(layout)

    def add_new_term_screen(self):
        """Shows input fields for adding a new term."""
        self.logger.debug("Adding new term screen")

        self.placeholder.close()
        self.add_new_term_button.close()
        self.scroll_menu.close()

        self.word_label = QLabel("Word:", self.centralwidget)
        self.word_label.setGeometry(QRect(115, 250, 100, 30))
        self.word_label.setFont(QFont("Helvetica", 20))
        self.word_label.setStyleSheet("color: #666666;")

        self.definition_label = QLabel("Definition:", self.centralwidget)
        self.definition_label.setGeometry(QRect(115, 300, 150, 30))
        self.definition_label.setFont(QFont("Helvetica", 20))
        self.definition_label.setStyleSheet("color: #666666;")

        self.word_input = QLineEdit(self.centralwidget)
        self.word_input.setGeometry(QRect(300, 250, 400, 30))
        self.word_input.setStyleSheet("font-size: 18px; color: #666666")
        self.word_input.setPlaceholderText("Enter the word")

        self.definition_input = QLineEdit(self.centralwidget)
        self.definition_input.setGeometry(QRect(300, 300, 400, 30))
        self.definition_input.setStyleSheet("font-size: 18px; color: #666666")
        self.definition_input.setPlaceholderText("Enter the definition")

        self.save_button = QPushButton("ADD", self.centralwidget)
        self.save_button.setGeometry(QRect(600, 400, 100, 40))
        self.save_button.setStyleSheet("background-color: #666666; color: #CADBDD; border-radius: 5px;")
        self.save_button.clicked.connect(self.add_term)

        self.word_label.show()
        self.definition_label.show()
        self.word_input.show()
        self.definition_input.show()
        self.save_button.show()

    def add_term(self):
        """Adds a new term to the database and updates the UI."""
        word = self.word_input.text()
        definition = self.definition_input.text()
        if word and definition:
            new_term = Term(word, definition, self.category.id)
            self.store.terms.create(new_term)

        self.word_label.close()
        self.definition_label.close()
        self.word_input.close()
        self.definition_input.close()
        self.save_button.close()

        self.add_new_term_button.show()
        self.scroll_menu.show()
        self.load_terms()

    def delete_term(self, term: Term):
        """Deletes a term from the database."""
        self.logger.debug(f"Deleting term: {term.term}")

        if term.id is not None:
            self.store.terms.delete(term.id)
        self.load_terms()

    def clear_layout(self, layout):
        """Clears all widgets from a layout."""
        self.logger.debug("Clearing the layout")
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def edit_term_screen(self, term: Term):
        """Loads the term in the input fields for editing."""
        self.logger.debug(f"Editing term: {term.term}")

        self.add_new_term_button.close()
        self.scroll_menu.close()

        self.word_label = QLabel("Word:", self.centralwidget)
        self.word_label.setGeometry(QRect(115, 250, 100, 30))
        self.word_label.setFont(QFont("Helvetica", 20))
        self.word_label.setStyleSheet("color: #666666;")

        self.definition_label = QLabel("Definition:", self.centralwidget)
        self.definition_label.setGeometry(QRect(115, 300, 150, 30))
        self.definition_label.setFont(QFont("Helvetica", 20))
        self.definition_label.setStyleSheet("color: #666666;")

        self.word_input = QLineEdit(self.centralwidget)
        self.word_input.setGeometry(QRect(300, 250, 400, 30))
        self.word_input.setStyleSheet("font-size: 18px; color: #666666;")
        self.word_input.setText(term.term)

        self.definition_input = QLineEdit(self.centralwidget)
        self.definition_input.setGeometry(QRect(300, 300, 400, 30))
        self.definition_input.setStyleSheet("font-size: 18px; color: #666666;")
        self.definition_input.setText(term.definition)

        self.save_button = QPushButton("SAVE", self.centralwidget)
        self.save_button.setGeometry(QRect(600, 400, 100, 40))
        self.save_button.setStyleSheet("background-color: #666666; color: #CADBDD; border-radius: 5px;")
        self.save_button.clicked.connect(partial(self.update_term, term))

        self.word_label.show()
        self.definition_label.show()
        self.word_input.show()
        self.definition_input.show()
        self.save_button.show()

    def update_term(self, term: Term):
        """Updates the term in the database and reloads the UI."""
        word = self.word_input.text()
        definition = self.definition_input.text()
        if word and definition:
            term.term = word
            term.definition = definition
            self.store.terms.update(term)

        self.word_label.close()
        self.definition_label.close()
        self.word_input.close()
        self.definition_input.close()
        self.save_button.close()

        self.add_new_term_button.show()
        self.scroll_menu.show()
        self.load_terms()

    def go_to_quiz_screen(self):
        """Navigates to the quiz screen."""
        self.logger.debug("Going to the quiz screen")

        self.QuizScreen = QuizScreen()
        if self.category.id:
            self.QuizScreen.start_quiz(self.MainWindow, self.store, self.category.id, self.user, self.welcome_screen)
