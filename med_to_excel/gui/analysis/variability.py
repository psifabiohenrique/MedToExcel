from typing import Callable

from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QVBoxLayout,
)

from med_to_excel.core.utils.u_value import calcular_valorU
from med_to_excel.core.utils.recorrence import calcular_recorrencia
from med_to_excel.core.utils.different_sequences import calcular_NSeq
from med_to_excel.core.utils.switches import n_mudancas
from med_to_excel.core.utils.rng import calculate_RNG


class BaseAnalysisWidget(QWidget):
    """Classe base para widgets de análise que compartilham funcionalidades comuns."""

    def __init__(self) -> None:
        super().__init__()
        self.layout: QVBoxLayout = QVBoxLayout(self)

    def _create_functionality_group(
        self,
        label: str,
        instruction: str,
        calculation_func: Callable,
        has_comma_option: bool = True,
    ) -> "GroupFunctionality":
        """Cria um grupo de funcionalidade com configuração comum.

        Args:
            label: Rótulo para a funcionalidade
            instruction: Instrução para o campo de entrada
            calculation_func: Função de cálculo a ser chamada
            has_comma_option: Se deve incluir opção de vírgula

        Returns:
            Grupo de funcionalidade configurado
        """
        group = GroupFunctionality(label, instruction, has_comma_option)
        group.button.clicked.connect(
            lambda: self._calculate_and_clear(group, calculation_func)
        )
        self.layout.addWidget(group)
        return group

    def _calculate_and_clear(
        self, group: "GroupFunctionality", calculation_func: Callable
    ) -> None:
        """Executa o cálculo e limpa o campo de entrada.

        Args:
            group: Grupo de funcionalidade
            calculation_func: Função de cálculo a ser chamada
        """
        value: str = group.text.text()
        group.text.setText("")

        if hasattr(group, "checkbox"):
            comma: bool = group.checkbox.isChecked()
            calculation_func(value, comma)
        else:
            calculation_func(value)


class Variability(BaseAnalysisWidget):
    """Widget para análise de variabilidade."""

    def __init__(self) -> None:
        """
        Inicializa o widget de variabilidade.

        Configura o layout do widget usando QVBoxLayout e inicializa vários objetos
        GroupFunctionality para diferentes funcionalidades. Cada objeto GroupFunctionality
        é conectado a um evento de clique de botão para executar uma ação específica.
        """
        super().__init__()

        self.u_value = self._create_functionality_group(
            "U Value", "Cole a frequência relativa", calcular_valorU
        )

        self.recurrence_time = self._create_functionality_group(
            "Recurrence Time",
            "Cole as sequências em ordem no formato '11221'",
            calcular_recorrencia,
        )

        self.different_sequences = self._create_functionality_group(
            "Different Sequences",
            "Cole as sequências no formato '11221'",
            calcular_NSeq,
            has_comma_option=False,
        )

        self.switches = self._create_functionality_group(
            "Switches", "Cole as sequências no formato '11221'", n_mudancas
        )

        self.rng = self._create_functionality_group(
            "RNG", "Cole as sequências no formato '11221'", calculate_RNG
        )


class GroupFunctionality(QWidget):
    """Widget para agrupar funcionalidades relacionadas."""

    def __init__(
        self,
        label: str,
        instruction: str = "Enter data",
        has_comma_option: bool = True,
    ) -> None:
        """
        Inicializa o widget de funcionalidade em grupo.

        Args:
            label: Rótulo para a funcionalidade
            instruction: Instrução para o campo de entrada
            has_comma_option: Se deve incluir opção de vírgula
        """
        super().__init__()

        self.layout: QGridLayout = QGridLayout(self)

        self.label: QLabel = QLabel(label)
        self.layout.addWidget(self.label, 0, 0)

        self.text: QLineEdit = QLineEdit(instruction)
        self.layout.addWidget(self.text, 1, 0)

        self.button: QPushButton = QPushButton("Calculate")
        self.layout.addWidget(self.button, 2, 0)

        if has_comma_option:
            self.checkbox: QCheckBox = QCheckBox("Use Comma")
            self.layout.addWidget(self.checkbox, 2, 1)
