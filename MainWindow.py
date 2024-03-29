from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout
import os

from med_to_excel import MedToExcel
from variability import Variability
from FAP_analysis import FAP_analysis


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initializes the class instance.
        """
        super().__init__()
        self.check_files()
        self.set_initial()
        self.layout.addWidget(self.med_to_excel)

        self.setWindowTitle("LabAEC UnB")

    def set_initial(self):
        """
        Initializes the initial state of the application window, setting up the layout and connecting button signals to their respective slots.
        """
        self.window = QWidget()
        self.layout = QVBoxLayout(self.window)
        self.menu = QWidget()
        self.menu_layout = QHBoxLayout(self.menu)
        self.med_to_excel = MedToExcel()
        self.variability = Variability()
        self.fap_analysis = FAP_analysis()

        self.button_med_to_excel = QPushButton("Med to Excel")
        self.button_var_calc = QPushButton("Variability Calc")
        self.button_fap_analysis = QPushButton("FAP analysis")

        self.menu_layout.addWidget(self.button_med_to_excel)
        self.menu_layout.addWidget(self.button_var_calc)
        self.menu_layout.addWidget(self.button_fap_analysis)
        self.layout.addWidget(self.menu)

        self.button_med_to_excel.clicked.connect(self.set_med_to_excel)
        self.button_var_calc.clicked.connect(self.set_variability)
        self.button_fap_analysis.clicked.connect(self.set_fap_analysis)

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
    
    def set_fap_analysis(self):
        self.set_initial()
        self.layout.addWidget(self.fap_analysis)

    def check_files(self):
        dir_exists = os.path.exists("./src")
        consequences_exists = os.path.exists("./src/consequences.txt")
        latency_exists = os.path.exists("./src/latency.txt")
        duration_exists = os.path.exists("./src/duration.txt")
        trial_duration = os.path.exists("./src/trial_duration.txt")

        if dir_exists and consequences_exists and latency_exists and duration_exists and trial_duration:
            return "Archives Checked"
        else:
            if not dir_exists:
                os.mkdir("./src")
            with open("./src/consequences.txt", "w") as f:
                f.write("E-FULL")
            with open("./src/latency.txt", "w") as f:
                f.write("A-FULL")
            with open("./src/duration.txt", "w") as f:
                f.write("D-FULL")
            with open("./src/trial_duration.txt", "w") as f:
                f.write("U-FULL")
            return "Archives Created"