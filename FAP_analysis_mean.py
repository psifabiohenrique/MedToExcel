from PySide6.QtWidgets import QPushButton, QWidget, QGridLayout, QLabel, QLineEdit, QCheckBox, QVBoxLayout, QHBoxLayout, QFrame

from Selector import Selector
from src.Copy import calc_row
from src.mean_fap_analysis import calc_latency, calc_sequence_duration, calc_trial_duration



class FAP_analysis_mean(QWidget):


    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.mpc_layout = QWidget()
        self.mpc_layout.layout = QHBoxLayout(self.mpc_layout)

        self.mpc_selector = Selector(".MPC")
        self.mpc_layout.layout.addWidget(self.mpc_selector)
        self.individual_response_checkbox = QCheckBox("Individual Response")
        self.mpc_layout.layout.addWidget(self.individual_response_checkbox)

        self.layout.addWidget(self.mpc_layout)

        self.latency = Program_choice(self.mpc_selector, self.individual_response_checkbox, program=Constant.LATENCY)
        self.layout.addWidget(self.latency)


        self.duration = Program_choice(self.mpc_selector, self.individual_response_checkbox, program=Constant.SEQUENCE_DURATION)
        self.layout.addWidget(self.duration)

        self.trial_duration = Program_choice(self.mpc_selector, self.individual_response_checkbox, program=Constant.TRIAL_DURATION)
        self.layout.addWidget(self.trial_duration)

        # self.correct_sequence_time = Program_choice("Correct Sequence/Response Time", self.mpc_selector, program=Constant.CORRECT_SEQUENCE_TIME)
        # self.layout.addWidget(self.correct_sequence_time)
    
    

class Program_choice(QWidget):
    def __init__(self, selector, individual, program="latency"):
        super().__init__()
        self.program = program
        self.individual = individual
        
        self.layout = QGridLayout(self)
      
        self.mpc_selector = selector
        
                
        self.button = QPushButton(program)
        self.button.clicked.connect(self.calculate_primary)
        self.layout.addWidget(self.button, 0, 0)

        
        # Adiciona um separador
        frame = QFrame()
        frame.setFrameShape(QFrame.HLine)
        frame.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(frame, 2, 0, 1, 1)

    def calculate_primary(self):
        self.archive = open(self.mpc_selector.file_path)

        if self.program == Constant.LATENCY:
            if self.individual.isChecked():
                self.sieve_time = open('./src/latency.txt')
                self.value_time = calc_row(self.archive, self.sieve_time, False, False)
                self.sieve_consequences = open('./src/consequences.txt')
                self.value_consequences = calc_row(self.archive, self.sieve_consequences, False, False)
                calc_latency(self.value_time, self.value_consequences, True, f"{self.program} - {self.mpc_selector.file_path.split("/")[-1]}")
            else:
                self.sieve_time = open('./src/latency.txt')
                self.value_time = calc_row(self.archive, self.sieve_time, False, False)
                self.sieve_consequences = open('./src/consequences.txt')
                self.value_consequences = calc_row(self.archive, self.sieve_consequences, False, False)
                calc_latency(self.value_time, self.value_consequences, False, f"{self.program} - {self.mpc_selector.file_path.split("/")[-1]}")

        elif self.program == Constant.SEQUENCE_DURATION:
            self.sieve_time = open('./src/duration.txt')
            self.value_time = calc_row(self.archive, self.sieve_time, False, False)
            self.sieve_consequences = open('./src/consequences.txt')
            self.value_consequences = calc_row(self.archive, self.sieve_consequences, False, False)
            calc_sequence_duration(self.value_time, self.value_consequences, f"{self.program} - {self.mpc_selector.file_path.split("/")[-1]}")
            
        elif self.program == Constant.TRIAL_DURATION:
            self.sieve_time = open('./src/trial_duration.txt')
            self.value_time = calc_row(self.archive, self.sieve_time, False, False)
            self.sieve_consequences = open('./src/consequences.txt')
            self.value_consequences = calc_row(self.archive, self.sieve_consequences, False, False)
            calc_trial_duration(self.value_time, self.value_consequences, f"{self.program} - {self.mpc_selector.file_path.split("/")[-1]}")
        elif self.program == Constant.CORRECT_SEQUENCE_TIME:
            if self.individual.isChecked():
                self.sieve_time = open('./src/latency.txt')
                self.value_time = calc_row(self.archive, self.sieve_time, False, False)
                self.sieve_consequences = open('./src/consequences.txt')
                self.value_consequences = calc_row(self.archive, self.sieve_consequences, False, False)
                
            else:
                self.sieve_time = open('./src/trial_duration.txt')
                self.value_time = calc_row(self.archive, self.sieve_time, False, False)
                self.sieve_consequences = open('./src/consequences.txt')
                self.value_consequences = calc_row(self.archive, self.sieve_consequences, False, False)
                
        elif self.program == Constant.PERCENTAGE:
            self.sieve_consequences = open('./src/consequences.txt')
            self.value_consequences = calc_row(self.archive, self.sieve_consequences, False, False)
            


class Constant():
    LATENCY = "latency"
    SEQUENCE_DURATION = "sequence duration"
    TRIAL_DURATION = "trial duration"
    CORRECT_SEQUENCE_TIME = "correct sequence time"
    PERCENTAGE = "Percentage of correct sequences"