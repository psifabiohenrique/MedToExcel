from PySide6.QtGui import QClipboard
from med_to_excel.core.utils.correct_sequence_time import clear_data


def calc_correct_response_time(time_data, consequences_data, comma):
    cb = QClipboard()
    row_time_data = clear_data(time_data)
    row_consequences_data = clear_data(consequences_data)

    temp = []
    for i in row_time_data:
        temp.append(int(i.split('.')[0]))
    row_time_data = temp

    reinforce_number = 1
    result = {}

    for i in range(len(row_consequences_data)):

        if f"Reforço: {reinforce_number}" in result.keys():
            ...
        else:
            ...
            