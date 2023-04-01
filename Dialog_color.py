from PySide6.QtWidgets import QApplication, QColorDialog, QLabel, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QColor


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        col = QColor(0, 0, 0)

        self.btn = QPushButton('Escolha a cor', self)
        self.btn.move(20, 20)

        self.btn.clicked.connect(self.showDialog)

        self.frm = QLabel(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())
        self.frm.setGeometry(130, 22, 100, 100)

        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Color dialog')
        self.show()

    def showDialog(self):
        dialog = QColorDialog()
        dialog.setOption(QColorDialog.ShowAlphaChannel, True)
        col = dialog.getColor()
        print(col, col.name())

        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())


if __name__ == '__main__':

    app = QApplication([])
    ex = Example()
    app.exec()
