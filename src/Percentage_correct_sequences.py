from PySide6.QtGui import QClipboard

from src.Recorrence import remover_ponto_virgula, remover_data, remover_zeros


def calc_percentage_correct_sequences(string, comma):
    cb = QClipboard()
    row_data = string.split()
    if '.' in string or ',' in string:
        row_data = remover_ponto_virgula(row_data)
    if '/' in string:
        row_data = remover_data(row_data)
    if '0' in row_data:
        row_data = remover_zeros(row_data)

    firt_sr = 0
    second_sr = 0
    third_sr = 0
    fourth_sr = 0
    
    reinforce = 1

    for i in range(len(row_data)):

        if reinforce == 1:
            firt_sr += 1
        elif reinforce == 2:
            second_sr += 1
        elif reinforce == 3:
            third_sr += 1
        elif reinforce == 4:
            fourth_sr += 1

        if row_data[i] == '2':
            reinforce += 1
        elif row_data[i] == '1':
            reinforce = 1
    
    total_reinforces = row_data.count('1')
    
    result = f'Porcentagem de sequências corretas\r' + \
             f'Primeira Correta: \t{total_reinforces / firt_sr * 100}%\r' + \
             f'Segunda Correta: \t{total_reinforces / second_sr * 100}%\r' + \
             f'Terceira Correta: \t{total_reinforces / third_sr * 100}%\r' + \
             f'Quarta Correta: \t{total_reinforces / fourth_sr * 100}%\r'

    if comma:
        result = result.replace('.', ',')

    try:
        cb.setText(result)
        return "Done"
    except:
        return "Error"
