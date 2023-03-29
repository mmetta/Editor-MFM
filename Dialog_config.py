from pathlib import Path

from atual_path import local_path
from pyCore import *

from config_app.estilos_config import style_qpush_button
# from config_app.settings import project_settings, save_new_conf
from config_app.icon_coloring import cor_icon
from sqlite_data import select_all, update_data

base_path = Path(local_path(), './icons/light/')
# config = project_settings()
config = select_all()


class DialogConfig:

    def __init__(self):
        super().__init__()

        self.new_conf = config
        self.Changed = False
        self.dialog_config = QDialog(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.dialog_config.setWindowTitle('Configurações do App')
        self.dialog_config.setMinimumSize(320, 400)
        self.dialog_config.setMaximumSize(320, 400)
        cog_ico = Path(base_path, 'settings.svg')
        self.dialog_config.setWindowIcon(cor_icon(cog_ico))

        layV_c = QVBoxLayout(self.dialog_config)
        lbl1_c = QLabel('Escolha suas preferências')
        lbl1_c.setAlignment(Qt.AlignCenter)
        lbl1_c.setFont(QFont('Arial', 16, 700))

        lbl2_c = QLabel('Tema - esquema geral de cores:')
        lbl2_c.setFont(QFont('Arial', 10))
        theme_w = QWidget()
        theme_lay = QHBoxLayout(theme_w)
        radio_dark = QRadioButton("dark", theme_w)
        radio_light = QRadioButton("light", theme_w)
        self.theme_group = QButtonGroup(theme_w)
        self.theme_group.addButton(radio_dark)
        self.theme_group.addButton(radio_light)

        theme_lay.addWidget(radio_dark)
        theme_lay.addWidget(radio_light)
        if self.new_conf['theme'] == 'dark':
            radio_dark.setChecked(True)
        else:
            radio_light.setChecked(True)

        # CORES DE DESTAQUE
        self.li_c = config['colors_theme']

        c_pr_index = 0
        for i, c_pr in enumerate(self.li_c):
            if c_pr[0] == self.new_conf['cor_pref'][0]:
                c_pr_index = i

        lbl6_c = QLabel('Cores de destaque:')
        cor_w = QWidget()
        cor_Vlay = QVBoxLayout(cor_w)

        # primeira linha de cores
        layH_1 = QHBoxLayout()
        dk0 = QLabel(' ')
        dk0.setStyleSheet(f'background-color: {self.li_c[0][1]};')
        dk0.setMaximumWidth(20)
        lg0 = QLabel(' ')
        lg0.setStyleSheet(f'background-color: {self.li_c[0][2]};')
        lg0.setMaximumWidth(20)
        azul_Hlay = QHBoxLayout(cor_w)
        self.azul_rad = QRadioButton(f'{self.li_c[0][0]}', cor_w)
        azul_Hlay.addWidget(self.azul_rad)
        azul_Hlay.addWidget(dk0)
        azul_Hlay.addWidget(lg0)
        layH_1.addLayout(azul_Hlay)

        # Espaçador horizontal
        cor_spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        layH_1.addItem(cor_spacer)

        dk1 = QLabel(' ')
        dk1.setStyleSheet(f'background-color: {self.li_c[1][1]};')
        dk1.setMaximumWidth(20)
        lg1 = QLabel(' ')
        lg1.setStyleSheet(f'background-color: {self.li_c[1][2]};')
        lg1.setMaximumWidth(20)
        ambar_Hlay = QHBoxLayout(cor_w)
        self.ambar_rad = QRadioButton(f'{self.li_c[1][0]}', cor_w)
        ambar_Hlay.addWidget(self.ambar_rad)
        ambar_Hlay.addWidget(dk1)
        ambar_Hlay.addWidget(lg1)
        layH_1.addLayout(ambar_Hlay)

        cor_Vlay.addLayout(layH_1)

        # segunda linha de cores
        layH_2 = QHBoxLayout()
        dk2 = QLabel(' ')
        dk2.setStyleSheet(f'background-color: {self.li_c[2][1]};')
        dk2.setMaximumWidth(20)
        lg2 = QLabel(' ')
        lg2.setStyleSheet(f'background-color: {self.li_c[2][2]};')
        lg2.setMaximumWidth(20)
        verde_Hlay = QHBoxLayout(cor_w)
        self.verde_rad = QRadioButton(f'{self.li_c[2][0]}', cor_w)
        verde_Hlay.addWidget(self.verde_rad)
        verde_Hlay.addWidget(dk2)
        verde_Hlay.addWidget(lg2)
        layH_2.addLayout(verde_Hlay)

        # Espaçador horizontal
        cor_spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        layH_2.addItem(cor_spacer)

        dk3 = QLabel(' ')
        dk3.setStyleSheet(f'background-color: {self.li_c[3][1]};')
        dk3.setMaximumWidth(20)
        lg3 = QLabel(' ')
        lg3.setStyleSheet(f'background-color: {self.li_c[3][2]};')
        lg3.setMaximumWidth(20)
        pink_Hlay = QHBoxLayout(cor_w)
        self.pink_rad = QRadioButton(f'{self.li_c[3][0]}', cor_w)
        pink_Hlay.addWidget(self.pink_rad)
        pink_Hlay.addWidget(dk3)
        pink_Hlay.addWidget(lg3)
        layH_2.addLayout(pink_Hlay)

        cor_Vlay.addLayout(layH_2)

        self.cor_group = QButtonGroup(cor_w)
        self.cor_group.addButton(self.azul_rad, 0)
        self.cor_group.addButton(self.ambar_rad, 1)
        self.cor_group.addButton(self.verde_rad, 2)
        self.cor_group.addButton(self.pink_rad, 3)
        self.cor_group.button(c_pr_index).setChecked(True)

        lbl3_c = QLabel('Janela na abertura:')
        lbl3_c.setFont(QFont('Arial', 10))
        size_w = QWidget()
        size_lay = QHBoxLayout(size_w)
        self.size_max = QRadioButton("Maximizado", size_w)
        self.size_def = QRadioButton("Tamanho inicial", size_w)
        self.size_group = QButtonGroup(size_w)
        self.size_group.addButton(self.size_max)
        self.size_group.addButton(self.size_def)

        size_lay.addWidget(self.size_max)
        size_lay.addWidget(self.size_def)
        if self.new_conf['max']:
            self.size_max.setChecked(True)
        else:
            self.size_def.setChecked(True)

        lbl4_c = QLabel('Largura:')
        self.edit_w = QLineEdit()
        self.edit_w.setText(str(config['app_w']))
        self.edit_w.setValidator(QIntValidator())
        self.edit_w.setDisabled(self.size_max.isChecked())
        lbl5_c = QLabel('Altura:')
        self.edit_h = QLineEdit()
        self.edit_h.setText(str(config['app_h']))
        self.edit_h.setValidator(QIntValidator())
        self.edit_h.setDisabled(self.size_max.isChecked())
        edit_Hlay = QHBoxLayout()
        edit_Hlay.addWidget(lbl4_c)
        edit_Hlay.addWidget(self.edit_w)
        edit_Hlay.addWidget(lbl5_c)
        edit_Hlay.addWidget(self.edit_h)

        self.size_group.buttonClicked.connect(self.check_edit)

        lbl_c = QLabel('As alterações serão aplicadas\nna próxima vez que o app for aberto')
        lbl_c.setStyleSheet('font-size: 8pt; color: red')
        lbl_c.setAlignment(Qt.AlignCenter)

        btn_c_yes = QPushButton('Salvar')
        btn_c_yes.setStyleSheet(style_qpush_button())
        btn_c_yes.clicked.connect(self.config_save)

        btn_c_no = QPushButton('Cancelar')
        btn_c_no.setStyleSheet(style_qpush_button())
        btn_c_no.clicked.connect(self.config_no_save)

        layH_c = QHBoxLayout()
        layH_c.addWidget(btn_c_no)
        layH_c.addWidget(btn_c_yes)

        layV_c.addWidget(lbl1_c)
        layV_c.addWidget(lbl2_c)
        layV_c.addWidget(theme_w)

        layV_c.addWidget(lbl6_c)
        layV_c.addWidget(cor_w)

        layV_c.addWidget(lbl3_c)
        layV_c.addWidget(size_w)

        layV_c.addLayout(edit_Hlay)

        layV_c.addWidget(lbl_c)
        layV_c.addLayout(layH_c)
        self.dialog_config.exec()

    def check_edit(self):
        self.edit_w.setDisabled(self.size_max.isChecked())
        self.edit_h.setDisabled(self.size_max.isChecked())

    def config_no_save(self):
        self.new_conf = config
        self.dialog_config.close()
        self.Changed = False

    def config_save(self):
        th = self.theme_group.checkedButton()
        if self.size_max.isChecked():
            mx = 1
        else:
            mx = 0
            self.new_conf['app_w'] = int(self.edit_w.text())
            self.new_conf['app_h'] = int(self.edit_h.text())
        self.new_conf['theme'] = th.text()
        self.new_conf['max'] = mx

        cp = self.cor_group.checkedButton()
        pref = tuple()

        for tons in self.li_c:
            if tons[0] == cp.text():
                pref = tons

        self.new_conf['cor_pref'] = pref

        # save_new_conf(self.new_conf)
        update_data(self.new_conf)
        self.dialog_config.close()
        self.Changed = True
