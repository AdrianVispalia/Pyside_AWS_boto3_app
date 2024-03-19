from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QWidget, \
                    QLabel, QPushButton, QStackedWidget
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt
from View.EC2.ec2_window import EC2Window
from View.S3.s3_window import S3Window


class MainWindow(QMainWindow):
    def __init__(self, session):
        super().__init__()

        self.session = session
        self.ec2_client = session.client('ec2')
        self.cloudwatch_client = session.client('cloudwatch')
        self.s3_client = session.client('s3')
        self.setWindowTitle('AWS Manager')
        self.setGeometry(100, 100, 700, 400)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(0)

        self.stacked_widget = QStackedWidget(self)
        main_page = QWidget()
        main_layout = QVBoxLayout(main_page)
        main_layout.setSpacing(0)

        title_label = QLabel('AWS Manager', self)
        title_label.setAlignment(Qt.AlignCenter)
        font = QFont('Sans Serif', 35)
        font.setBold(True)
        title_label.setFont(font)
        main_layout.addWidget(title_label)

        ec2_button = QPushButton('EC2 service', main_page)
        ec2_button.clicked.connect(self.show_ec2_page)
        main_layout.addWidget(ec2_button)

        s3_button = QPushButton('S3 service', main_page)
        s3_button.clicked.connect(self.show_s3_page)
        main_layout.addWidget(s3_button)

        self.stacked_widget.addWidget(main_page)

        layout.addWidget(self.stacked_widget)
        self.setCentralWidget(central_widget)


    def show_ec2_page(self):
        ec2_window = EC2Window(self)
        self.stacked_widget.addWidget(ec2_window)
        self.stacked_widget.setCurrentIndex(1)


    def show_s3_page(self):
        s3_window = S3Window(self)
        self.stacked_widget.addWidget(s3_window)
        self.stacked_widget.setCurrentIndex(1)