from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QFileDialog
import os


class Selector(QWidget):
    def __init__(self, archive:str):
        super().__init__()
        self.file_path = ''
        self.button_select = QPushButton(f"Select {archive}")
        self.label_file_path = QLabel(f"File: {self.file_path}")
        self.label_file_path.setFixedSize(400, 30)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.button_select)
        self.layout.addWidget(self.label_file_path)

        self.button_select.clicked.connect(self.get_file_path)

    def get_file_path(self):
        self.file_path = self.open_dialog()
        self.label_file_path.setText(f"File: {self.file_path}")

    def open_dialog(self):
        window = QWidget()

        file_path, _ = QFileDialog.getOpenFileName(window, 'Open file', './')

        window.show()
        return file_path