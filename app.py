# app.py

import sys
from PyQt5.QtWidgets import QApplication
from main.main_view import MainView


def main():
    app = QApplication(sys.argv)

    main_window = MainView()
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
