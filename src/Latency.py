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

    session_latency = []
    session_first_second = []
    session_second_third = []

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
                counter = 1
                for i in result[f"Reforço: {last_reinforce}"]:
                    mean_latency_list.append(i[0])
                    mean_block_latency += i[0]
                    mean_first_second_list.append(i[1])
                    mean_block_first_second += i[1]
                    mean_second_third_list.append(i[2])
                    mean_block_second_third += i[2]
                    result_string += f"{i[0]}\t{i[1]}\t{i[2]}\t\t"
                    
                    counter += 1

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

            session_latency.append(sum(mean_latency_list))
            session_first_second.append(sum(mean_first_second_list))
            session_second_third.append(sum(mean_second_third_list))
        except:
            result_string += f"Média:\t0\t0\t0\t\r"
        

    """
    Calculating the session mean
    """
    mean_result = {
        '1':[],
        '2':[],
        '3':[],
        '4':[],
        '5':[],
        '6':[],
        '7':[],
        '8':[],
        '9':[],
        '10':[]
    }
    count_reinforce = 1
    for key, value in result.items():
        """
        Organizing the data in a dictionary to calculate session resume mean
        """
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

    result_string += f"\r\rMédia\tInício-1a R\t1a e 2a Rs\t2a e 3a Rs\tRepete -->\r"
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
    final_mean_latency = []
    final_mean_first_second = []
    final_mean_second_third = []
    for i in range(10):
        """
        Calculating the mean and writing it in the result string
        """
        result_string += f"{row_labels[i]}\t"
        mean_latency_list2 = []
        mean_first_second_list2 = []
        mean_second_third_list2 = []
        
        count = 0
        for j in mean_result[str(i + 1)]:
            sum_latency = 0
            sum_first_second = 0
            sum_second_third = 0
            for k in j:
                sum_latency += k[0]
                sum_first_second += k[1]
                sum_second_third += k[2]

                try :
                    final_mean_latency[count].append(k[0])
                    final_mean_first_second[count].append(k[1])
                    final_mean_second_third[count].append(k[2])
                except IndexError:
                    final_mean_latency.append([k[0]])
                    final_mean_first_second.append([k[1]])
                    final_mean_second_third.append([k[2]])

                mean_latency_list2.append(k[0])
                mean_first_second_list2.append(k[1])
                mean_second_third_list2.append(k[2])
            count += 1        


            result_string += f"{sum_latency/len(j)}\t"
            result_string += f"{sum_first_second/len(j)}\t"
            result_string += f"{sum_second_third/len(j)}\t\t"
    
        try:
            result_string += f"\tMédia:\t{sum(mean_latency_list2)/len(mean_latency_list2)}\t{sum(mean_first_second_list2)/len(mean_first_second_list2)}\t{sum(mean_second_third_list2)/len(mean_second_third_list2)}\t\r"
        except ZeroDivisionError:
            result_string += f"\tMédia:\t0\t0\t0\t\r"


    result_string += "\r"
    result_string += f"Média Sessão\t"

    for i in range(len(final_mean_latency)):
        result_string += f"{sum(final_mean_latency[i])/len(final_mean_latency[i])}\t"
        result_string += f"{sum(final_mean_first_second[i])/len(final_mean_first_second[i])}\t"
        result_string += f"{sum(final_mean_second_third[i])/len(final_mean_second_third[i])}\t\t"
    
    result_string += f"\tMédia:\t{sum(session_latency) / (len(row_time_data) / 3)}\t{sum(session_first_second) / (len(row_time_data) / 3)}\t{sum(session_second_third) / (len(row_time_data) / 3)}\t\r"

        


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