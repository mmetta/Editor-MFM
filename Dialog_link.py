from config_application.icon_coloring import cor_icon
from pyCore import *

from config_application.estilos_config import style_qpush_button, style_qline_edit


class DialogLink:

    def __init__(self, nome):
        super().__init__()

        self.dialog_link = QDialog()
        self.dialog_link.setWindowTitle('Inserir link')
        self.dialog_link.setWindowIcon(cor_icon(f"icons/light/link.svg"))
        self.dialog_link.setFixedSize(QSize(440, 120))
        self.link_nome = ''
        self.link_url = ''

        d_lay = QVBoxLayout(self.dialog_link)
        d_lay.setAlignment(Qt.AlignCenter)

        layH_2 = QHBoxLayout()
        lbl_nome = QLabel('Nome: ')
        lbl_nome.setFont(QFont('Arial', 12, 700))
        layH_2.addWidget(lbl_nome)

        disabled = False
        if nome != '':
            disabled = True
        self.edt_nome = QLineEdit(nome)
        self.edt_nome.setReadOnly(disabled)
        self.edt_nome.setFont(QFont('Arial', 10, 400))
        self.edt_nome.setMaximumWidth(340)
        self.edt_nome.setStyleSheet(style_qline_edit())
        layH_2.addWidget(self.edt_nome)

        layH_3 = QHBoxLayout()
        lbl_url = QLabel('URL: ')
        lbl_url.setFont(QFont('Arial', 12, 700))
        layH_3.addWidget(lbl_url)

        self.edt_url = QLineEdit()
        self.edt_url.setFont(QFont('Arial', 10, 400))
        self.edt_url.setMaximumWidth(340)
        self.edt_url.setStyleSheet(style_qline_edit())
        layH_3.addWidget(self.edt_url)

        layH_4 = QHBoxLayout()
        btn_inserir = QPushButton('Inserir')
        btn_inserir.setFixedSize(QSize(100, 30))
        btn_inserir.setStyleSheet(style_qpush_button())
        btn_inserir.clicked.connect(self.about_close)
        layH_4.addWidget(btn_inserir)

        d_lay.addLayout(layH_2)
        d_lay.addLayout(layH_3)
        d_lay.addLayout(layH_4)

        self.dialog_link.exec()

    def about_close(self):
        self.link_nome = self.edt_nome.text()
        self.link_url = self.edt_url.text()
        self.dialog_link.close()
