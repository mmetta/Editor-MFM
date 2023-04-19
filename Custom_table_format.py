from PySide6.QtGui import QTextTableFormat


class CustomTableFormat(QTextTableFormat):
    def __init__(self):
        super().__init__()
        self._left_margin = 0
        self._top_margin = 0
        self._right_margin = 0
        self._bottom_margin = 0

    def setMargins(self, left: float, top: float, right: float, bottom: float):
        self.setLeftMargin(left)
        self.setTopMargin(top)
        self.setRightMargin(right)
        self.setBottomMargin(bottom)

    def margins(self):
        return self._left_margin, self._top_margin, self._right_margin, self._bottom_margin

    def setMargin(self, margin):
        self.setMargins(float(0), float(0), margin, float(0))
