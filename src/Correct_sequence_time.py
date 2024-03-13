from PySide6.QtGui import QClipboard

from src.Recorrence import remover_data


def calc_correct_sequence_time(time_data, consequences_data, comma):
    cb = QClipboard()
    row_time_data = clear_data(time_data)
    row_consequences_data = clear_data(consequences_data)

    reinforce_number = 1
    result = {}

    temp = []
    for i in row_time_data:
        temp.append(int(i.split('.')[0]))
    row_time_data = temp

    secondary_reinforce_number = 0
    for i in range(len(row_consequences_data)):

        if f"Reforço: {reinforce_number}" in result.keys():
            result[f"Reforço: {reinforce_number}"][secondary_reinforce_number].append(row_time_data[i])
        else:
            result[str(f"Reforço: {reinforce_number}")] = [[row_time_data[i]],[],[],[]]

        if row_consequences_data[i][0] == '1':
            reinforce_number += 1
            secondary_reinforce_number = 0
        if row_consequences_data[i][0] == '2':
            secondary_reinforce_number += 1
    

    last_reinforce = 1
    result_string = 'TEMPO DA SEQUÊNCIA CORRETA (Tempo entre início da tentativa e a 3a resposta da sequência correta)\r\r'

    for block in range(5):
        """Separating five blocks of ten reinforcements"""
        result_string += f"Bloco {block + 1}:\t1ª sequência correta\t 2ª sequência correta\t 3ª sequência correta\t 4ª sequência correta\tMédia\r"

        list_duration = [[],[],[],[]]
        reinforce_per_block = 0

        for reinforce in range(10):
            result_string += f"{last_reinforce}° SR:\t"
            mean_block_duration = 0

            if f"Reforço: {last_reinforce}" in result.keys():
                for i in range(len(result[f"Reforço: {last_reinforce}"])):
                    list_duration[i].append(sum(result[f"Reforço: {last_reinforce}"][i]))

                for i in result[f"Reforço: {last_reinforce}"]:
                    mean_block_duration += sum(i)

                    result_string += f"{sum(i)}\t"
                
                mean_duration = mean_block_duration / len(result[f"Reforço: {last_reinforce}"])

                result_string += f"{mean_duration}"
                reinforce_per_block += 1
            
            result_string += "\r"
            last_reinforce += 1
        
        try:
            result_string += f"Média:\t{sum(list_duration[0]) / reinforce_per_block}\t{sum(list_duration[1]) / reinforce_per_block}\t{sum(list_duration[2]) / reinforce_per_block}\t{sum(list_duration[3]) / reinforce_per_block}\t{sum(list_duration[0] + list_duration[1] + list_duration[2] + list_duration[3]) / (reinforce_per_block)}\r\r"
        except:
            result_string += f"Média:\t0\r\r"
            
            

    if comma:
        result_string = result_string.replace('.', ',')

    try:
        cb.setText(result_string)
        return "Done"
    except:
        return "Error"



def calc_secondary_duration(time_data, consequences_data, comma):
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

        if f"Correta: {reinforce_number}" in result.keys():
            result[f"Correta: {reinforce_number}"].append(row_time_data[i])
        else:
            result[str(f"Correta: {reinforce_number}")] = [row_time_data[i]]

        if row_consequences_data[i][0] == '2':
            if reinforce_number == 4:
                reinforce_number = 1
            else:
                reinforce_number += 1
    
    result_string = 'Tabela duração por reforço secundário: \r'
    for k in result.keys():
        result_string += f"{k}:"
        result_string += f"\t Média:\t{sum(result[k])/len(result[k])}\tSoma:\t{sum(result[k])} \tDurações individuais:"
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