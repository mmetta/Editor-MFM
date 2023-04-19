from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton

from atual_path import local_path

base_path = Path(local_path(), './icons')


class DialogAbout:

    def __init__(self):
        super().__init__()

        self.dialog_about = QDialog(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.dialog_about.setWindowTitle('Sobre o Aplicativo')
        ico_logo = Path(base_path, 'favicon.png')
        self.dialog_about.setWindowIcon(QIcon(QPixmap(ico_logo)))
        self.dialog_about.setMinimumSize(320, 400)
        self.dialog_about.setMaximumSize(320, 400)

        d_lay = QVBoxLayout(self.dialog_about)
        d_lay.setContentsMargins(30, 10, 30, 10)
        d_lay.setAlignment(Qt.AlignCenter)

        layH_1 = QHBoxLayout()
        lbl_logo = QLabel('Logo')
        mfm_logo = Path(base_path, 'mfm_logo.png')
        img = QPixmap(mfm_logo)
        img = img.scaledToWidth(50)
        lbl_logo.setPixmap(img)
        lbl_logo.setAlignment(Qt.AlignCenter)
        layH_1.addWidget(lbl_logo)

        layH_2 = QHBoxLayout()
        lbl_nome = QLabel('MFM Editor')
        lbl_nome.setFont(QFont('Arial', 16, 700))
        layH_2.setAlignment(Qt.AlignCenter)
        layH_2.addWidget(lbl_nome)

        layH_5 = QHBoxLayout()
        lbl_version = QLabel('versão 0.0.3')
        lbl_version.setFont(QFont('Arial', 10, 400))
        layH_5.setContentsMargins(0, 2, 0, 20)
        layH_5.setAlignment(Qt.AlignCenter)
        layH_5.addWidget(lbl_version)

        texto = '    Um editor simples, porém útil e eficaz na elaboração de documentos contendo textos' \
                ' ricos em formatação, links e imagens.\n\n    Esta versão conta com os recursos do PySide6, ' \
                'vários widgets, várias funções e classes do Python 3.11, aproveitem.\n'

        layH_3 = QHBoxLayout()
        lbl_text = QLabel(texto)
        lbl_text.setMinimumWidth(244)
        lbl_text.setFont(QFont('Arial', 10))
        lbl_text.setWordWrap(True)
        lbl_text.setAlignment(Qt.AlignJustify)
        layH_3.addWidget(lbl_text)

        lbl_ass = QLabel('Mario F Metta')
        lbl_ass.setFont(QFont('Arial', 8, 700))
        lbl_ano = QLabel('2023')
        lbl_ano.setFont(QFont('Arial', 8, 700))
        lay_ass = QHBoxLayout()
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        lay_ass.addWidget(lbl_ass)
        lay_ass.addItem(spacer)
        lay_ass.addWidget(lbl_ano)

        layH_4 = QHBoxLayout()
        layH_4.setContentsMargins(0, 20, 0, 0)
        btn_fim = QPushButton('OK')
        btn_fim.setFixedSize(36, 30)
        btn_fim.clicked.connect(self.about_close)
        layH_4.addWidget(btn_fim)

        d_lay.addLayout(layH_1)
        d_lay.addLayout(layH_2)
        d_lay.addLayout(layH_5)
        d_lay.addLayout(layH_3)
        d_lay.addLayout(lay_ass)
        d_lay.addLayout(layH_4)

        self.dialog_about.exec()

    def about_close(self):
        self.dialog_about.close()
