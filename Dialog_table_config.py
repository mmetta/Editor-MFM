from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QRadioButton, QButtonGroup, \
    QPushButton, QSpacerItem, QSizePolicy, QSpinBox

from atual_path import local_path
from icon_coloring import cor_icon

base_path = Path(local_path(), './icons/')


class DialogTableConfig:

    def __init__(self, border, border_color, conf):
        super().__init__()

        self.config = conf
        self.resp = None

        self.border = 1.0 if not border else border
        self.border_color = '#bfbfbf' if not border_color else border_color
        self.width = 393 if not conf else None
        self.align = Qt.AlignHCenter if not conf else None
        self.rows = 2 if not conf else 0
        self.cols = 3 if not conf else 0

        self.dialog_tab_config = QDialog(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.dialog_tab_config.setWindowTitle('Formatar tabela')
        self.dialog_tab_config.setMinimumSize(320, 400)
        self.dialog_tab_config.setMaximumSize(320, 400)
        cog_ico = Path(base_path, 'table.svg')
        self.dialog_tab_config.setWindowIcon(cor_icon(cog_ico))

        layV = QVBoxLayout(self.dialog_tab_config)

        lbl1 = QLabel('Largura da tabela:')
        lbl1.setFont(QFont('Arial', 10, 700))
        self.wid_tab = QWidget()
        wid_lay = QHBoxLayout(self.wid_tab)
        self.radio_100 = QRadioButton("100%", self.wid_tab)
        self.radio_100.toggled.connect(self.disable_align)
        self.radio_100.setChecked(True if self.width == 630 else False)
        radio_50 = QRadioButton("50%", self.wid_tab)
        radio_50.setChecked(True if self.width == 393 else False)
        radio_25 = QRadioButton("25%", self.wid_tab)
        radio_25.setChecked(True if self.width == 236 else False)
        self.wid_group = QButtonGroup(self.wid_tab)
        self.wid_group.addButton(self.radio_100)
        self.wid_group.addButton(radio_50)
        self.wid_group.addButton(radio_25)

        wid_lay.addWidget(self.radio_100)
        wid_lay.addWidget(radio_50)
        wid_lay.addWidget(radio_25)

        lbl2 = QLabel('Alinhamento:')
        lbl2.setFont(QFont('Arial', 10, 700))
        self.alg_tab = QWidget()
        self.alg_tab.setEnabled(False if conf else True)
        alg_lay = QHBoxLayout(self.alg_tab)
        radio_left = QRadioButton("Esquerdo", self.alg_tab)
        radio_left.setChecked(True if self.align == Qt.AlignLeft else False)
        radio_center = QRadioButton("Centro", self.alg_tab)
        radio_center.setChecked(True if self.align == Qt.AlignHCenter else False)
        radio_right = QRadioButton("Direito", self.alg_tab)
        radio_right.setChecked(True if self.align == Qt.AlignRight else False)
        self.alg_group = QButtonGroup(self.alg_tab)
        self.alg_group.addButton(radio_left)
        self.alg_group.addButton(radio_center)
        self.alg_group.addButton(radio_right)
        alg_lay.addWidget(radio_left)
        alg_lay.addWidget(radio_center)
        alg_lay.addWidget(radio_right)

        lbl3 = QLabel('Grade:')
        lbl3.setFont(QFont('Arial', 10, 700))
        self.grd_tab = QWidget()
        grd_lay = QHBoxLayout(self.grd_tab)
        lbl4 = QLabel('Linhas:')
        lbl4.setFont(QFont('Arial', 10, 400))
        self.grd_rows = QSpinBox()
        self.grd_rows.setMinimum(1)
        self.grd_rows.setMaximum(100)
        self.grd_rows.setValue(self.rows)
        lbl5 = QLabel('Colunas:')
        lbl5.setFont(QFont('Arial', 10, 400))
        self.grd_cols = QSpinBox()
        self.grd_cols.setMinimum(1)
        self.grd_cols.setMaximum(30)
        self.grd_cols.setValue(self.cols)
        grd_lay.addWidget(lbl4)
        grd_lay.addWidget(self.grd_rows)
        grd_lay.addWidget(lbl5)
        grd_lay.addWidget(self.grd_cols)

        lbl6 = QLabel('Espessura das bordas:')
        lbl6.setFont(QFont('Arial', 10, 700))
        esp_tab = QWidget()
        esp_lay = QHBoxLayout(esp_tab)
        radio_one = QRadioButton("1 px", esp_tab)
        radio_one.setChecked(True if self.border == 1 else False)
        radio_two = QRadioButton("2 px", esp_tab)
        radio_two.setChecked(True if self.border == 2 else False)
        self.radio_none = QRadioButton("sem borda", esp_tab)
        self.radio_none.toggled.connect(self.disable_color)
        self.radio_none.setChecked(True if self.border == 0 else False)
        self.esp_group = QButtonGroup(esp_tab)
        self.esp_group.addButton(radio_one)
        self.esp_group.addButton(radio_two)
        self.esp_group.addButton(self.radio_none)
        esp_lay.addWidget(radio_one)
        esp_lay.addWidget(radio_two)
        esp_lay.addWidget(self.radio_none)

        lbl7 = QLabel('Cor das bordas:')
        lbl7.setFont(QFont('Arial', 10, 700))
        self.cor_tab = QWidget()
        cor_lay = QHBoxLayout(self.cor_tab)
        cor0 = QLabel(' ')
        cor0.setStyleSheet('background-color: #000000;')
        cor0.setMaximumWidth(20)
        cor1 = QLabel(' ')
        cor1.setStyleSheet('background-color: #bfbfbf;')
        cor1.setMaximumWidth(20)
        cor2 = QLabel(' ')
        cor2.setStyleSheet('background-color: #ff0000;')
        cor2.setMaximumWidth(20)

        radio_black = QRadioButton(None, lbl7)
        radio_black.setChecked(True if self.border_color == '#000000' else False)
        radio_grey = QRadioButton(None, lbl7)
        radio_grey.setChecked(True if self.border_color == '#bfbfbf' else False)
        radio_red = QRadioButton(None, lbl7)
        radio_red.setChecked(True if self.border_color == '#ff0000' else False)
        self.cor_group = QButtonGroup(lbl7)
        self.cor_group.addButton(radio_black)
        self.cor_group.addButton(radio_grey)
        self.cor_group.addButton(radio_red)

        cor_lay.addWidget(cor0)
        cor_lay.addWidget(radio_black)
        cor_lay.addWidget(cor1)
        cor_lay.addWidget(radio_grey)
        cor_lay.addWidget(cor2)
        cor_lay.addWidget(radio_red)

        # Espaçador horizontal
        tab_spacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Minimum)
        btn_lay = QHBoxLayout()
        btn_no = QPushButton('Cancelar')
        btn_no.clicked.connect(self.dialog_cancel)
        btn_yes = QPushButton('Ok')
        btn_yes.clicked.connect(self.set_tab)
        btn_lay.addWidget(btn_no)
        btn_lay.addWidget(btn_yes)

        layV.addWidget(lbl1)
        layV.addWidget(self.wid_tab)
        layV.addWidget(lbl2)
        layV.addWidget(self.alg_tab)
        layV.addWidget(lbl3)
        layV.addWidget(self.grd_tab)
        layV.addWidget(lbl6)
        layV.addWidget(esp_tab)
        layV.addWidget(lbl7)
        layV.addWidget(self.cor_tab)

        layV.addItem(tab_spacer)
        layV.addLayout(btn_lay)

        if self.config:
            self.disable_all()

        self.dialog_tab_config.exec()

    def dialog_cancel(self):
        self.dialog_tab_config.close()

    def disable_align(self):
        size = self.radio_100.isChecked()
        for button in self.alg_group.buttons():
            button.setEnabled(not size)
        bg = '#dddddd' if size else 'transparent'
        self.alg_tab.setStyleSheet(f"background-color: {bg};")

    def disable_all(self):
        self.wid_tab.setEnabled(False)
        self.wid_tab.setStyleSheet(f"background-color: '#dddddd';")
        self.alg_tab.setEnabled(False)
        self.alg_tab.setStyleSheet(f"background-color: '#dddddd';")
        self.grd_rows.setEnabled(False)
        self.grd_cols.setEnabled(False)
        self.grd_tab.setStyleSheet(f"background-color: '#dddddd';")

    def disable_color(self):
        no_border = self.radio_none.isChecked()
        for button in self.cor_group.buttons():
            button.setEnabled(not no_border)
        bg = '#dddddd' if no_border else 'transparent'
        self.cor_tab.setStyleSheet(f"background-color: {bg};")

    def set_tab(self):
        self.resp = 'success'
        btn_e = self.esp_group.checkedButton().text()
        if btn_e == '1 px':
            self.border = 1
        if btn_e == '2 px':
            self.border = 2
        if btn_e == 'sem borda':
            self.border = 0

        cor = self.cor_group.checkedId()
        if cor == -2:
            self.border_color = QColor('#000000')
        if cor == -3:
            self.border_color = QColor('#bfbfbf')
        if cor == -4:
            self.border_color = QColor('#ff0000')

        if self.config:
            self.dialog_tab_config.close()

        else:
            btn_w = self.wid_group.checkedButton().text()
            if btn_w == '100%':
                self.width = 630
            if btn_w == '50%':
                self.width = 393
            if btn_w == '25%':
                self.width = 236

            btn_a = self.alg_group.checkedButton().text()
            if btn_a == 'Esquerdo':
                self.align = Qt.AlignLeft
            if btn_a == 'Centro':
                self.align = Qt.AlignHCenter
            if btn_a == 'Direito':
                self.align = Qt.AlignRight

            self.rows = int(self.grd_rows.text())
            self.cols = int(self.grd_cols.text())

            self.dialog_tab_config.close()
