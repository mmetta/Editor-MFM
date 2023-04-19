from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QSpinBox


class ResizeDialog:
    def __init__(self, w, h):
        super().__init__()

        self.dialog_resize = QDialog(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.dialog_resize.setWindowTitle('Redimensionar Imagem')
        self.res = ()
        self.w = w
        self.h = h

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        layH = QHBoxLayout()
        layVw = QVBoxLayout()
        layVh = QVBoxLayout()
        lbl_w = QLabel('Largura')
        lbl_h = QLabel('Altura')

        self.check_prop = QCheckBox()
        self.check_prop.setText('Manter proporção')
        self.check_prop.setChecked(True)

        self.img_w = QSpinBox()
        self.img_w.setMaximum(1000)
        self.img_w.setValue(w)
        self.img_w.valueChanged.connect(self.proportion_w)

        self.img_h = QSpinBox()
        self.img_h.setMaximum(1000)
        self.img_h.setValue(h)
        self.img_h.valueChanged.connect(self.proportion_h)

        layVw.addWidget(lbl_w)
        layVw.addWidget(self.img_w)

        layVh.addWidget(lbl_h)
        layVh.addWidget(self.img_h)

        layH.addLayout(layVw)
        layH.addLayout(layVh)

        self.layout.addLayout(layH)
        self.layout.addWidget(self.check_prop)
        self.layout.addWidget(self.buttonBox)
        self.dialog_resize.setLayout(self.layout)
        self.dialog_resize.exec()

    def proportion_w(self):
        if self.check_prop.isChecked():
            w1 = self.w
            h1 = self.h
            w2 = self.img_w.text()
            if int(w2) > 0:
                h2 = float(w2) * float(h1) / float(w1)
                self.img_h.setValue(int(h2))

    def proportion_h(self):
        if self.check_prop.isChecked():
            w1 = self.w
            h1 = self.h
            h2 = self.img_h.text()
            if int(h2) > 0:
                w2 = float(w1) * float(h2) / float(h1)
                self.img_w.setValue(int(w2))

    def accept(self):
        self.dialog_resize.close()
        self.res = self.img_w.text(), self.img_h.text()

    def reject(self):
        self.dialog_resize.close()
