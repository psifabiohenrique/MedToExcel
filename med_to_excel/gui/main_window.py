from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFrame,
    QHBoxLayout,
)
import os

from med_to_excel.gui.analysis.variability import Variability
from med_to_excel.gui.analysis.fap_analysis import FAP_analysis
from med_to_excel.gui.analysis.fap_analysis_mean import FAP_analysis_mean
from med_to_excel.core.med_to_excel import MedToExcel


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
        self.fap_analysis_mean = FAP_analysis_mean()

        self.button_med_to_excel = QPushButton("Med to Excel")
        self.button_var_calc = QPushButton("Variability Calc")
        self.button_fap_analysis = QPushButton("FAP analysis")
        self.button_fap_analysis_mean = QPushButton("FAP analysis mean")

        self.menu_layout.addWidget(self.button_med_to_excel)
        self.menu_layout.addWidget(self.button_var_calc)
        self.menu_layout.addWidget(self.button_fap_analysis)
        self.menu_layout.addWidget(self.button_fap_analysis_mean)
        self.layout.addWidget(self.menu)

        self.button_med_to_excel.clicked.connect(self.set_med_to_excel)
        self.button_var_calc.clicked.connect(self.set_variability)
        self.button_fap_analysis.clicked.connect(self.set_fap_analysis)
        self.button_fap_analysis_mean.clicked.connect(self.set_fap_analysis_mean)

        self.layout.addWidget(self.menu)
        self.setCentralWidget(self.window)

    def set_med_to_excel(self):
        self.set_initial()
        self.layout.addWidget(self.med_to_excel)
    
    def set_variability(self):
        self.set_initial()
        self.layout.addWidget(self.variability)
    
    def set_fap_analysis(self):
        self.set_initial()
        self.layout.addWidget(self.fap_analysis)
    
    def set_fap_analysis_mean(self):
        self.set_initial()
        self.layout.addWidget(self.fap_analysis_mean)

    def check_files(self):
        dir_exists = os.path.exists("./src")
        dir_sheets_exists = os.path.exists("./planilhas")
        consequences_exists = os.path.exists("./src/consequences.txt")
        latency_exists = os.path.exists("./src/latency.txt")
        duration_exists = os.path.exists("./src/duration.txt")
        trial_duration = os.path.exists("./src/trial_duration.txt")

        if dir_exists and dir_sheets_exists and consequences_exists and latency_exists and duration_exists and trial_duration:
            return "Archives Checked"
        else:
            if not dir_exists:
                os.mkdir("./src")
            if not dir_sheets_exists:
                os.mkdir("./planilhas")
            with open("./src/consequences.txt", "w") as f:
                f.write("E-FULL")
            with open("./src/latency.txt", "w") as f:
                f.write("A-FULL")
            with open("./src/duration.txt", "w") as f:
                f.write("D-FULL")
            with open("./src/trial_duration.txt", "w") as f:
                f.write("U-FULL")
            return "Archives Created"