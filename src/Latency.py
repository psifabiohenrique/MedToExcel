from PySide6.QtGui import QClipboard

from src.Recorrence import remover_data


def calc_primary_latency(time_data, consequences_data, comma):
    """
    Calculate primary latency based on time and consequences data.

    Args:
        time_data: list, data related to latencytime
        consequences_data: list, data related to consequences
        comma: bool, whether to replace '.' with ',' in the result string

    Returns:
        Copy to clipboard a table with the data processed
        str, indicating whether the operation was successful or not
    """
    cb = QClipboard()
    row_time_data = clear_data(time_data)
    row_consequences_data = clear_data(consequences_data)

    all_latency = []
    first_to_second_response = []
    second_to_third_response = []
    
    for i in row_time_data:
        if i[-3:] == '001':
            temp = i[:-3]
            temp = temp.replace('.', '')
            all_latency.append(int(temp))
        elif i[-3:] == '002':
            temp = i[:-3]
            temp = temp.replace('.', '')
            first_to_second_response.append(int(temp))
        elif i[-3:] == '003':
            temp = i[:-3]
            temp = temp.replace('.', '')
            second_to_third_response.append(int(temp))

    reinforce_number = 1
    result = {}
    for i in range(len(row_consequences_data)):

        if f"Reforço: {reinforce_number}" in result.keys():
            result[f"Reforço: {reinforce_number}"].append([all_latency[i], first_to_second_response[i], second_to_third_response[i]])
        else:
            result[str(f"Reforço: {reinforce_number}")] = [[all_latency[i], first_to_second_response[i], second_to_third_response[i]]]

        if row_consequences_data[i][0] == '1':
            reinforce_number += 1
    
    result_string = 'LATÊNCIA (tempo entre início da tentativa e 1a resposta da sequência) e IRT (tempo entre 1a e 2a respostas e entre 2a e 3a respostas)\r\r'
    # for k in result.keys():
    #     result_string += f"{k}:"
    #     result_string += f"\t Média:\t{sum(result[k])/len(result[k])}\tSoma:\t{sum(result[k])} \tLatências individuais:"
    #     for i in result[k]:
    #         result_string += f"\t{i}"
    #     result_string += "\r"


    last_reinforce = 1
    for block in range(5):
        """Separating five blocks of ten reinforcements"""
        result_string += f"Bloco {block + 1}\tInício-1a R\t1a e 2a Rs\t2a e 3a Rs\tRepete -->\r"

        mean_latency_list = []
        mean_first_second_list = []
        mean_second_third_list = []
        reinforces_per_block = 0

        for reinforce in range(10):
            result_string += f"{last_reinforce}° SR:\t"
            mean_block_latency = 0
            mean_block_first_second = 0
            mean_block_second_third = 0
            if f"Reforço: {last_reinforce}" in result.keys():
                for i in result[f"Reforço: {last_reinforce}"]:
                    mean_latency_list.append(i[0])
                    mean_block_latency += i[0]
                    mean_first_second_list.append(i[1])
                    mean_block_first_second += i[1]
                    mean_second_third_list.append(i[2])
                    mean_block_second_third += i[2]
                    result_string += f"{i[0]}\t{i[1]}\t{i[2]}\t\t"

                mean_latency = mean_block_latency/len(result[f"Reforço: {last_reinforce}"])
                mean_first_second = mean_block_first_second/len(result[f"Reforço: {last_reinforce}"])
                mean_second_third = mean_block_second_third/len(result[f"Reforço: {last_reinforce}"])
                result_string += f"\tMédia:\t{mean_latency}\t{mean_first_second}\t{mean_second_third}\t"
                reinforces_per_block += 1
            
            result_string += "\r"
            last_reinforce += 1
        
        try:
            result_string += f"Média:\t{sum(mean_latency_list)/reinforces_per_block}\t"
            result_string += f"{sum(mean_first_second_list)/reinforces_per_block}\t"
            result_string += f"{sum(mean_second_third_list)/reinforces_per_block}\t\r"
        except:
            result_string += f"Média:\t0\t0\t0\t\r"
        



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