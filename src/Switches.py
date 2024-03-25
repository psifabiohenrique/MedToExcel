from PySide6.QtGui import QClipboard
from src.Recorrence import remover_ponto_virgula, remover_data, remover_zeros



def n_mudancas(string, comma=True):
    cb = QClipboard()
    dados_brutos = string.split()
    if '.' in string or ',' in string:
        dados_brutos = remover_ponto_virgula(dados_brutos)
    if '/' in string:
        dados_brutos = remover_data(dados_brutos)
    if '0' in dados_brutos:
        dados_brutos = remover_zeros(dados_brutos)
    conjunto = set(dados_brutos)
    lista_dados = []

    for i in dados_brutos:
        resp = i[0]
        n_mud = 0
        for ii in i:
            if resp != ii:
                resp = ii
                n_mud += 1
        lista_dados.append(n_mud)

    def calc_map(i, comma=True):
        return (i / len(dados_brutos)) * 100
    resultado = [lista_dados.count(x) for x in range(len(dados_brutos[0]))]
    # resultado = np.array(resultado)
    # resultado = (resultado / len(dados_brutos)) * 100
    resultado2 = map(calc_map, resultado)
    string_final = ''
    for i in resultado2:
        string_final += f'{i}\r'
    
    if comma:
        string_final = string_final.replace('.', ',')
    cb.setText(string_final)
    # pyperclip.copy(string_final)
    return resultado