from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout
from med_to_excel import MedToExcel
from variability import Variability
from FAP_analysis import FAP_analysis


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initializes the class instance.
        """
        super().__init__()
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