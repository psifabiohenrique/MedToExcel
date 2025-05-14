from typing import List, Tuple, Union, Literal
from pathlib import Path

from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
    QGridLayout,
    QLabel,
    QCheckBox,
    QVBoxLayout,
    QFrame,
)

from med_to_excel.gui.widgets.selector import Selector
from med_to_excel.core.utils.percentage_correct_sequences import (
    calc_percentage_correct_sequences,
)
from med_to_excel.core.utils.latency import calc_primary_latency
from med_to_excel.core.utils.duration import calc_primary_duration
from med_to_excel.core.utils.trial_duration import (
    calc_primary_trial_duration_or_individual_latency,
)
from med_to_excel.core.utils.error_log import set_errors


# Tipos personalizados para melhor documentação
AnalysisType = Literal[
    "latency",
    "sequence duration",
    "trial duration",
    "correct sequence time",
    "Percentage of correct sequences",
]

FileData = Tuple[List[float], List[float]]
FilePath = Union[str, Path]


class BaseAnalysisWidget(QWidget):
    """Classe base para widgets de análise que compartilham funcionalidades comuns."""

    def __init__(self) -> None:
        super().__init__()
        self.layout: QVBoxLayout = QVBoxLayout(self)

    def _create_program_choice(
        self,
        label: str,
        selector: Selector,
        program: AnalysisType,
        has_individual_option: bool = False,
    ) -> "Program_choice":
        """Cria um widget de escolha de programa com configuração comum.

        Args:
            label: Rótulo para o programa
            selector: Seletor de arquivo
            program: Tipo de programa
            has_individual_option: Se deve incluir opção de resposta individual

        Returns:
            Widget de escolha de programa configurado
        """
        choice = Program_choice(label, selector, program, has_individual_option)
        self.layout.addWidget(choice)
        return choice


class FAP_analysis(BaseAnalysisWidget):
    """Widget principal para análise FAP."""

    def __init__(self) -> None:
        super().__init__()

        self.mpc_selector: Selector = Selector(".MPC")
        self.layout.addWidget(self.mpc_selector)

        self.correct_sequences = self._create_program_choice(
            "Percentage of correct sequences",
            self.mpc_selector,
            program=Constant.PERCENTAGE,
        )

        self.latency = self._create_program_choice(
            "Latency",
            self.mpc_selector,
            program=Constant.LATENCY,
            has_individual_option=True,
        )

        self.duration = self._create_program_choice(
            "Sequence Duration",
            self.mpc_selector,
            program=Constant.SEQUENCE_DURATION,
        )

        self.trial_duration = self._create_program_choice(
            "Trial Duration (latency + sequence duration)",
            self.mpc_selector,
            program=Constant.TRIAL_DURATION,
        )

        self.correct_sequence_time = self._create_program_choice(
            "Correct Sequence/Response Time",
            self.mpc_selector,
            program=Constant.CORRECT_SEQUENCE_TIME,
            has_individual_option=True,
        )


class Program_choice(QWidget):
    """Widget para escolha de programa de análise."""

    def __init__(
        self,
        label: str,
        selector: Selector,
        program: AnalysisType = "latency",
        has_individual_option: bool = False,
    ) -> None:
        """
        Inicializa o widget de escolha de programa.

        Args:
            label: Rótulo para o programa
            selector: Seletor de arquivo
            program: Tipo de programa
            has_individual_option: Se deve incluir opção de resposta individual
        """
        super().__init__()
        self.program: AnalysisType = program
        self.layout: QGridLayout = QGridLayout(self)

        self.label: QLabel = QLabel(label)
        self.layout.addWidget(self.label, 0, 0)

        self.mpc_selector: Selector = selector

        self.button: QPushButton = QPushButton("Calculate")
        self.button.clicked.connect(self.calculate_primary)
        self.layout.addWidget(self.button, 0, 1)

        self.checkbox: QCheckBox = QCheckBox("Use Comma")
        self.layout.addWidget(self.checkbox, 0, 2)

        if has_individual_option:
            self.checkbox_individual: QCheckBox = QCheckBox(
                "Individual Responses"
            )
            self.layout.addWidget(self.checkbox_individual, 0, 3)

        # Adiciona um separador
        frame: QFrame = QFrame()
        frame.setFrameShape(QFrame.HLine)
        frame.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(frame, 2, 0, 1, 4)

    def _calculate_values(
        self, time_file: FilePath, consequences_file: FilePath
    ) -> FileData:
        """Calcula valores comuns para diferentes tipos de análise.

        Args:
            time_file: Caminho para o arquivo de tempo
            consequences_file: Caminho para o arquivo de consequências

        Returns:
            Tupla contendo os valores de tempo e consequências calculados
        """
        self.archive = open(self.mpc_selector.file_path)
        self.sieve_time = open(time_file)
        self.value_time = calc_row(self.archive, self.sieve_time, False, False)
        self.sieve_consequences = open(consequences_file)
        self.value_consequences = calc_row(
            self.archive, self.sieve_consequences, False, False
        )
        return self.value_time, self.value_consequences

    def calculate_primary(self) -> None:
        """Executa o cálculo principal baseado no tipo de programa selecionado."""
        try:
            comma: bool = self.checkbox.isChecked()
            self.archive = open(self.mpc_selector.file_path)

            if self.program == Constant.LATENCY:
                if self.checkbox_individual.isChecked():
                    value_time, value_consequences = self._calculate_values(
                        "./src/latency.txt", "./src/consequences.txt"
                    )
                    calc_primary_trial_duration_or_individual_latency(
                        value_time, value_consequences, comma, individual=True
                    )
                else:
                    value_time, value_consequences = self._calculate_values(
                        "./src/latency.txt", "./src/consequences.txt"
                    )
                    calc_primary_latency(value_time, value_consequences, comma)
            elif self.program == Constant.SEQUENCE_DURATION:
                value_time, value_consequences = self._calculate_values(
                    "./src/duration.txt", "./src/consequences.txt"
                )
                calc_primary_duration(value_time, value_consequences, comma)
            elif self.program == Constant.TRIAL_DURATION:
                value_time, value_consequences = self._calculate_values(
                    "./src/trial_duration.txt", "./src/consequences.txt"
                )
                calc_primary_trial_duration_or_individual_latency(
                    value_time, value_consequences, comma
                )
            elif self.program == Constant.CORRECT_SEQUENCE_TIME:
                if self.checkbox_individual.isChecked():
                    value_time, value_consequences = self._calculate_values(
                        "./src/latency.txt", "./src/consequences.txt"
                    )
                    calc_correct_sequence_time(
                        value_time, value_consequences, comma, individual=True
                    )
                else:
                    value_time, value_consequences = self._calculate_values(
                        "./src/trial_duration.txt", "./src/consequences.txt"
                    )
                    calc_correct_sequence_time(
                        value_time, value_consequences, comma
                    )
            elif self.program == Constant.PERCENTAGE:
                self.sieve_consequences = open("./src/consequences.txt")
                self.value_consequences = calc_row(
                    self.archive, self.sieve_consequences, False, False
                )
                calc_percentage_correct_sequences(self.value_consequences, comma)
        except Exception as e:
            set_errors(e)


class Constant:
    """Constantes utilizadas no programa."""

    LATENCY: AnalysisType = "latency"
    SEQUENCE_DURATION: AnalysisType = "sequence duration"
    TRIAL_DURATION: AnalysisType = "trial duration"
    CORRECT_SEQUENCE_TIME: AnalysisType = "correct sequence time"
    PERCENTAGE: AnalysisType = "Percentage of correct sequences"
