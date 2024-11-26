import sqlite3
from functools import partial

from PySide6.QtCore import * #type: ignore
from PySide6.QtGui import * #type: ignore
from PySide6.QtWidgets import * #type: ignore
from store import TermsStore, Term, TermGroup

class DictionaryScreen(object):
    def setup_ui(self, MainWindow, category: TermGroup):
        self.category = category
        self.connection = sqlite3.connect("database.db")
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
        font = QFont("Helvetica", 40)
        font.setBold(True)
        self.header_label.setFont(font)
        self.header_label.setStyleSheet("background-color: transparent; color: #666666;")
        self.header_label.setText("DICTIONARY")

        # Scroll Area for Terms
        self.scroll_menu = QScrollArea(self.centralwidget)
        self.scroll_menu.setGeometry(QRect(30, 200, 736, 300))
        self.scroll_menu.setWidgetResizable(True)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_menu.setWidget(self.scroll_area_widget_contents)

        self.terms_buttons_list = {}
        self.trashcan_buttons_list = {}
        terms = TermsStore(self.connection).list()
        self.load_terms(terms)

        image = QPixmap("./assets/plus.png")
        self.add_new_term_plus_button = QPushButton(QIcon(image), "", self.centralwidget)
        self.add_new_term_plus_button.setGeometry(QRect(720, 150, 46, 46))
        self.add_new_term_plus_button.setStyleSheet("border-radius: 0px")
        self.add_new_term_plus_button.setIconSize(QSize(48, 48))
        self.add_new_term_plus_button.clicked.connect(lambda: self.add_new_term_screen())
        self.add_new_term_plus_button.show()

        self.start_quiz_button = QPushButton(self.centralwidget)
        self.start_quiz_button.setGeometry(QRect(636, 90, 136, 32))
        font = QFont("Helvetica", 20)
        font.setBold(True)
        self.start_quiz_button.setFont(font)
        self.start_quiz_button.setStyleSheet(u"border-radius: 5px; color: #666666; background-color:transparent")
        self.start_quiz_button.setText("START QUIZ")
        self.start_quiz_button.clicked.connect(lambda: self.start_quiz())

        MainWindow.setCentralWidget(self.centralwidget)

    def load_terms(self, terms: list[Term]):
        """Loads terms for the current category and updates the scroll area."""
        if self.scroll_area_widget_contents.layout() is not None:
            self.clear_layout(self.scroll_area_widget_contents.layout())
            QWidget().setLayout(self.scroll_area_widget_contents.layout())

        layout = QVBoxLayout(self.scroll_area_widget_contents)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        font = QFont("Helvetica", 20)

        terms = TermsStore(self.connection).list()

        if terms:
            for term in terms:
                term_button = QPushButton(term.term, self.scroll_area_widget_contents)
                term_button.setFont(font)
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
            placeholder_label = QLabel("No terms available. Add new terms using the '+' button.")
            placeholder_label.setFont(font)
            placeholder_label.setStyleSheet("color: #666666; text-align: center;")
            placeholder_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(placeholder_label)

        self.scroll_area_widget_contents.setLayout(layout)

    def add_new_term_screen(self):
        """Shows input fields for adding a new term."""
        self.add_new_term_plus_button.close()
        self.scroll_menu.close()

        self.term_word_label = QLabel("Word:", self.centralwidget)
        self.term_word_label.setGeometry(QRect(115, 250, 100, 30))
        self.term_word_label.setFont(QFont("Helvetica", 20))
        self.term_word_label.setStyleSheet("color: #666666;")
        self.term_word_label.show()

        self.definition_label = QLabel("Definition:", self.centralwidget)
        self.definition_label.setGeometry(QRect(115, 300, 150, 30))
        self.definition_label.setFont(QFont("Helvetica", 20))
        self.definition_label.setStyleSheet("color: #666666;")
        self.definition_label.show()

        self.term_word_input = QLineEdit(self.centralwidget)
        self.term_word_input.setGeometry(QRect(300, 250, 400, 30))
        self.term_word_input.setStyleSheet("font-size: 18px;")
        self.term_word_input.show()

        self.term_definition_input = QLineEdit(self.centralwidget)
        self.term_definition_input.setGeometry(QRect(300, 300, 400, 30))
        self.term_definition_input.setStyleSheet("font-size: 18px;")
        self.term_definition_input.show()

        self.add_new_term_button = QPushButton("ADD", self.centralwidget)
        self.add_new_term_button.setGeometry(QRect(600, 400, 100, 40))
        self.add_new_term_button.setStyleSheet("background-color: #666666; color: #CADBDD; border-radius: 5px;")
        self.add_new_term_button.clicked.connect(self.add_term)
        self.add_new_term_button.show()

        self.retranslate_ui_for_add_term()

    def add_term(self):
        """Adds a new term to the database and updates the UI."""
        word = self.term_word_input.text()
        definition = self.term_definition_input.text()
        if word and definition:
            print(f"Adding term: {word} - {definition}")
            new_term = Term(word, definition, 1)
            TermsStore(self.connection).create(new_term)
            self.connection.commit()

        terms = TermsStore(self.connection).list()

        self.term_word_label.close()
        self.definition_label.close()
        self.term_word_input.close()
        self.term_definition_input.close()
        self.add_new_term_button.close()

        self.scroll_menu.show()
        self.add_new_term_plus_button.show()
        self.load_terms(terms)

    def delete_term(self, term: Term):
        """Deletes a term from the database."""
        if term.id is not None:
            TermsStore(self.connection).delete(term.id)
            self.connection.commit()

        terms = TermsStore(self.connection).list()
        self.load_terms(terms)


    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def edit_term_screen(self, term: Term):
        """Loads the term in the input fields for editing."""
        print(f"Editing term: {term.term}")

    def retranslate_ui_for_add_term(self):
        """Sets the text for the add term screen."""
        self.term_word_label.setText("Word:")
        self.definition_label.setText("Definition:")
        self.add_new_term_button.setText("ADD")

        self.term_word_label.show()
        self.definition_label.show()
        self.add_new_term_button.show()

    def start_quiz(self):
        print("Starting quiz")
