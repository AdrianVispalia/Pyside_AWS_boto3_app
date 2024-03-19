from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, \
        QHBoxLayout, QListWidget, QListWidgetItem, QComboBox
from PySide2.QtGui import QFont, QColor
from PySide2.QtCore import Qt
from View.S3.bucket_window import BucketWindow
from View.S3.new_bucket_window import NewBucketWindow
from Controller.s3_controller import get_buckets, delete_bucket


class S3Window(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()

        title_label = QLabel('S3 Menu', self)
        title_label.setAlignment(Qt.AlignCenter)
        font = QFont('Sans Serif', 30)
        font.setBold(True)
        title_label.setFont(font)
        layout.addWidget(title_label)

        back_button = QPushButton('Back to Main', self)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        self.bucket_list_widget = QListWidget(self)
        self.bucket_list_widget.setStyleSheet(
            "QListWidget:item {selection-background-color: #C8C8C8;}")

        layout.addWidget(self.bucket_list_widget)

        update_button = QPushButton('Update', self)
        update_button.clicked.connect(self.update_bucket_list)
        button_layout.addWidget(update_button)

        new_bucket_button = QPushButton('New bucket', self)
        new_bucket_button.clicked.connect(self.new_bucket_button_clicked)
        button_layout.addWidget(new_bucket_button)

        layout.addLayout(button_layout)

        self.update_bucket_list()


    def go_back(self):
        old_widget = self.main_window.stacked_widget.currentWidget()
        self.main_window.stacked_widget.setCurrentIndex(1)
        self.main_window.stacked_widget.removeWidget(old_widget)


    def update_bucket_list(self):
        self.bucket_list_widget.clear()
        items = get_buckets(self.main_window.s3_client)
        for index, item in enumerate(items):
            list_item = QListWidgetItem()
            list_item.setBackground( \
                    QColor(240, 240, 240) if index % 2 == 0 \
                    else QColor(220, 220, 220))
            item_container = QWidget()
            item_layout = QHBoxLayout(item_container)

            label = QLabel(item.id, item_container)
            item_layout.addWidget(label)

            modify_button = QPushButton('Modify', item_container)
            modify_button.setProperty('bucket_id', item.id)
            modify_button.clicked.connect(self.modify_bucket_button_clicked)
            modify_button.setToolTip("Modify " + item.id)
            item_layout.addWidget(modify_button)

            delete_button = QPushButton('Delete', item_container)
            delete_button.setProperty('bucket_id', item.id)
            delete_button.clicked.connect(self.delete_bucket_button_clicked)
            delete_button.setToolTip("Delete " + item.id)
            item_layout.addWidget(delete_button)

            list_item.setSizeHint(item_container.sizeHint())
            self.bucket_list_widget.addItem(list_item)
            self.bucket_list_widget.setItemWidget(list_item, item_container)


    def delete_bucket_button_clicked(self):
        print(self.sender().property('bucket_id'))
        delete_bucket(self.sender().property('bucket_id'), self.main_window.s3_client)


    def modify_bucket_button_clicked(self):
        print("Bucket id:")
        print(str(self.sender().property('bucket_id')))
        print(self.sender())
        bucket_window = BucketWindow(
            self.main_window,
            str(self.sender().property('bucket_id'))
        )
        self.main_window.stacked_widget.addWidget(bucket_window)
        self.main_window.stacked_widget.setCurrentIndex(2)


    def new_bucket_button_clicked(self):
        new_bucket_window = NewBucketWindow(self.main_window)
        self.main_window.stacked_widget.addWidget(new_bucket_window)
        self.main_window.stacked_widget.setCurrentIndex(2)