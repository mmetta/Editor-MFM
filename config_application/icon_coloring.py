from pyCore import *

from config_application.settings import project_settings

config = project_settings()


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
