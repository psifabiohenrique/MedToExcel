from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
    QGridLayout,
    QCheckBox,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)

from med_to_excel.gui.widgets.selector import Selector
from med_to_excel.core.utils.copy import calc_row
from med_to_excel.core.utils.mean_fap_analysis import (
    calc_latency,
    calc_sequence_duration,
    calc_trial_duration,
)
from med_to_excel.core.utils.error_log import set_errors


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

        self.latency = Program_choice(
            self.mpc_selector,
            self.individual_response_checkbox,
            program=Constant.LATENCY,
        )
        self.layout.addWidget(self.latency)

        self.duration = Program_choice(
            self.mpc_selector,
            self.individual_response_checkbox,
            program=Constant.SEQUENCE_DURATION,
        )
        self.layout.addWidget(self.duration)

        self.trial_duration = Program_choice(
            self.mpc_selector,
            self.individual_response_checkbox,
            program=Constant.TRIAL_DURATION,
        )
        self.layout.addWidget(self.trial_duration)


class Program_choice(QWidget):
    def __init__(
        self, selector, individual, program="latency (Response and Sequence)"
    ):
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
                self.sieve_time = open("./src/latency.txt")
                self.value_time = calc_row(
                    self.archive, self.sieve_time, False, False
                )
                self.sieve_consequences = open("./src/consequences.txt")
                self.value_consequences = calc_row(
                    self.archive, self.sieve_consequences, False, False
                )
                try:
                    calc_latency(
                        self.value_time,
                        self.value_consequences,
                        True,
                        f"{self.program} - {self.mpc_selector.file_path.split('/')[-1]}",
                    )
                except Exception as e:
                    set_errors(e)
            else:
                self.sieve_time = open("./src/latency.txt")
                self.value_time = calc_row(
                    self.archive, self.sieve_time, False, False
                )
                self.sieve_consequences = open("./src/consequences.txt")
                self.value_consequences = calc_row(
                    self.archive, self.sieve_consequences, False, False
                )
                try:
                    calc_latency(
                        self.value_time,
                        self.value_consequences,
                        False,
                        f"{self.program} - {self.mpc_selector.file_path.split('/')[-1]}",
                    )
                except Exception as e:
                    set_errors(e)

        elif self.program == Constant.SEQUENCE_DURATION:
            self.sieve_time = open("./src/duration.txt")
            self.value_time = calc_row(
                self.archive, self.sieve_time, False, False
            )
            self.sieve_consequences = open("./src/consequences.txt")
            self.value_consequences = calc_row(
                self.archive, self.sieve_consequences, False, False
            )
            try:
                calc_sequence_duration(
                    self.value_time,
                    self.value_consequences,
                    f"{self.program} - {self.mpc_selector.file_path.split('/')[-1]}",
                )
            except Exception as e:
                set_errors(e)

        elif self.program == Constant.TRIAL_DURATION:
            if self.individual.isChecked():
                self.sieve_time = open("./src/latency.txt")
                self.value_time = calc_row(
                    self.archive, self.sieve_time, False, False
                )
                self.sieve_consequences = open("./src/consequences.txt")
                self.value_consequences = calc_row(
                    self.archive, self.sieve_consequences, False, False
                )
                try:
                    calc_trial_duration(
                        self.value_time,
                        self.value_consequences,
                        True,
                        f"{self.program} - {self.mpc_selector.file_path.split('/')[-1]}",
                    )
                except Exception as e:
                    set_errors(e)
            else:
                self.sieve_time = open("./src/trial_duration.txt")
                self.value_time = calc_row(
                    self.archive, self.sieve_time, False, False
                )
                self.sieve_consequences = open("./src/consequences.txt")
                self.value_consequences = calc_row(
                    self.archive, self.sieve_consequences, False, False
                )
                try:
                    calc_trial_duration(
                        self.value_time,
                        self.value_consequences,
                        False,
                        f"{self.program} - {self.mpc_selector.file_path.split('/')[-1]}",
                    )
                except Exception as e:
                    set_errors(e)


class Constant:
    LATENCY = "latency (Response and Sequence)"
    SEQUENCE_DURATION = "sequence duration"
    TRIAL_DURATION = "trial duration (Response and Sequence)"
    CORRECT_SEQUENCE_TIME = "correct sequence time"
    PERCENTAGE = "Percentage of correct sequences"
