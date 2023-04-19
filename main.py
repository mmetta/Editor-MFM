import sys
from pathlib import Path

from PySide6.QtCore import Qt, QCoreApplication, QProcess
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QCursor, QIcon

import qdarktheme

from Dialog_config import DialogConfig
from Dialog_Confirm import CustomDialog
from Editor import Editor
from atual_path import local_path
from sqlite_data import select_all

base_path = Path(local_path(), './icons')
config = select_all()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Editor 0.0.3')
        self.setMinimumSize(config['app_w'], config['app_h'])

        self.text_edit = Editor()
        self.setCentralWidget(self.text_edit)

        self.text_edit.edit_title.connect(self.set_title)
        self.text_edit.get_config.connect(self.set_config)
        self.text_edit.show_minimized.connect(self.showMinimized)
        self.text_edit.show_maximized.connect(self.showMaximized)
        self.text_edit.show_full_screen.connect(self.showFullScreen)
        self.text_edit.show_normal.connect(self.showNormal)
        self.closeEvent = self.text_edit.closeEvent

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

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            widget = app.widgetAt(QCursor.pos())
            print(widget)


def restart_program():
    QCoreApplication.quit()
    status = QProcess.startDetached(sys.executable, sys.argv)
    print(status)


fav = str(Path(base_path, 'favicon.ico'))
theme = config['theme']
primary_color = config['cor_pref'][2]

if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon(fav))
    qdarktheme.setup_theme(theme, custom_colors={"primary": primary_color})
    window = MainWindow()
    window.show()
    app.exec()
