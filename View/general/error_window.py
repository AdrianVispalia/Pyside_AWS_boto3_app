from PySide2.QtWidgets import QMessageBox


class ErrorWindow(QMessageBox):
    def __init__(self, description):
        super().__init__()

        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle("Error")
        self.setText(f"An error occurred. Error description:")
        self.setInformativeText(description)
        self.setStandardButtons(QMessageBox.Ok)