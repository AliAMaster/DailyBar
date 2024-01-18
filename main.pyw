from sys import exit
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QProgressBar, QStyleFactory
from PySide6.QtCore import Qt, QTimer
from time import localtime, time, struct_time
from calendar import monthrange
import calendar

start_time = (7, 45)
end_time = (17, 30)
working_days = (calendar.SUNDAY, calendar.MONDAY, calendar.TUESDAY, calendar.WEDNESDAY, calendar.THURSDAY)
salary = 360
job_start_date = (5, 6, 2022)
yearly_holidays = 30
holidays_enjoyed = 39
target_holidays = 30

start_time = (start_time[0] + start_time[1] / 60) * 3600
end_time = (end_time[0] + end_time[1] / 60) * 3600
job_start_date = struct_time((job_start_date[2], job_start_date[1], job_start_date[0], 0, 0, 0, 0, 0, 0))


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
        self.holiday_bar = QProgressBar()
        self.holiday_bar.setStyleSheet("QProgressBar::chunk { background-color: #AEBDCA; }""QProgressBar { text-align: center; }")
        a.addWidget(self.holiday_bar)
        self.setLayout(a)
        self.update_bars()
        timer = QTimer(self)
        timer.timeout.connect(self.update_bars)
        timer.start(5000)

    def update_bars(self):
        curr_time = localtime(time())
        day_tot_secs = int(end_time - start_time)
        day_secs = min(max(0, int(curr_time.tm_hour * 3600 + curr_time.tm_min * 60 + curr_time.tm_sec - start_time)), day_tot_secs)
        self.daily_bar.setValue(day_secs * 100 / day_tot_secs)

        week_tot_secs = len(working_days) * day_tot_secs
        if curr_time.tm_wday in working_days:
            week_secs = working_days.index(curr_time.tm_wday) * day_tot_secs + day_secs
        else:
            week_secs = 0
        self.weekly_bar.setValue(week_secs * 100 / week_tot_secs)

        month_tot_secs = monthrange(curr_time.tm_year, curr_time.tm_mon)[1] * 86400
        month_secs = (curr_time.tm_mday - 1) * 86400 + curr_time.tm_hour * 3600 + curr_time.tm_min * 60 + curr_time.tm_sec
        month_progress = month_secs * 100 / month_tot_secs
        self.monthly_bar.setValue(month_progress)

        amount_earned = month_secs * salary / month_tot_secs
        self.monthly_bar.setFormat('{0:.2f}'.format(month_progress) + "%  |  " + '{0:.3f}'.format(amount_earned))

        holidays_earned = delta_days(job_start_date, curr_time) - holidays_enjoyed
        self.holiday_bar.setValue(holidays_earned * 100 / target_holidays)
        self.holiday_bar.setFormat('{0:.2f}'.format(holidays_earned) + " days")


def days_in_year(year):
    a = 0
    for i in range(1, 13):
        a = a + monthrange(year, i)[1]
    return a


def delta_days(start: struct_time, end: struct_time):
    if end.tm_year > start.tm_year:
        a = monthrange(start.tm_year, start.tm_mon)[1] - start.tm_mday + 1
        for i in range(start.tm_mon + 1, 13):
            a += monthrange(start.tm_year, i)[1]
        b = a / days_in_year(start.tm_year)
        for i in range(start.tm_year + 1, end.tm_year):
            b += 1
        a = 0
        for i in range(1, end.tm_mon):
            a += monthrange(end.tm_year, i)
        a += end.tm_mday
        b += a / days_in_year(end.tm_year)
        return b * yearly_holidays
    elif end.tm_mon > start.tm_mon:
        a = monthrange(start.tm_year, start.tm_mon)[1] - start.tm_mday + 1
        for i in range(start.tm_mon + 1, end.tm_mon):
            a = a + monthrange(start.tm_year, i)[1]
        a = a + end.tm_mday
        return a * yearly_holidays / days_in_year(start.tm_year)
    elif end.tm_mday > start.tm_mday:
        return (end.tm_mday - start.tm_mday + 1) * yearly_holidays / days_in_year(start.tm_year)
    else:
        return 0


app = QApplication()
style = QStyleFactory.create("Fusion")
QApplication.setStyle(style)
window = Dialog()
window.show()
exit(app.exec())
