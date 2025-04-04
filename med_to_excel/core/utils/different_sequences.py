from PySide6.QtGui import QClipboard
from med_to_excel.core.utils.recorrence import remover_ponto_virgula, remover_data, remover_zeros


def calcular_NSeq(string):
    cb = QClipboard()
    dados_brutos = string.split()
    if '.' in string or ',' in string:
        dados_brutos = remover_ponto_virgula(dados_brutos)
    if '/' in string:
        dados_brutos = remover_data(dados_brutos)
    if '0' in dados_brutos:
        dados_brutos = remover_zeros(dados_brutos)
    conjunto = set(dados_brutos)
        
    try:
        cb.setText(str(len(conjunto)))
        return 'Copiado'
    except:
        return 'Falha'