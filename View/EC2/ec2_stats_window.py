from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, \
        QHBoxLayout, QLineEdit, QComboBox, QSizePolicy
from PySide2.QtGui import QFont, QColor, QPainter, QBrush
from PySide2.QtCore import Qt, QPointF, QDateTime, QRectF
from PySide2.QtCharts import QtCharts
from datetime import datetime, timedelta
from Model.datapoint_model import DatapointModel
from Controller.cloudwatch_controller import get_ec2_stats, get_last_15_min_stats


class EC2StatsWindow(QWidget):
    def __init__(self, main_window, region, instance_id):
        super().__init__()

        self.main_window = main_window
        self.instance_id = instance_id
        self.region = region
        self.axis_x = None
        self.axis_y = None

        layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()

        title_label = QLabel('EC2 Stats Menu', self)
        title_label.setAlignment(Qt.AlignCenter)
        font = QFont('Sans Serif', 30)
        font.setBold(True)
        title_label.setFont(font)
        layout.addWidget(title_label)

        subtitle_label = QLabel(self.instance_id, self)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont('Sans Serif', 18))
        layout.addWidget(subtitle_label)

        back_button = QPushButton('Back to EC2', self)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        stat_selection_layout = QHBoxLayout()
        self.stat_selection_label = QLabel("Select stat:")
        stat_selection_layout.addWidget(self.stat_selection_label)
        self.stat_selection_input = QComboBox()
        #print("Stats:")
        #print(get_ec2_stats(self.main_window.session))
        self.stat_selection_input.addItems(get_ec2_stats(self.main_window.session))
        self.stat_selection_input.currentTextChanged.connect(self.stat_changed)
        stat_selection_layout.addWidget(self.stat_selection_input)
        layout.addLayout(stat_selection_layout)

        self.chart = QtCharts.QChart()
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart.setBackgroundBrush(QBrush(QColor(0, 0, 0, 0)))
        self.view = QtCharts.QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setBackgroundBrush(QBrush(QColor(0, 0, 0, 0)))
        layout.addWidget(self.view)

        layout.addLayout(button_layout)

        self.stat_changed()


    def go_back(self):
        old_widget = self.main_window.stacked_widget.currentWidget()
        self.main_window.stacked_widget.setCurrentIndex(1)
        self.main_window.stacked_widget.removeWidget(old_widget)
    

    def stat_changed(self):
        print("New stat")
        print(self.stat_selection_input.currentText())
        self.chart.removeAllSeries()
        self.chart.removeAxis(self.axis_x)
        self.chart.removeAxis(self.axis_y)
        datapoints = get_last_15_min_stats(
            self.main_window.session,
            self.region,
            self.stat_selection_input.currentText(),
            self.instance_id
        )
        print("datapoints:")
        print([[str(datapoint.timestamp), str(datapoint.value)] for datapoint in datapoints])

        series = QtCharts.QLineSeries()

        for datapoint in datapoints:
            timestamp = QDateTime.fromSecsSinceEpoch(datapoint.timestamp.timestamp())
            series.append(QPointF(timestamp.toMSecsSinceEpoch(), datapoint.value))
            #series.append(datapoint.timestamp, datapoint.value)

        value_count = len(datapoints)
        value_max = max([datapoint.value for datapoint in datapoints]) if value_count > 0 else 0

        self.chart.addSeries(series)
        self.chart.legend().hide()
        #self.chart.setTitle(self.stat_selection_input.currentText())

        #self.chart.createDefaultAxes()
        #axis_x = self.chart.axes(Qt.Horizontal)[0]
        #axis_x.setRange(0, value_max)
        #axis_y = self.chart.axes(Qt.Vertical)[0]
        #axis_y.setRange(0, value_count)
        #axis_y.setLabelFormat("%.1f  ")

        self.axis_x = QtCharts.QDateTimeAxis()
        self.axis_x.setTickCount(10)
        #self.axis_x.setFormat("dd/MM/yyyy ss:mm:hh")
        self.axis_x.setFormat("ss:mm:hh")
        #self.axis_x.setTitleText("Time")
        self.axis_x.setLabelsAngle(45)
        font = self.axis_x.labelsFont()
        font.setPointSize(8)
        self.axis_x.setLabelsFont(font)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        series.attachAxis(self.axis_x)

        self.axis_y = QtCharts.QValueAxis()
        #self.axis_y.setLabelFormat("%i")
        #axis_y.setTickCount(5)
        #axis_y.setRange(0, value_max)
        self.axis_y.setTitleText(self.stat_selection_input.currentText())
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        series.attachAxis(self.axis_y)
        self.chart.setPlotAreaBackgroundVisible(False)
        self.view.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        #self.chart.setPlotArea(QRectF(0,0,300,180))
