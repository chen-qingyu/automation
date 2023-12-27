# FileName: autogit-gui.py
# Brief: GUI for autogit.
# Author: 青羽 (chen_qingyu@qq.com, https://chen-qingyu.github.io/)
# CreateDate: 2023.12.27
# Copyright (C) 2022 - 2023

import sys


from PySide6.QtWidgets import QApplication, QWidget


def main():
    app = QApplication(sys.argv)

    _ = Widget()

    sys.exit(app.exec())


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AutoGit")
        self.show()


if __name__ == '__main__':
    main()
