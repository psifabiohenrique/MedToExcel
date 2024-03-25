from PySide6.QtGui import QClipboard

from src.Recorrence import remover_data


def calc_primary_duration(time_data, consequences_data, comma):
    cb = QClipboard()
    row_time_data = clear_data(time_data)
    row_consequences_data = clear_data(consequences_data)

    reinforce_number = 1
    result = {}

    temp = []
    for i in row_time_data:
        temp.append(int(i.split('.')[0]))
    row_time_data = temp

    for i in range(len(row_consequences_data)):

        if f"Reforço: {reinforce_number}" in result.keys():
            result[f"Reforço: {reinforce_number}"].append(row_time_data[i])
        else:
            result[str(f"Reforço: {reinforce_number}")] = [row_time_data[i]]

        if row_consequences_data[i][0] == '1':
            reinforce_number += 1
    

    last_reinforce = 1
    result_string = 'TEMPO DE RESPOSTA = DURAÇÂO DA SEQUÊNCIA (tempo entre 1a e 3a respostas da sequência)\r\r'

    session_duration = []

    for block in range(5):
        """Separating five blocks of ten reinforcements"""
        result_string += f"Bloco {block + 1}:\t1ª sequência\t 2ª sequência\t 3ª sequência \t 4ª sequência \t--> continua\r"

        list_duration = []
        reinforce_per_block = 0

        for reinforce in range(10):
            result_string += f"{last_reinforce}° SR:\t"
            mean_block_duration = 0

            if f"Reforço: {last_reinforce}" in result.keys():
                for i in result[f"Reforço: {last_reinforce}"]:
                    list_duration.append(i)
                    mean_block_duration += i

                    result_string += f"{i}\t"
                
                mean_duration = mean_block_duration / len(result[f"Reforço: {last_reinforce}"])
                result_string += f"\tMédia:\t{mean_duration}\t"
                reinforce_per_block += 1
            
            result_string += "\r"
            last_reinforce += 1
        
        try:
            result_string += f"Média:\t{sum(list_duration) / reinforce_per_block}\r\r"

            session_duration.append(sum(list_duration))
        except:
            result_string += f"Média:\t0\r\r"
            
    
    """Calculating the session mean"""

    mean_result = {
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': [],
        '6': [],
        '7': [],
        '8': [],
        '9': [],
        '10': []
    }

    count_reinforce = 1

    for key, value in result.items():
        """Organizing the data in a dictionary to calculate session resume mean"""
        count_sequence = 0
        for i in value:
            try:
                mean_result[str(count_reinforce)][count_sequence].append(i)
            except IndexError:
                mean_result[str(count_reinforce)].append([i])
            count_sequence += 1
        
        if count_reinforce == 10:
            count_reinforce = 1
        else:
            count_reinforce += 1
        
    result_string += f"\r\rMédia:\t1ª sequência\t 2ª sequência\t 3ª sequência \t 4ª sequência \t--> continua\r"

    row_labels = [
        '1, 11, 21, 31, 41',
        '2, 12, 22, 32, 42',
        '3, 13, 23, 33, 43',
        '4, 14, 24, 34, 44',
        '5, 15, 25, 35, 45',
        '6, 16, 26, 36, 46',
        '7, 17, 27, 37, 47',
        '8, 18, 28, 38, 48',
        '9, 19, 29, 39, 49',
        '10, 20, 30, 40, 50'
    ]

    final_mean_duration = []

    for i in range(10):
        """
        Calculating the mean and writing it in the result string
        """

        result_string += f"{row_labels[i]}\t"
        mean_duration2 = []

        count = 0

        for j in mean_result[str(i + 1)]:
            sum_duration = 0

            for k in j:
                sum_duration += k

                try:
                    final_mean_duration[count].append(k)
                except IndexError:
                    final_mean_duration.append([k])

                mean_duration2.append(k)
            count += 1

            result_string += f"{sum_duration / len(j)}\t"

        try:
            result_string += f"\tMédia:\t{sum(mean_duration2) / len(mean_duration2)}\r"
        except ZeroDivisionError:
            result_string += f"\tMédia:\t0\r"
    
    result_string += "\rMédia Sessão:\t"

    for i in range(len(final_mean_duration)):
        result_string += f"{sum(final_mean_duration[i]) / len(final_mean_duration[i])}\t"
    

    result_string += f"\tMédia:\t{sum(session_duration) / len(row_time_data)}\r"



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