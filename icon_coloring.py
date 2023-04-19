import os

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QColor, QPixmap, QPainter, QIcon
from sqlite_data import select_all, create_db

appData = os.getenv('APPDATA') + '\\EditorMFM'
db_dir = os.path.isdir(appData)
if not db_dir:
    os.makedirs(os.path.join(os.environ['APPDATA'], 'EditorMFM'))
    create_db()

config = select_all()


def cor_icon(path):
    th_cor = config['cor_pref'][2]
    ico_cor = QColor(th_cor)
    pixmap = QPixmap(path)
    rect = QRect(1, 1, 18, 18)

    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)

    painter.setPen(Qt.NoPen)
    painter.fillRect(rect, ico_cor)

    painter.drawPixmap(16, 16, pixmap)
    painter.end()

    return QIcon(pixmap)
