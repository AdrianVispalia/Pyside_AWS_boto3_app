from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, \
        QHBoxLayout, QLineEdit, QComboBox
from PySide2.QtGui import QFont, QColor
from PySide2.QtCore import Qt
from View.general.error_window import ErrorWindow
from Controller.ec2_controller import get_ec2_regions, run_ec2_instance, \
        find_ubuntu_ami, get_key_pairs, get_security_groups, get_subnets



class NewEC2Window(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()

        title_label = QLabel('New EC2 Menu', self)
        title_label.setAlignment(Qt.AlignCenter)
        font = QFont('Sans Serif', 30)
        font.setBold(True)
        title_label.setFont(font)
        layout.addWidget(title_label)

        back_button = QPushButton('Back to EC2', self)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        region_selection_layout = QHBoxLayout()
        self.region_selection_label = QLabel("Select region:")
        region_selection_layout.addWidget(self.region_selection_label)
        self.region_selection_input = QComboBox()
        self.region_selection_input.addItems(get_ec2_regions(self.main_window.session))
        self.region_selection_input.currentTextChanged.connect(self.region_changed)
        region_selection_layout.addWidget(self.region_selection_input)
        layout.addLayout(region_selection_layout)

        instance_selection_layout = QHBoxLayout()
        self.instance_selection_label = QLabel("Select size:")
        instance_selection_layout.addWidget(self.instance_selection_label)
        self.instance_selection_input = QComboBox()
        self.instance_selection_input.addItems(["t3.micro", "t3.small"])
        instance_selection_layout.addWidget(self.instance_selection_input)
        layout.addLayout(instance_selection_layout)

        key_selection_layout = QHBoxLayout()
        self.key_selection_label = QLabel("Select key pair:")
        key_selection_layout.addWidget(self.key_selection_label)
        self.key_selection_input = QComboBox()
        self.key_selection_input.addItems(
            get_key_pairs(self.main_window.session,
            self.region_selection_input.currentText())
        )
        key_selection_layout.addWidget(self.key_selection_input)
        layout.addLayout(key_selection_layout)

        sg_selection_layout = QHBoxLayout()
        self.sg_selection_label = QLabel("Select security group:")
        sg_selection_layout.addWidget(self.sg_selection_label)
        self.sg_selection_input = QComboBox()
        self.sg_selection_input.addItems(
            get_security_groups(self.main_window.session,
                self.region_selection_input.currentText())
        )
        sg_selection_layout.addWidget(self.sg_selection_input)
        layout.addLayout(sg_selection_layout)

        subnet_selection_layout = QHBoxLayout()
        self.subnet_selection_label = QLabel("Select subnet:")
        subnet_selection_layout.addWidget(self.subnet_selection_label)
        self.subnet_selection_input = QComboBox()
        self.subnet_selection_input.addItems(
            get_subnets(self.main_window.session,
                self.region_selection_input.currentText())
        )
        subnet_selection_layout.addWidget(self.subnet_selection_input)
        layout.addLayout(subnet_selection_layout)

        new_ec2_button = QPushButton('Create', self)
        new_ec2_button.clicked.connect(self.create_button_clicked)
        button_layout.addWidget(new_ec2_button)

        layout.addLayout(button_layout)


    def go_back(self):
        old_widget = self.main_window.stacked_widget.currentWidget()
        self.main_window.stacked_widget.setCurrentIndex(1)
        self.main_window.stacked_widget.removeWidget(old_widget)


    def create_button_clicked(self):
        instance_type = self.instance_selection_input.currentText()
        region = self.region_selection_input.currentText()
        image_id = find_ubuntu_ami(self.main_window.session, region)
        key_name = self.key_selection_input.currentText()
        security_group_ids = [self.sg_selection_input.currentText()]
        subnet_id = self.subnet_selection_input.currentText()

        print("AMI: ")
        print(image_id)

        try:
            run_ec2_instance(self.main_window.session, image_id, instance_type,
                             key_name, security_group_ids, subnet_id, 1, 1, region)
        except Exception as e:
            error_window = ErrorWindow(str(e))
            error_window.exec_()
        
        self.go_back()
    

    def region_changed(self):
        print("New region")
        print(self.region_selection_input.currentText())
        self.key_selection_input.clear()
        self.key_selection_input.addItems(
            get_key_pairs(self.main_window.session,
            self.region_selection_input.currentText())
        )
        self.sg_selection_input.clear()
        self.sg_selection_input.addItems(
            get_security_groups(self.main_window.session,
                self.region_selection_input.currentText())
        )
        self.subnet_selection_input.clear()
        self.subnet_selection_input.addItems(
            get_subnets(self.main_window.session,
                self.region_selection_input.currentText())
        )