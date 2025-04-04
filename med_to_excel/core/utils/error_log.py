import os
import time
import logging

from PySide6.QtWidgets import QDialog, QMessageBox


def set_errors(e):


    # dialog = QDialog()
    # dialog.setWindowTitle('Erro')
    # dialog.exec()

    msg_box = QMessageBox()
    if(e == SEQUENCE_RESPONSE_ERROR):
        msg_box.setText(SEQUENCE_RESPONSE_ERROR)
    else:
        if not os.path.exists("./erros"):
            os.mkdir("./erros")
        logging.basicConfig(filename=f'./erros/ErrorLog_{time.strftime("%d-%m-%Y-%H-%M-%S")}.log', level=logging.DEBUG)
        logging.error('Ocorreu um erro:', exc_info=True)

        msg_box.setText(f"O arquivo de log se encontra em ./erros/{time.strftime('%d-%m-%Y-%H-%M-%S')}.log")
    msg_box.exec()

SEQUENCE_RESPONSE_ERROR = "A condição do animal não condiz com a opção escolhida. Verifique a caixa de respostas individuais e tente novamente."