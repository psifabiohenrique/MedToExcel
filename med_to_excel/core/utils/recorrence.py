from statistics import mean, median
from .universe import universo4resp, universo5resp, universo6resp, universo8resp
from PySide6.QtGui import QClipboard


def remover_ponto_virgula(lista_seq:list[str]):
    resultados = []
    for i in lista_seq:
        if '.' in i:
            resultados.append(i.split('.')[0])
        elif ',' in i:
            resultados.append(i.split(',')[0])
    return resultados


def remover_data(lista_seq:list[str]):
    
    for i in range(len(lista_seq)):
        if '/' in lista_seq[i]:
            lista_seq.pop(i)
            return lista_seq
    return lista_seq


def remover_zeros(lista_seq:list[str]):
    resultados = []
    for i in lista_seq:
        if i != '0':
            resultados.append(i)
    return resultados
    

def calcular_recorrencia(string, virgula):
    clippboard = QClipboard()
    dados_brutos = string.split()
    universo = ['1111', '1112', '1121', '1122', '1211', '1212', '1221', '1222', '2222', '2221', '2212', '2211', '2122', '2121', '2112', '2111']
    if '.' in string or ',' in string:
        dados_brutos = remover_ponto_virgula(dados_brutos)
    if '/' in string:
        dados_brutos = remover_data(dados_brutos)
    valores = []

    n_resp = len(dados_brutos[0])
    if n_resp == 4:
        universo = universo4resp
    elif n_resp == 5:
        universo = universo5resp
    elif n_resp == 6:
        universo = universo6resp
    elif n_resp == 8:
        universo = universo8resp

    for uni in universo:
        contador = 0
        primeira = True
        for seq in dados_brutos:
            if not primeira:
                if uni == seq:
                    valores.append(contador)
                    contador = 0
                else:
                    contador += 1
            if primeira:
                if uni == seq:
                    primeira = False
                    contador = 0
        primeira = True
    print(valores)
    mean_value = mean(valores)
    median_value = median(valores)
    resultado = f"Média\t Mediana\r{mean_value}\t{median_value}"

    if virgula:
        resultado = resultado.replace('.', ',')
    
    try:
        clippboard.setText(resultado)
        return 'Copiado'
    except:
        return 'Falha'
