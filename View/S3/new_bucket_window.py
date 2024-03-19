from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, \
        QHBoxLayout, QLineEdit, QComboBox
from PySide2.QtGui import QFont, QColor
from PySide2.QtCore import Qt
from View.general.error_window import ErrorWindow
from Controller.s3_controller import get_available_regions, create_bucket


class NewBucketWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()

        title_label = QLabel('New Bucket Menu', self)
        title_label.setAlignment(Qt.AlignCenter)
        font = QFont('Sans Serif', 30)
        font.setBold(True)
        title_label.setFont(font)
        layout.addWidget(title_label)

        back_button = QPushButton('Back to EC2', self)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        bucket_name_layout = QHBoxLayout()
        bucket_name_label = QLabel("Write your bucket name:")
        bucket_name_layout.addWidget(bucket_name_label)
        self.bucket_name_input_box = QLineEdit()
        bucket_name_layout.addWidget(self.bucket_name_input_box)
        layout.addLayout(bucket_name_layout)

        region_selection_layout = QHBoxLayout()
        self.region_selection_label = QLabel("Select region:")
        region_selection_layout.addWidget(self.region_selection_label)
        self.region_selection_input = QComboBox()
        self.region_selection_input.addItems(get_available_regions())
        self.region_selection_input.setCurrentText(self.main_window.s3_client.meta.region_name)
        region_selection_layout.addWidget(self.region_selection_input)
        layout.addLayout(region_selection_layout)

        new_bucket_button = QPushButton('Create', self)
        new_bucket_button.clicked.connect(self.create_button_clicked)
        button_layout.addWidget(new_bucket_button)

        layout.addLayout(button_layout)


    def go_back(self):
        old_widget = self.main_window.stacked_widget.currentWidget()
        self.main_window.stacked_widget.setCurrentIndex(1)
        self.main_window.stacked_widget.removeWidget(old_widget)


    def create_button_clicked(self):
        self.main_window.s3_client = self.main_window.session.client(
            's3',
            region_name=self.region_selection_input.currentText()
        )
        name = self.bucket_name_input_box.text()
        try:
            create_bucket(self.main_window.s3_client, name,
                          self.main_window.s3_client.meta.region_name)
        except Exception as e:
            error_window = ErrorWindow(str(e))
            error_window.exec_()

        self.go_back()
