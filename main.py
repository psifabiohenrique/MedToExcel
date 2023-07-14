from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
import sys
from qdarktheme import load_stylesheet

from MainWindow import MainWindow


app = QApplication(sys.argv)
app.setStyleSheet(load_stylesheet('dark'))
app.setWindowIcon(QIcon("icone.png"))
window = MainWindow()
window.show()


app.exec()
