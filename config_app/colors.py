from pyCore import *


class ColorAction(QWidgetAction):
    colorSelected = Qt.pyqtSignal(QColor)

    def __init__(self, parent):
        QWidgetAction.__init__(self, parent)
        widget = QWidget(parent)
        layout = QGridLayout(widget)
        layout.setSpacing(0)
        layout.setContentsMargins(2, 2, 2, 2)
        palette = self.palette()
        count = len(palette)
        rows = count // round(count ** .5)
        for row in range(rows):
            for column in range(count // rows):
                color = palette.pop()
                button = QToolButton(widget)
                button.setAutoRaise(True)
                button.clicked[()].connect(
                    lambda color=color: self.handleButton(color))
                pixmap = QPixmap(16, 16)
                pixmap.fill(color)
                button.setIcon(QIcon(pixmap))
                layout.addWidget(button, row, column)
        self.setDefaultWidget(widget)

    def handleButton(self, color):
        self.parent().hide()
        self.colorSelected.emit(color)

    def palette(self):
        palette = []
        for g in range(4):
            for r in range(4):
                for b in range(3):
                    palette.append(QColor(
                        r * 255 // 3, g * 255 // 3, b * 255 // 2))
        return palette


class ColorMenu(QMenu):
    def __init__(self, parent):
        QMenu.__init__(self, parent)
        self.colorAction = ColorAction(self)
        self.colorAction.colorSelected.connect(self.handleColorSelected)
        self.addAction(self.colorAction)
        self.addSeparator()
        self.addAction('Custom Color...')

    def handleColorSelected(self, color):
        print(color.name())
