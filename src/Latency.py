from PySide6.QtGui import QClipboard

from src.Recorrence import remover_data


def calc_primary_latency(time_data, consequences_data, comma):
    cb = QClipboard()
    row_time_data = clear_data(time_data)
    row_consequences_data = clear_data(consequences_data)

    all_latency = []
    for i in row_time_data:
        if i[-3:] == '001':
            temp = i[:-3]
            temp = temp.replace('.', '')
            all_latency.append(int(temp))
    reinforce_number = 0
    result = {}
    for i in range(len(row_consequences_data)):

        if f"Reforço: {reinforce_number}" in result.keys():
            result[f"Reforço: {reinforce_number}"].append(all_latency[i])
        else:
            result[str(f"Reforço: {reinforce_number}")] = [all_latency[i]]

        if row_consequences_data[i][0] == '1':
            reinforce_number += 1
    
    result_string = 'Tabela latência por reforço: \r'
    for k in result.keys():
        result_string += f"{k}:"
        result_string += f"\t Média:\t{sum(result[k])/len(result[k])}\tSoma:\t{sum(result[k])} \tLatências individuais:"
        for i in result[k]:
            result_string += f"\t{i}"
        result_string += "\r"

    if comma:
        result_string = result_string.replace('.', ',')

    try:
        cb.setText(result_string)
        return "Done"
    except:
        return "Error"



def calc_secondary_latency(time_data, consequences_data, comma):
    cb = QClipboard()
    row_time_data = clear_data(time_data)
    row_consequences_data = clear_data(consequences_data)

    all_latency = []
    for i in row_time_data:
        if i[-3:] == '001':
            temp = i[:-3]
            temp = temp.replace('.', '')
            all_latency.append(int(temp))
    reinforce_number = 1
    result = {}

    for i in range(len(row_consequences_data)):

        if f"Correta: {reinforce_number}" in result.keys():
            result[f"Correta: {reinforce_number}"].append(all_latency[i])
        else:
            result[str(f"Correta: {reinforce_number}")] = [all_latency[i]]

        if row_consequences_data[i][0] == '2':
            if reinforce_number == 4:
                reinforce_number = 1
            else:
                reinforce_number += 1
    
    result_string = 'Tabela latência por reforço secundário: \r'
    for k in result.keys():
        result_string += f"{k}:"
        result_string += f"\t Média:\t{sum(result[k])/len(result[k])}\tSoma:\t{sum(result[k])} \tLatências individuais:"
        for i in result[k]:
            result_string += f"\t{i}"
        result_string += "\r"

    if comma:
        result_string = result_string.replace('.', ',')

    try:
        cb.setText(result_string)
        return "Done"
    except:
        return "Error"
    


def clear_data(string):
    row_data = string.split()
    if ',' in string:
        temp = []
        for i in row_data:
            temp.append(i.replace(',', '.'))
        row_data = temp
    if '/' in string:
        row_data = remover_data(row_data)
    
    temp = []
    for i in row_data:
        if '0.000' != i:
            temp.append(i)

    row_data = temp
    return row_data