from PySide6.QtWidgets import QPushButton, QWidget, QGridLayout, QLabel, QLineEdit, QCheckBox, QVBoxLayout

from src.U_Value import calcular_valorU
from src.Recorrence import calcular_recorrencia
from src.Different_sequences import calcular_NSeq
from src.Switches import n_mudancas


class Variability(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.u_value = GroupFunctionality("U Value")
        self.u_value.button.clicked.connect(self.get_u_value)
        self.layout.addWidget(self.u_value)

        self.recurrence_time = GroupFunctionality("Recurrence Time")
        self.recurrence_time.button.clicked.connect(self.get_recurrence)
        self.layout.addWidget(self.recurrence_time)

        self.different_sequences = GroupFunctionality("Different Sequences")
        self.different_sequences.button.clicked.connect(self.get_different_sequence)
        self.layout.addWidget(self.different_sequences)

        self.switches = GroupFunctionality("Switches")
        self.switches.button.clicked.connect(self.get_switches)
        self.layout.addWidget(self.switches)

    def get_u_value(self):
        comma = self.u_value.checkbox.isChecked()
        value = self.u_value.text.text()
        self.u_value.text.setText("")
        calcular_valorU(value, comma)
    
    def get_recurrence(self):
        comma = self.recurrence_time.checkbox.isChecked()
        value = self.recurrence_time.text.text()
        self.recurrence_time.text.setText("")
        calcular_recorrencia(value, comma)
    
    def get_different_sequence(self):
        # comma = self.different_sequences.checkbox.isChecked()
        value = self.different_sequences.text.text()
        self.different_sequences.text.setText("")
        calcular_NSeq(value)
    
    def get_switches(self):
        # comma = self.switches.checkbox.isChecked()
        value = self.switches.text.text()
        self.switches.text.setText("")
        n_mudancas(value)

class GroupFunctionality(QWidget):
    def __init__(self, label):
        super().__init__()

        self.layout = QGridLayout(self)

        self.label = QLabel(label)
        self.layout.addWidget(self.label, 0, 0)
        self.text = QLineEdit()
        self.layout.addWidget(self.text, 1, 0)
        self.button = QPushButton("Calculate")
        self.layout.addWidget(self.button, 2, 0)
        if "Switches" != label != "Different Sequences":
            self.checkbox = QCheckBox("Use Comma")
            self.layout.addWidget(self.checkbox, 2, 1)