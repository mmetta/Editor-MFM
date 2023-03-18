from pyCore import *


class CustomDialog:
    def __init__(self, title, msg):
        super().__init__()

        self.dialog_confirm = QDialog(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.dialog_confirm.setWindowTitle(title)
        self.chosen = ''

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(msg)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.dialog_confirm.setLayout(self.layout)
        self.dialog_confirm.exec()

    def accept(self):
        self.chosen = "Success"
        self.dialog_confirm.close()

    def reject(self):
        self.chosen = "Cancel"
        self.dialog_confirm.close()
