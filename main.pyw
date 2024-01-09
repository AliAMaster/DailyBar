from sys import exit
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QProgressBar, QStyleFactory, QLabel
from PySide6.QtCore import Qt, QTimer
from time import localtime, time
from calendar import monthrange

start_time = 7.5 * 3600
end_time = 17.66 * 3600
working_days = 5
salary = 360


class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowTitle("API")
        self.resize(1280, 130)
        a = QVBoxLayout()
        self.daily_bar = QProgressBar()
        self.daily_bar.setStyleSheet("QProgressBar::chunk { background-color: #756AB6; }""QProgressBar { text-align: center; }")
        a.addWidget(self.daily_bar)
        self.weekly_bar = QProgressBar()
        self.weekly_bar.setStyleSheet("QProgressBar::chunk { background-color: #B06161; }""QProgressBar { text-align: center; }")
        a.addWidget(self.weekly_bar)
        self.monthly_bar = QProgressBar()
        self.monthly_bar.setStyleSheet("QProgressBar::chunk { background-color: #618264; }""QProgressBar { text-align: center; }")
        self.earning = QLabel()
        self.earning.setAlignment(Qt.AlignCenter)
        a.addWidget(self.monthly_bar)
        a.addWidget(self.earning)
        self.setLayout(a)
        self.update_bars()
        timer = QTimer(self)
        timer.timeout.connect(self.update_bars)
        timer.start(30000)

    def update_bars(self):
        self.daily_bar.setValue(day_progress())
        self.weekly_bar.setValue(week_progress())
        self.monthly_bar.setValue(month_progress())
        self.earning.setText(earning_calc())


def day_progress():
    global start_time
    global end_time
    curr_time = localtime(time())
    current = curr_time.tm_hour * 3600 + curr_time.tm_min * 60 + curr_time.tm_sec
    return int((current - start_time) * 100 / (end_time - start_time))


def week_progress():
    global start_time
    global end_time
    global working_days
    curr_time = localtime(time())
    wday = curr_time.tm_wday + 1 if curr_time.tm_wday < 5 else curr_time.tm_wday - 6
    current = wday * (end_time - start_time) + curr_time.tm_hour * 3600 + curr_time.tm_min * 60 + curr_time.tm_sec
    return int((current - start_time) * 100 / (working_days * (end_time - start_time)))


def month_progress():
    curr_time = localtime(time())
    current = curr_time.tm_mday * 86400 + curr_time.tm_hour * 3600 + curr_time.tm_min * 60 + curr_time.tm_sec
    return int(current * 100 / (monthrange(curr_time.tm_year, curr_time.tm_mon)[1] * 86400))


def earning_calc():
    global salary
    return str(int(salary * month_progress() / 100))


app = QApplication()
style = QStyleFactory.create("Fusion")
QApplication.setStyle(style)
window = Dialog()
window.show()
exit(app.exec())
