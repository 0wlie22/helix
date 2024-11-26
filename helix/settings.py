from PyQt5.QtGui import QFont
import sqlite3

CONNECTION = sqlite3.connect("database.db")

# Text
FONT_FAMILY = "Helvetica"
FONT_SIZE_TITLE = 70
MINI_TITLE_SIZE = 40
SUBFONT_SIZE = 20
TEXT_SIZE = 15

# Windows sizes
SCREEN_SIZE = (800, 600)
SETTINGS_SCREEN_SIZE = (800, 400)

font = QFont(FONT_FAMILY, 30)
font.setBold(True)

subfont = QFont(FONT_FAMILY, 25)
subfont.setBold(True)
