from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, \
        QHBoxLayout, QLineEdit, QComboBox, QFileDialog
from PySide2.QtGui import QFont, QColor
from PySide2.QtCore import Qt
from View.general.error_window import ErrorWindow
from Controller.s3_controller import upload_object


class NewObjectWindow(QWidget):
    def __init__(self, main_window, bucket_name):
        super().__init__()

        self.main_window = main_window
        self.bucket_name = bucket_name
        self.selected_file_path = ""

        layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()

        title_label = QLabel('New Object Menu', self)
        title_label.setAlignment(Qt.AlignCenter)
        font = QFont('Sans Serif', 30)
        font.setBold(True)
        title_label.setFont(font)
        layout.addWidget(title_label)

        back_button = QPushButton('Back to EC2', self)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        bucket_name_layout = QHBoxLayout()
        bucket_name_label = QLabel("Write your file path:")
        bucket_name_layout.addWidget(bucket_name_label)
        self.bucket_name_input_box = QLineEdit()
        bucket_name_layout.addWidget(self.bucket_name_input_box)
        layout.addLayout(bucket_name_layout)

        select_file_button = QPushButton("Select File")
        select_file_button.clicked.connect(self.select_file)
        layout.addWidget(select_file_button)

        new_object_button = QPushButton('Upload', self)
        new_object_button.clicked.connect(self.upload_button_clicked)
        button_layout.addWidget(new_object_button)

        layout.addLayout(button_layout)


    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Optional: Restrict file selection to read-only

        # Display a file dialog to select a file
        file_dialog = QFileDialog()
        self.selected_file_path, _ = file_dialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt)", options=options)


    def go_back(self):
        old_widget = self.main_window.stacked_widget.currentWidget()
        self.main_window.stacked_widget.setCurrentIndex(2)
        self.main_window.stacked_widget.removeWidget(old_widget)


    def upload_button_clicked(self):
        object_key = self.bucket_name_input_box.text()
        try:
            upload_object(self.main_window.s3_client, self.bucket_name,
                          object_key, self.selected_file_path)
        except Exception as e:
            error_window = ErrorWindow(str(e))
            error_window.exec_()
        
        self.go_back()