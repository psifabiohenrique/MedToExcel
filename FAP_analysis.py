from PySide6.QtWidgets import QPushButton, QWidget, QGridLayout, QLabel, QLineEdit, QCheckBox, QVBoxLayout

from Selector import Selector
from src.Copy import calc_row
from src.Percentage_correct_sequences import calc_percentage_correct_sequences
from src.Latency import calc_primary_latency, calc_secondary_latency
from src.Duration import calc_primary_duration, calc_secondary_duration


class FAP_analysis(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.correct_sequences = Percentage_correct_sequences("Percentage of correct sequences")
        self.layout.addWidget(self.correct_sequences)

        self.latency = Latency_duration("Latency")
        self.layout.addWidget(self.latency)

        self.duration = Latency_duration("Duration", latency=False)
        self.layout.addWidget(self.duration)
    
    

class Percentage_correct_sequences(QWidget):
    def __init__(self, label):
        super().__init__()

        self.layout = QGridLayout(self)

        self.label = QLabel(label)
        self.layout.addWidget(self.label, 0, 0)
        self.mpc_selector = Selector(".MPC")
        self.layout.addWidget(self.mpc_selector, 1, 0)

        self.button = QPushButton("Calculate")
        self.button.clicked.connect(self.calculate)
        self.layout.addWidget(self.button, 2, 0)


        self.checkbox = QCheckBox("Use Comma")
        self.layout.addWidget(self.checkbox, 2, 1)

    def calculate(self):
        comma = self.checkbox.isChecked()
        self.archive = open(self.mpc_selector.file_path)

        self.sieve_consequences = open('./src/consequences.txt')
        self.value_consequences = calc_row(self.archive, self.sieve_consequences, False, False)

        calc_percentage_correct_sequences(self.value_consequences, comma)
        # calcular_valorU(value, comma)


class Latency_duration(QWidget):
    def __init__(self, label, latency=True):
        super().__init__()
        self.latency = latency
        self.layout = QGridLayout(self)

        self.label = QLabel(label)
        self.layout.addWidget(self.label, 0, 0)
        # self.text_time = QLineEdit('Time data')
        # self.layout.addWidget(self.text_time, 1, 0)
        
        # self.text_consequences = QLineEdit('Consequences data')
        # self.layout.addWidget(self.text_consequences, 2, 0)
        self.mpc_selector = Selector(".MPC")
        self.layout.addWidget(self.mpc_selector, 1, 0)
        
        self.button = QPushButton("Separate each primary reinforcement")
        self.button.clicked.connect(self.calculate_primary)
        self.layout.addWidget(self.button, 3, 0)

        self.button = QPushButton("Separate each secondary reinforcement")
        self.button.clicked.connect(self.calculate_secondary)
        self.layout.addWidget(self.button, 3, 1)


        self.checkbox = QCheckBox("Use Comma")
        self.layout.addWidget(self.checkbox, 2, 1)

    def calculate_primary(self):
        comma = self.checkbox.isChecked()
        # value_time = self.text_time.text()
        # value_consequences = self.text_consequences.text()
        self.archive = open(self.mpc_selector.file_path)

        if self.latency:
            self.sieve_time = open('./src/latency.txt')
            self.value_time = calc_row(self.archive, self.sieve_time, False, False)
            self.sieve_consequences = open('./src/consequences.txt')
            self.value_consequences = calc_row(self.archive, self.sieve_consequences, False, False)
            calc_primary_latency(self.value_time, self.value_consequences, comma)
        else:
            self.sieve_time = open('./src/duration.txt')
            self.value_time = calc_row(self.archive, self.sieve_time, False, False)
            self.sieve_consequences = open('./src/consequences.txt')
            self.value_consequences = calc_row(self.archive, self.sieve_consequences, False, False)
            calc_primary_duration(self.value_time, self.value_consequences, comma)
            


    def calculate_secondary(self):
        comma = self.checkbox.isChecked()
        self.archive = open(self.mpc_selector.file_path)

        if self.latency:
            self.sieve_time = open('./src/latency.txt')
            self.value_time = calc_row(self.archive, self.sieve_time, False, False)
            self.sieve_consequences = open('./src/consequences.txt')
            self.value_consequences = calc_row(self.archive, self.sieve_consequences, False, False)
            calc_secondary_latency(self.value_time, self.value_consequences, comma)
        else:
            self.sieve_time = open('./src/latency.txt')
            self.value_time = calc_row(self.archive, self.sieve_time, False, False)
            self.sieve_consequences = open('./src/consequences.txt')
            self.value_consequences = calc_row(self.archive, self.sieve_consequences, False, False)
            calc_secondary_duration(self.value_time, self.value_consequences, comma)
