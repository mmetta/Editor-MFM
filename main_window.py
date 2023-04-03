import os
from pathlib import Path
from PySide6.QtWidgets import QFrame, QHBoxLayout

from qdarkstyle.dark.palette import DarkPalette
from qdarkstyle.light.palette import LightPalette

from atual_path import local_path
from editor_html import EditorHtml
from sqlite_data import select_all, create_db

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


class MainWindow(object):
    def __init__(self, *args, **kwargs):
        self.editor = EditorHtml(*args, **kwargs)
        self.main_layout = None
        self.central_frame = None

    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName('MainWindow')

        parent.setMinimumSize(config['app_w'], config['app_h'])
        if config['max']:
            parent.showMaximized()

        self.editor.show_minimized.connect(parent.showMinimized)
        self.editor.show_maximized.connect(parent.showMaximized)
        self.editor.show_full_screen.connect(parent.showFullScreen)
        self.editor.show_normal.connect(parent.showNormal)

        self.th_cores = []
        self.central_frame = QFrame()

        self.main_layout = QHBoxLayout(self.central_frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addWidget(self.editor)

        parent.setCentralWidget(self.central_frame)
