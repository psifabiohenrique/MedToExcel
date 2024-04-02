from typing import List, Dict
import math
import numpy as np
from PySide6.QtGui import QClipboard
from src.universe_dict import universe_four_responses, universe_six_responses, universe_eight_responses, universe_five_responses
from src.Recorrence import remover_data


def calculate_RNG(string: List[str], comma: bool=True) -> float:
    """
    Calculate the RNG of a list of sequences copied from a Excel row.

    Args:
        sequences (List[str]): List of sequences.

    Returns:
        float: The calculated RNG value.
    """

    if ',' in string:
        string = string.replace(',', '.')
    row_data = string.split()
    if '/' in string:
        row_data = remover_data(row_data)

    universe_inverted: Dict[int, str]
    condition = len(row_data[0])
    
    if condition == 4:
        universe_inverted = universe_four_responses
    elif condition == 5:
        universe_inverted = universe_five_responses
    elif condition == 6:
        universe_inverted = universe_six_responses
    elif condition == 8:
        universe_inverted = universe_eight_responses
    
    # organize the sequences strings as keys and their indices as values
    universe = {v: i for i, v in enumerate(universe_inverted)}
    
    # count the number of sequence dyads that occurred in the session
    occurrence_matrix = np.zeros((2 ** condition, 2 ** condition))
    for i, sequence in enumerate(row_data):
        if i != 0:
            current = universe[sequence]
            previous = universe[row_data[i - 1]]
            occurrence_matrix[previous][current] += 1

    numerator_sum = 0
    denominator_sum = 0
    
    for row in occurrence_matrix:
        for column in row:
            try:
                temp = math.log(column)
            except ValueError:
                temp = 0
            numerator_sum += column * temp
    
    for row in occurrence_matrix:
        for column in row:
            try:
                temp = math.log(sum(row))
            except ValueError:
                temp = 0
            denominator_sum += column * temp
    
    result = str(numerator_sum / denominator_sum)
    if comma:
        result = result.replace('.', ',')
    clipboard = QClipboard()
    clipboard.setText(result)

    return numerator_sum / denominator_sum
