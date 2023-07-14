from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout
from med_to_excel import MedToExcel
from variability import Variability


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_initial()
        self.layout.addWidget(self.med_to_excel)

        self.setWindowTitle("LabAEC UnB")

    def set_initial(self):
        self.window = QWidget()
        self.layout = QVBoxLayout(self.window)
        self.menu = QWidget()
        self.menu_layout = QHBoxLayout(self.menu)
        self.med_to_excel = MedToExcel()
        self.variability = Variability()

        self.button_med_to_excel = QPushButton("Med to Excel")
        self.button_var_calc = QPushButton("Variability Calc")

        self.menu_layout.addWidget(self.button_med_to_excel)
        self.menu_layout.addWidget(self.button_var_calc)
        self.layout.addWidget(self.menu)

        self.button_med_to_excel.clicked.connect(self.set_med_to_excel)
        self.button_var_calc.clicked.connect(self.set_variability)

        self.layout.addWidget(self.menu)
        self.setCentralWidget(self.window)

    def set_med_to_excel(self):
        # widgets = self.layout.findChildren(QWidget)
        # for widget in widgets:
        #     widget.deleteLater()
        # self.layout.addWidget(self.menu)
        self.set_initial()
        self.layout.addWidget(self.med_to_excel)
    
    def set_variability(self):
        # widgets = self.layout.findChildren(QWidget)
        # for widget in widgets:
        #     widget.deleteLater()
        # self.layout.addWidget(self.menu)
        self.set_initial()
        self.layout.addWidget(self.variability)