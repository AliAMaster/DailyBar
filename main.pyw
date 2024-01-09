from sys import exit
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QProgressBar, QStyleFactory
from PySide6.QtCore import Qt, QTimer
from time import localtime, time
from calendar import monthrange
import calendar

start_time = 7.75 * 3600
end_time = 17.5 * 3600
working_days = (calendar.SUNDAY, calendar.MONDAY, calendar.TUESDAY, calendar.WEDNESDAY, calendar.THURSDAY)
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
        a.addWidget(self.monthly_bar)
        self.setLayout(a)
        self.update_bars()
        timer = QTimer(self)
        timer.timeout.connect(self.update_bars)
        timer.start(5000)

    def update_bars(self):
        a = calculations()
        self.daily_bar.setValue(a[0])
        self.weekly_bar.setValue(a[1])
        self.monthly_bar.setValue(a[2])
        self.monthly_bar.setFormat(a[3])


def calculations():
    global start_time
    global end_time
    global working_days
    global salary
    curr_time = localtime(time())
    day_tot_secs = end_time - start_time
    day_secs = curr_time.tm_hour * 3600 + curr_time.tm_min * 60 + curr_time.tm_sec - start_time
    day_secs = day_secs if day_secs > 0 else 0
    week_tot_secs = len(working_days) * day_tot_secs
    try:
        week_secs = working_days.index(curr_time.tm_wday) * day_tot_secs + min(day_tot_secs, day_secs)
    except:
        week_secs = 0
    month_tot_secs = monthrange(curr_time.tm_year, curr_time.tm_mon)[1] * 86400
    month_secs = (curr_time.tm_mday - 1) * 86400 + day_secs + start_time
    return min(100, int(day_secs * 100 / day_tot_secs)), min(100, int(week_secs * 100 / week_tot_secs)), min(100, int(month_secs * 100 / month_tot_secs)), '{0:.3f}'.format(
        min(float(salary), round(month_secs * salary / month_tot_secs, 3)))


app = QApplication()
style = QStyleFactory.create("Fusion")
QApplication.setStyle(style)
window = Dialog()
window.show()
exit(app.exec())
