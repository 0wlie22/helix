# pyright: basic

import argparse
import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QComboBox, QGridLayout, QLabel, QPushButton, QWidget
from settings import FONT, MINI_TITLE_SIZE, SCREEN_SIZE, SETTINGS_SCREEN_SIZE, SUBFONT, SUBFONT_SIZE


class Screen(QWidget):
    BLOCK_WIDTH = SETTINGS_SCREEN_SIZE[0] // 10
    BLOCK_HEIGHT = SETTINGS_SCREEN_SIZE[1] // 12

    def __init__(self) -> None:
        super().__init__()

        parser = argparse.ArgumentParser()
        parser.add_argument("--log", type=str, default="INFO")
        args = parser.parse_args()
        log_level = getattr(logging, args.log.upper())
        logging.basicConfig(
            format="%(asctime)s: %(levelname)s - %(message)s",
            level=log_level,
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logging.info("Logging level set to %s", args.log)

        self.init_ui()

    def init_ui(self) -> None:
        logging.info("Initializing UI")
        self.setWindowTitle("HELIX")
        self.start_screen()

    def start_screen(self) -> None:
        logging.info("Start screen")
        self.setStyleSheet(
            "background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.4, \
            fx: 0.5, fy: 0.8, stop: 0 #CADBDD, stop: 1 #49C2CE);"
        )

        self.layout = QGridLayout()
        self.resize(*SCREEN_SIZE)

        self.logo = QPixmap("./assets/helix-logo.png")
        self.label = QLabel(self)

        self.label.setPixmap(self.logo)
        self.label.resize(self.logo.width(), self.logo.height())
        self.label.setStyleSheet("background: transparent;")

        self.layout.addWidget(self.label, 0, 0, 1, 1, Qt.AlignCenter)

        # Buttons
        self.log_in_button = QPushButton("Log in", self)
        self.log_in_button.setFixedSize(self.BLOCK_WIDTH * 3, self.BLOCK_HEIGHT * 2)
        self.log_in_button.setStyleSheet(
            "border-radius : 10; \
            color: white; \
            background-color: #666666"
        )
        self.log_in_button.setFont(QFont(SUBFONT, SUBFONT_SIZE))
        self.log_in_button.clicked.connect(self.log_in)

        self.layout.addWidget(self.log_in_button, 1, 0, 1, 1, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)

    def clear_layout(self) -> None:
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

    def log_in(self) -> None:
        self.clear_layout()

        self.setStyleSheet("background-color: #CADBDD")
        self.layout.setSpacing(0)

        # Light blue header
        self.layout.setContentsMargins(0, 0, 0, 0)
        header = QPixmap("./assets/header.png")
        header = header.scaledToWidth(SCREEN_SIZE[0])
        self.header_label = QLabel(self)
        self.header_label.setPixmap(header)

        # Logo in header
        logo = QPixmap("./assets/helix-logo.png")
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(logo)
        self.logo_label.setStyleSheet("background-color: transparent")

        self.choose_user_label = QLabel("\tChoose user:")
        self.choose_user_label.setStyleSheet(
            "color: #666666; font-size: \
            30px; font-weight: bold"
        )

        self.drop_down = QComboBox()
        self.fill_drop_down()
        self.drop_down.setStyleSheet(
            "background-color: transparent; \
            font-size: 30px; color: #666666; \
            min-width: 100px"
        )

        plus = QPixmap("./assets/plus.svg")
        scaled_plus = plus.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Adjust the width and height as needed
        self.plus_label = QLabel(self)
        self.plus_label.setPixmap(scaled_plus)
        # self.plus_label = ClickableLabel(self)
        self.plus_label.setPixmap(scaled_plus)
        # self.plus_label.set_color("#666666")
        self.plus_label.setContentsMargins(20, 0, 0, 0)  # Add left margin

        # self.plus_label.clicked.connect(self.on_plus_label_clicked)  # Connect the click event to a function

        self.blank = QLabel(" ")

        # Submit button
        self.submit = QPushButton("SUBMIT")
        self.submit.setFixedSize(self.BLOCK_WIDTH * 3, self.BLOCK_HEIGHT * 2)
        self.submit.setStyleSheet(
            "border-radius : 10; color: white; \
            background-color: #666666; font-size: 30px"
        )

        self.submit.setFont(QFont(SUBFONT, SUBFONT_SIZE))
        self.submit.clicked.connect(self.start_page)

        self.layout.addWidget(self.header_label, 0, 0, 2, 4)
        self.layout.addWidget(self.logo_label, 0, 0, 2, 4, Qt.AlignCenter)
        self.layout.addWidget(self.blank, 3, 0, 3, 1)
        self.layout.addWidget(self.choose_user_label, 4, 0, 1, 1)
        self.layout.addWidget(self.drop_down, 4, 2, 1, 1)
        self.layout.addWidget(self.plus_label, 4, 3, 1, 1)
        self.layout.addWidget(self.blank, 5, 0, 1, 3)
        self.layout.addWidget(self.submit, 5, 2, 1, 3, Qt.AlignCenter)
        self.setLayout(self.layout)

    def fill_drop_down(self) -> None:
        for i in range(10):
            self.drop_down.addItem(f"User {i}")

    def start_page(self) -> None:
        self.clear_layout()
        self.layout.addWidget(self.header_label, 0, 0, 2, 4)
        self.layout.addWidget(self.logo_label, 0, 0, 2, 4, Qt.AlignCenter)
        self.setLayout(self.layout)

    def on_plus_label_clicked(self) -> None:
        self.drop_down.addItem("User 1")
