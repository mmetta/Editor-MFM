import os
import sys
from pathlib import Path

from Dialog_Confirm import CustomDialog
from Dialog_config import DialogConfig
from atual_path import local_path
from pyCore import *

import qdarkstyle
from qdarkstyle.dark.palette import DarkPalette
from qdarkstyle.light.palette import LightPalette

from py_editor import EditorHtml
from sqlite_data import create_db, select_all

appData = os.getenv('APPDATA') + '\\EditorMFM'
db_dir = os.path.isdir(appData)
if not db_dir:
    os.makedirs(os.path.join(os.environ['APPDATA'], 'EditorMFM'))
    create_db()

base_path = Path(local_path(), './icons')
config = select_all()

if config['theme'] == 'dark':
    tema = DarkPalette
else:
    tema = LightPalette


class MainApp(QMainWindow):

    def __init__(self, parent=None):
        self.editor = EditorHtml()
        self.main_layout = None
        self.central_frame = None
        super(MainApp, self).__init__(parent)

        self.main_layout = self.editor.lay_v
        self.closeEvent = self.editor.fechar

        # window title
        self.title = self.editor.title
        self.setWindowTitle(self.title)
        self.setMinimumSize(config['app_w'], config['app_h'])
        if config['max']:
            self.showMaximized()
        self.th_cores = []

        self.central_frame = QFrame()

        self.main_layout = QHBoxLayout(self.central_frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addWidget(self.editor)

        self.setCentralWidget(self.central_frame)

        self.editor.get_config.connect(self.set_config)

    # #################################
    # ####  RESTART AFTER CONFIG   ####
    # #################################
    def set_config(self):
        conf = DialogConfig()
        if conf.Changed:
            re_st = CustomDialog('Reinicializar?', 'Deseja reinicializar o aplicativo agora?')
            if re_st.chosen == 'Success':
                restart_program()

def restart_program():
    QCoreApplication.quit()
    status = QProcess.startDetached(sys.executable, sys.argv)


fav = str(Path(base_path, 'favicon.ico'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(fav))
    app.setStyleSheet(qdarkstyle.load_stylesheet(tema))
    window = MainApp()
    window.show()
    sys.exit(app.exec())
