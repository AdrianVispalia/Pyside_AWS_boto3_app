from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, \
        QHBoxLayout, QListWidget, QListWidgetItem, QFileDialog
from PySide2.QtGui import QFont, QColor
from PySide2.QtCore import Qt
from Controller.s3_controller import get_bucket_objects, delete_object
from View.S3.new_object_window import NewObjectWindow


class BucketWindow(QWidget):
    def __init__(self, main_window, bucket_name):
        super().__init__()

        self.main_window = main_window
        self.bucket_name = bucket_name

        layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()

        title_label = QLabel('Bucket Menu', self)
        title_label.setAlignment(Qt.AlignCenter)
        font = QFont('Sans Serif', 30)
        font.setBold(True)
        title_label.setFont(font)
        layout.addWidget(title_label)

        subtitle_label = QLabel(self.bucket_name, self)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont('Sans Serif', 18))
        layout.addWidget(subtitle_label)

        back_button = QPushButton('Back to S3', self)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        self.object_list_widget = QListWidget(self)
        self.object_list_widget.setStyleSheet(
            "QListWidget:item {selection-background-color: #C8C8C8;}")

        layout.addWidget(self.object_list_widget)

        update_button = QPushButton('Update', self)
        update_button.clicked.connect(self.update_object_list)
        button_layout.addWidget(update_button)

        upload_button = QPushButton('Upload object', self)
        upload_button.clicked.connect(self.new_object_button_clicked)
        button_layout.addWidget(upload_button)

        layout.addLayout(button_layout)


    def update_object_list(self):
        self.object_list_widget.clear()
        items = get_bucket_objects(self.main_window.s3_client, self.bucket_name)
        for index, item in enumerate(items):
            list_item = QListWidgetItem()
            list_item.setBackground( \
                    QColor(240, 240, 240) if index % 2 == 0 \
                    else QColor(220, 220, 220))
            item_container = QWidget()
            item_layout = QHBoxLayout(item_container)

            id_label = QLabel(item.id, item_container)
            item_layout.addWidget(id_label)

            size_label = QLabel(str(item.size), item_container)
            item_layout.addWidget(size_label)

            delete_button = QPushButton('Delete', item_container)
            delete_button.setProperty('object_id', item.id)
            delete_button.clicked.connect(self.delete_object_button_clicked)
            delete_button.setToolTip("Delete " + item.id)
            item_layout.addWidget(delete_button)

            list_item.setSizeHint(item_container.sizeHint())
            self.object_list_widget.addItem(list_item)
            self.object_list_widget.setItemWidget(list_item, item_container)


    def delete_object_button_clicked(self):
        delete_object(
            self.main_window.s3_client,
            self.bucket_name,
            self.sender().property('object_id')
        )


    def new_object_button_clicked(self):
        new_bucket_window = NewObjectWindow(self.main_window, self.bucket_name)
        self.main_window.stacked_widget.addWidget(new_bucket_window)
        self.main_window.stacked_widget.setCurrentIndex(3)


    def go_back(self):
        old_widget = self.main_window.stacked_widget.currentWidget()
        self.main_window.stacked_widget.setCurrentIndex(2)
        self.main_window.stacked_widget.removeWidget(old_widget)
