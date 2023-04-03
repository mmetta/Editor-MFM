import os
import sys
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QProcess
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication

import qdarkstyle
from qdarkstyle.dark.palette import DarkPalette
from qdarkstyle.light.palette import LightPalette

from Dialog_config import DialogConfig
from Dialog_Confirm import CustomDialog
from atual_path import local_path
from main_window import MainWindow
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
    def __init__(self):
        super().__init__()

        self.main_ui = MainWindow()
        self.main_ui.setup_ui(self)
        # window title
        self.title = self.main_ui.editor.title
        self.setWindowTitle(self.title)
        self.main_ui.editor.get_config.connect(self.set_config)
        self.main_ui.editor.edit_title.connect(self.set_title)
        self.closeEvent = self.main_ui.editor.fechar

        self.show()

    def set_title(self, title):
        self.setWindowTitle(title)

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
