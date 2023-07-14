from PySide6.QtGui import QClipboard

import math
from src.Recorrence import remover_data


def calcular_valorU(string, virgula):
    clipboard = QClipboard()
    if ',' in string:
        string = string.replace(',', '.')
    dados_brutos = string.split()
    if '/' in string:
        dados_brutos = remover_data(dados_brutos)
    dados = []
    for i in dados_brutos:
        dados.append(float(i))
    lista = []
    dividir = math.log2(len(dados)) // math.log2(2)
    acumulador = 0

    for i in dados:
        if i != 0:
            log_item = math.log2(float(i))
            log_2 = math.log2(2)
            lista.append((i * (log_item / log_2)) / dividir)
        else:
            lista.append(0)

    for i in lista:
        acumulador += i
    valor_u = acumulador * -1
    if virgula:
        valor_u = str(valor_u).replace('.', ',')

    try:
        clipboard.setText(valor_u)
        return 'Copiado'
    except:
        return 'Falha'
