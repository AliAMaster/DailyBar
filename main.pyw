from sys import exit
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QProgressBar, QStyleFactory
from PySide6.QtCore import Qt, QTimer
from time import localtime, time
from calendar import monthrange, month_name
from datetime import date, timedelta, datetime
import calendar

start_time = (7, 45)
end_time = (17, 30)
working_days = (calendar.SUNDAY, calendar.MONDAY, calendar.TUESDAY, calendar.WEDNESDAY, calendar.THURSDAY)
job_start_date = date(2022, 6, 5)
yearly_holidays = 30
holidays_enjoyed = 39
target_holidays = 30
planned_holiday = None

start_time = (start_time[0] + start_time[1] / 60) * 3600
end_time = (end_time[0] + end_time[1] / 60) * 3600


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
        self.holiday_bar.setStyleSheet("QProgressBar::chunk { background-color: #013C4D; }""QProgressBar { text-align: center; }")
        a.addWidget(self.holiday_bar)
        self.setLayout(a)
        self.init_update()
        self.update_bars()
        timer = QTimer(self)
        timer.timeout.connect(self.update_bars)
        timer.start(5000)

    def init_update(self):
        curr_time = date.today()
        holidays_earned = max(holiday_calc(job_start_date, curr_time) - holidays_enjoyed, 0.0)
        self.holiday_bar.setValue(min(holidays_earned, target_holidays) * 100 / target_holidays)

        holiday_start_date = suffrage_calc(job_start_date, holidays_enjoyed + target_holidays)
        self.holiday_bar.setFormat(
            '{0:.2f}'.format(holidays_earned) + " days" + "  |  " + str(holiday_start_date.day) + " " + month_name[holiday_start_date.month] + " " + str(
                holiday_start_date.year))

    def update_bars(self):
        curr_time = localtime(time())
        day_tot_secs = int(end_time - start_time)
        day_secs = min(max(0, int(curr_time.tm_hour * 3600 + curr_time.tm_min * 60 + curr_time.tm_sec - start_time)), day_tot_secs)
        self.daily_bar.setValue(int(day_secs * 100 / day_tot_secs))

        week_tot_secs = len(working_days) * day_tot_secs
        if curr_time.tm_wday in working_days:
            week_secs = working_days.index(curr_time.tm_wday) * day_tot_secs + day_secs
        else:
            week_secs = 0
        self.weekly_bar.setValue(int(week_secs * 100 / week_tot_secs))

        month_tot_secs = monthrange(curr_time.tm_year, curr_time.tm_mon)[1] * 86400
        month_secs = (curr_time.tm_mday - 1) * 86400 + curr_time.tm_hour * 3600 + curr_time.tm_min * 60 + curr_time.tm_sec
        month_progress = month_secs * 100 / month_tot_secs
        self.monthly_bar.setValue(int(month_progress))

        self.monthly_bar.setFormat('{0:.2f}'.format(month_progress) + "%")

        if planned_holiday is not None:
            self.holiday_bar.setFormat(planned_holiday_calc(planned_holiday))


def days_in_year(year: int):
    return (date(year + 1, 1, 1) - date(year, 1, 1)).days


def holiday_calc(start: date, end: date):
    if start >= end:
        a = start
        start = end
        end = a
    if start.year == end.year:
        return ((end - start).days + 1) * yearly_holidays / days_in_year(start.year)
    else:
        a = (date(start.year + 1, 1, 1) - start).days * yearly_holidays / days_in_year(start.year)
        for i in range(start.year + 1, end.year):
            a += yearly_holidays
        a += (end - date(end.year - 1, 12, 31)).days * yearly_holidays / days_in_year(end.year)
    return a


def suffrage_calc(start: date, holidays: int):
    if holiday_calc(start, date(start.year, 12, 1)) < holidays:
        return start + timedelta(days=int(holidays * days_in_year(start.year) / yearly_holidays))
    else:
        a = holidays - holiday_calc(start, date(start.year + 1, 1, 1))
        year = start.year + 1
        while True:
            if a < yearly_holidays:
                break
            a -= yearly_holidays
            year += 1
        a += date(year - 1, 12, 31) + timedelta(days=int(a * days_in_year(year) / yearly_holidays))


def planned_holiday_calc(dt: datetime):
    a = str(dt - datetime.now())
    a = a[:a.find(".")]
    return a


app = QApplication()
style = QStyleFactory.create("Fusion")
QApplication.setStyle(style)
window = Dialog()
window.show()
exit(app.exec())
