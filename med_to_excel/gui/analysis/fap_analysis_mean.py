from typing import List, Tuple, Optional, Union, Literal
from pathlib import Path

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
from med_to_excel.core.utils.mean_fap_analysis import (
    calc_latency,
    calc_sequence_duration,
    calc_trial_duration,
)
from med_to_excel.core.utils.error_log import set_errors


# Tipos personalizados para melhor documentação
AnalysisType = Literal[
    "latency (Response and Sequence)",
    "sequence duration",
    "trial duration (Response and Sequence)",
    "correct sequence time",
    "Percentage of correct sequences",
]

FileData = Tuple[List[float], List[float]]
FilePath = Union[str, Path]


class BaseAnalysisWidget(QWidget):
    """Classe base para widgets de análise que compartilham funcionalidades comuns."""

    def __init__(self) -> None:
        super().__init__()
        self._setup_mpc_selector()

    def _setup_mpc_selector(self) -> None:
        """Configura o seletor de arquivo MPC e checkbox de resposta individual."""
        self.mpc_layout: QWidget = QWidget()
        self.mpc_layout.layout: QHBoxLayout = QHBoxLayout(self.mpc_layout)

        self.mpc_selector: Selector = Selector(".MPC")
        self.mpc_layout.layout.addWidget(self.mpc_selector)

        self.individual_response_checkbox: QCheckBox = QCheckBox(
            "Individual Response"
        )
        self.mpc_layout.layout.addWidget(self.individual_response_checkbox)

        self.layout().addWidget(self.mpc_layout)

    def _get_file_name(self) -> str:
        """Retorna o nome do arquivo selecionado para uso em mensagens."""
        return self.mpc_selector.file_path.split("/")[-1]

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


class FAP_analysis_mean(QWidget):
    """Widget principal para análise FAP."""

    def __init__(self) -> None:
        super().__init__()
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self._setup_mpc_selector()
        self._setup_analysis_buttons()

    def _setup_mpc_selector(self) -> None:
        """Configura o seletor de arquivo MPC e checkbox de resposta individual."""
        self.mpc_layout: QWidget = QWidget()
        self.mpc_layout.layout: QHBoxLayout = QHBoxLayout(self.mpc_layout)

        self.mpc_selector: Selector = Selector(".MPC")
        self.mpc_layout.layout.addWidget(self.mpc_selector)

        self.individual_response_checkbox: QCheckBox = QCheckBox(
            "Individual Response"
        )
        self.mpc_layout.layout.addWidget(self.individual_response_checkbox)

        self.layout.addWidget(self.mpc_layout)

    def _setup_analysis_buttons(self) -> None:
        """Configura os botões de análise."""
        self.latency: Program_choice = Program_choice(
            self.mpc_selector,
            self.individual_response_checkbox,
            program=Constant.LATENCY,
        )
        self.layout.addWidget(self.latency)

        self.duration: Program_choice = Program_choice(
            self.mpc_selector,
            self.individual_response_checkbox,
            program=Constant.SEQUENCE_DURATION,
        )
        self.layout.addWidget(self.duration)

        self.trial_duration: Program_choice = Program_choice(
            self.mpc_selector,
            self.individual_response_checkbox,
            program=Constant.TRIAL_DURATION,
        )
        self.layout.addWidget(self.trial_duration)


class Program_choice(QWidget):
    """Widget para escolha de programa de análise."""

    def __init__(
        self,
        selector: Selector,
        individual: QCheckBox,
        program: AnalysisType = "latency (Response and Sequence)",
    ) -> None:
        super().__init__()
        self.program: AnalysisType = program
        self.individual: QCheckBox = individual
        self.mpc_selector: Selector = selector
        self._setup_button()

    def _setup_button(self) -> None:
        """Configura o botão e o separador."""
        layout: QGridLayout = QGridLayout(self)
        self.button: QPushButton = QPushButton(self.program)
        self.button.clicked.connect(self.calculate_primary)
        layout.addWidget(self.button, 0, 0)

        frame: QFrame = QFrame()
        frame.setFrameShape(QFrame.HLine)
        frame.setFrameShadow(QFrame.Sunken)
        layout.addWidget(frame, 2, 0, 1, 1)

    def calculate_primary(self) -> None:
        """Executa o cálculo principal baseado no tipo de programa selecionado."""
        try:
            if self.program == Constant.LATENCY:
                self._calculate_latency()
            elif self.program == Constant.SEQUENCE_DURATION:
                self._calculate_sequence_duration()
            elif self.program == Constant.TRIAL_DURATION:
                self._calculate_trial_duration()
        except Exception as e:
            set_errors(e)

    def _calculate_latency(self) -> None:
        """Calcula a latência."""
        value_time, value_consequences = self._calculate_values(
            "./src/latency.txt", "./src/consequences.txt"
        )
        calc_latency(
            value_time,
            value_consequences,
            self.individual.isChecked(),
            f"{self.program} - {self._get_file_name()}",
        )

    def _calculate_sequence_duration(self) -> None:
        """Calcula a duração da sequência."""
        value_time, value_consequences = self._calculate_values(
            "./src/duration.txt", "./src/consequences.txt"
        )
        calc_sequence_duration(
            value_time,
            value_consequences,
            f"{self.program} - {self._get_file_name()}",
        )

    def _calculate_trial_duration(self) -> None:
        """Calcula a duração do trial."""
        time_file: FilePath = (
            "./src/latency.txt"
            if self.individual.isChecked()
            else "./src/trial_duration.txt"
        )
        value_time, value_consequences = self._calculate_values(
            time_file, "./src/consequences.txt"
        )
        calc_trial_duration(
            value_time,
            value_consequences,
            self.individual.isChecked(),
            f"{self.program} - {self._get_file_name()}",
        )

    def _get_file_name(self) -> str:
        """Retorna o nome do arquivo selecionado para uso em mensagens."""
        return self.mpc_selector.file_path.split("/")[-1]

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


class Constant:
    """Constantes utilizadas no programa."""

    LATENCY: AnalysisType = "latency (Response and Sequence)"
    SEQUENCE_DURATION: AnalysisType = "sequence duration"
    TRIAL_DURATION: AnalysisType = "trial duration (Response and Sequence)"
    CORRECT_SEQUENCE_TIME: AnalysisType = "correct sequence time"
    PERCENTAGE: AnalysisType = "Percentage of correct sequences"
