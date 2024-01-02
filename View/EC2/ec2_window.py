from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, \
        QHBoxLayout, QListWidget, QListWidgetItem, QComboBox
from PySide2.QtGui import QFont, QColor
from PySide2.QtCore import Qt
from View.EC2.new_ec2_window import NewEC2Window
from View.EC2.ec2_stats_window import EC2StatsWindow
from Model.ec2_model import EC2Model
from Controller.ec2_controller import get_ec2_regions, get_ec2_instances, stop_ec2_instance


class EC2Window(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()

        title_label = QLabel('EC2 Menu', self)
        title_label.setAlignment(Qt.AlignCenter)
        font = QFont('Sans Serif', 30)
        font.setBold(True)
        title_label.setFont(font)
        layout.addWidget(title_label)

        back_button = QPushButton('Back to Main', self)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        region_selection_layout = QHBoxLayout()
        self.region_selection_label = QLabel("Select region:")
        region_selection_layout.addWidget(self.region_selection_label)
        self.region_selection_input = QComboBox()
        self.region_selection_input.addItems(get_ec2_regions(self.main_window.session))
        self.region_selection_input.currentTextChanged.connect(self.update_ec2_list)
        region_selection_layout.addWidget(self.region_selection_input)
        layout.addLayout(region_selection_layout)

        self.ec2_list_widget = QListWidget(self)
        self.ec2_list_widget.setStyleSheet("QListWidget:item {selection-background-color: #C8C8C8;}")
        
        layout.addWidget(self.ec2_list_widget)

        update_button = QPushButton('Update', self)
        update_button.clicked.connect(self.update_ec2_list)
        button_layout.addWidget(update_button)

        new_ec2_button = QPushButton('New EC2', self)
        new_ec2_button.clicked.connect(self.new_ec2_button_clicked)
        button_layout.addWidget(new_ec2_button)

        layout.addLayout(button_layout)

        self.update_ec2_list()


    def go_back(self):
        old_widget = self.main_window.stacked_widget.currentWidget()
        self.main_window.stacked_widget.setCurrentIndex(1)
        self.main_window.stacked_widget.removeWidget(old_widget)


    def update_ec2_list(self):
        self.ec2_list_widget.clear()
        items = get_ec2_instances(
            self.main_window.session,
            self.region_selection_input.currentText()
        )

        for index, item in enumerate(items):
            list_item = QListWidgetItem()
            list_item.setBackground( \
                    QColor(240, 240, 240) if index % 2 == 0 \
                    else QColor(220, 220, 220))
            item_container = QWidget()
            item_layout = QHBoxLayout(item_container)

            id_label = QLabel(item.id, item_container)
            item_layout.addWidget(id_label)

            state_label = QLabel(item.state, item_container)
            item_layout.addWidget(state_label)

            stats_button = QPushButton('Stats', item_container)
            stats_button.setProperty('ec2_id', item.id)
            stats_button.clicked.connect(self.stats_ec2_button_clicked)
            stats_button.setToolTip("Stats of " + item.id)
            item_layout.addWidget(stats_button)

            if item.state == "running":
                stop_button = QPushButton('Stop', item_container)
                stop_button.setProperty('ec2_id', item.id)
                stop_button.clicked.connect(self.stop_ec2_button_clicked)
                stop_button.setToolTip("Stop " + item.id)
                item_layout.addWidget(stop_button)
            else:
                replace_label = QLabel("", item_container)
                item_layout.addWidget(replace_label)

            list_item.setSizeHint(item_container.sizeHint())
            self.ec2_list_widget.addItem(list_item)
            self.ec2_list_widget.setItemWidget(list_item, item_container)


    def new_ec2_button_clicked(self):
        new_ec2_window = NewEC2Window(self.main_window)
        self.main_window.stacked_widget.addWidget(new_ec2_window)
        self.main_window.stacked_widget.setCurrentIndex(2)


    def stats_ec2_button_clicked(self):
        stats_ec2_window = EC2StatsWindow(
            self.main_window,
            self.region_selection_input.currentText(),
            self.sender().property('ec2_id')
        )
        self.main_window.stacked_widget.addWidget(stats_ec2_window)
        self.main_window.stacked_widget.setCurrentIndex(2)


    def stop_ec2_button_clicked(self):
        stop_ec2_instance(
            self.main_window.session,
            self.sender().property('ec2_id'),
            self.region_selection_input.currentText()
        )
