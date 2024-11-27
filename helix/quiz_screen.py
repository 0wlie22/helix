import logging

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
from quiz import Quiz
from store import Store, Term, User


class QuizScreen:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def start_quiz(self, MainWindow, store: Store, category_id: int, user: User, welcome_screen):
        """Initialize the quiz screen and start the quiz."""
        self.logger.debug("Starting the quiz")

        self.store = store
        self.user = user
        self.welcome_screen = welcome_screen
        self.MainWindow = MainWindow

        if self.user.id is not None:
            self.quiz = Quiz(self.store, self.user.id)

        self.terms = self.store.terms.get_by_group_id(category_id)
        self.current_term_index = 0
        if self.terms:
            self.setup_ui(self.terms[self.current_term_index])

    def setup_ui(self, term: Term):
        """Set up the quiz user interface."""
        self.logger.debug("Setting up the quiz screen UI")

        # Configure the main window
        self.MainWindow.setEnabled(True)
        self.MainWindow.setSizePolicy(QSizePolicy())
        self.MainWindow.setMinimumSize(800, 600)
        self.MainWindow.setMaximumSize(600, 400)
        self.MainWindow.setFont(QFont("", 30))
        self.MainWindow.setIconSize(QSize(48, 48))

        # Set up the central widget and styles
        self.centralwidget = QWidget(self.MainWindow)
        self.centralwidget.setStyleSheet("background-color: #CADBDD")

        # Header and logo
        self.setup_header()

        # Term input and definition display
        self.setup_definition_display()
        self.setup_input_section()

        # Message label for feedback
        self.message_label = self.create_label(
            120, 440, 601, 30, "Helvetica", 16, "color: #666666; text-align: center;"
        )
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.retranslate_ui(term)

        # Connect events
        self.submit_button.clicked.connect(lambda: self.on_submit())
        QMetaObject.connectSlotsByName(self.MainWindow)

    def setup_header(self):
        """Set up the header section."""
        self.header = QLabel(self.centralwidget)
        self.header.setGeometry(1, -3, 813, 136)
        self.header.setFont(QFont("Helvetica", 25))
        self.header.setPixmap(QPixmap("./assets/header.png"))

        self.logo = QLabel(self.centralwidget)
        self.logo.setGeometry(15, 15, 91, 91)
        self.logo.setStyleSheet("background-color: transparent;")
        self.logo.setPixmap(QPixmap("./assets/helix-log-small.png"))
        self.logo.setScaledContents(True)

        self.header_label = self.create_label(
            135, 45, 271, 46, "Helvetica", 40, "background-color: transparent; color: #666666;", bold=True
        )

    def setup_definition_display(self):
        """Set up the definition display section."""
        self.definition_label = self.create_label(
            120,
            300,
            601,
            61,
            "Helvetica",
            20,
            "border-style: solid; border-radius: 5px; color: #666666; border-color: #666666; text-indent: 5px",
            bold=True,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        self.scroll_area = QScrollArea(self.centralwidget)
        self.scroll_area.setGeometry(120, 300, 601, 61)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("color: #666666; border-radius: 5px; border-style: solid; border-color: #666666")
        self.scroll_area.setWidget(self.definition_label)

    def setup_input_section(self):
        """Set up the term input and submit button."""
        self.term_input = QLineEdit(self.centralwidget)
        self.term_input.setGeometry(120, 210, 601, 61)
        self.term_input.setFont(QFont("Helvetica", 25, italic=True))
        self.term_input.setStyleSheet("color: #666666;")

        self.submit_button = QPushButton(self.centralwidget)
        self.submit_button.setGeometry(120, 375, 601, 46)
        self.submit_button.setFont(QFont("Helvetica", 20))
        self.submit_button.setStyleSheet("color: #cadbdd; background-color: #666666; border-radius: 5px")

    def create_label(
        self, x, y, width, height, font_family, font_size, style, bold=False, alignment=Qt.AlignmentFlag.AlignLeft
    ):
        """Helper function to create a QLabel."""
        label = QLabel(self.centralwidget)
        label.setGeometry(x, y, width, height)
        font = QFont(font_family, font_size)
        font.setBold(bold)
        label.setFont(font)
        label.setStyleSheet(style)
        label.setAlignment(alignment)
        label.show()
        return label

    def retranslate_ui(self, term: Term):
        """Update the UI with the term's information."""
        self.logger.debug("Retranslating the quiz screen UI")

        self.definition_label.setText(QCoreApplication.translate("MainWindow", term.definition, None))
        self.header_label.setText(QCoreApplication.translate("MainWindow", "QUIZ", None))
        self.term_input.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Input the correct term of the definition", None)
        )
        self.submit_button.setText(QCoreApplication.translate("MainWindow", "SUBMIT", None))

    def on_submit(self):
        """Handle the submit action."""
        self.logger.debug("Submitting the answer")

        user_answer = self.term_input.text()
        correct = self.quiz.check_answer(user_answer, self.terms[self.current_term_index].term)
        self.logger.debug(f"User answer: {user_answer}, Correct answer: {self.terms[self.current_term_index].term}")

        if correct:
            self.message_label.setStyleSheet("color: green;")
            self.message_label.setText("Correct!")
        else:
            self.message_label.setStyleSheet("color: red;")
            self.message_label.setText(f"Incorrect. Correct answer: {self.terms[self.current_term_index].term}")

        self.logger.debug(self.message_label.text())
        self.quiz.update_mastery(self.terms[self.current_term_index], correct=correct)
        self.next_term()

    def next_term(self):
        """Move to the next term or show the final message."""
        self.logger.debug("Moving to the next term")

        if self.current_term_index < len(self.terms) - 1:
            self.current_term_index += 1
            self.retranslate_ui(self.terms[self.current_term_index])
            self.term_input.clear()
        else:
            self.logger.debug("Quiz finished")
            self.show_final_message(self.quiz.points, len(self.terms))

    def show_final_message(self, score, total):
        """Display the final score and provide navigation back to the main page."""
        # Hide quiz elements
        for widget in [
            self.term_input,
            self.definition_label,
            self.submit_button,
            self.message_label,
            self.scroll_area,
        ]:
            widget.close()

        # Show final score and message
        self.create_label(
            100, 200, 600, 50, "Helvetica", 18, "color: #666666", alignment=Qt.AlignmentFlag.AlignCenter
        ).setText("You answered all the questions!")
        self.create_label(
            100, 270, 600, 50, "Helvetica", 18, "color: #666666", bold=True, alignment=Qt.AlignmentFlag.AlignCenter
        ).setText(f"Score: {score}/{total}")

        self.to_main_page_button = QPushButton(self.centralwidget)
        self.to_main_page_button.setGeometry(300, 350, 200, 50)
        self.to_main_page_button.setFont(QFont("Helvetica", 16))
        self.to_main_page_button.setStyleSheet("background-color: #666666; color: #cadbdd; border-radius: 5px")
        self.to_main_page_button.setText("To Main Page")
        self.to_main_page_button.clicked.connect(self.go_to_main_page)
        self.to_main_page_button.show()

    def go_to_main_page(self):
        """Handle navigation back to the main page."""
        self.logger.debug("Going back to the main page")
        self.welcome_screen.setup_ui(self, self.store, self.user)
