from PySide6.QtGui import Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QGridLayout, QCheckBox, QHBoxLayout

from med_to_excel.gui.widgets.selector import Selector
from med_to_excel.core.utils.copy import calc

class MedToExcel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.data_line = False
        self.comma = False


        self.layout = QGridLayout(self)

        self.model_selector = Selector("Model")
        self.mpc_selector = Selector(".MPC")

        self.layout.addWidget(self.model_selector, 1, 0)
        self.layout.addWidget(self.mpc_selector, 2, 0)

        self.check_data_line = QCheckBox("Receive data on the same line?")
        self.check_data_line.stateChanged.connect(self.get_data_line)
        self.button_copy_data = QPushButton("Copy data")
        self.button_copy_data.clicked.connect(self.get_copy_data)
        self.check_comma = QCheckBox("Use Comma?")
        self.check_comma.stateChanged.connect(self.get_comma)


        self.layout.addWidget(self.check_data_line, 1, 1)
        self.layout.addWidget(self.button_copy_data, 3, 0)
        self.layout.addWidget(self.check_comma, 2, 1)


        # self.button.clicked.connect(self.button_clicked)

    def get_copy_data(self):
        model_file = open(self.model_selector.file_path)
        mpc_file = open(self.mpc_selector.file_path)
        calc(mpc_file, model_file, self.check_data_line.isChecked(), self.check_comma.isChecked())
    
    def get_data_line(self, state):
        if state == Qt.CheckState.Checked:
            self.data_line = True
        else:
            self.data_line = False

    def get_comma(self, state):
        if state == Qt.CheckState.Checked:
            self.comma = True
        else:
            self.comma = False