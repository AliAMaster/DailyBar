from sys import exit
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QProgressBar, QStyleFactory
from PySide6.QtCore import Qt, QTimer
from calendar import monthrange, month_name
from datetime import date, timedelta, datetime, time
import calendar

start_time = (7, 35)
end_time = (13, 55)
working_days = (calendar.SUNDAY, calendar.MONDAY, calendar.TUESDAY, calendar.WEDNESDAY, calendar.THURSDAY)
job_start_date = date(2022, 6, 5)
yearly_holidays = 30
holidays_enjoyed = 98
target_holidays = 30
planned_holiday = None
salary = 850
salary_paid_till = date(2025, 12, 31)
other_funds = -6000
cheat_time = datetime(2026, 3, 9, 15, 30)
cheat_target = timedelta(days=14)


class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("API")
        self.resize(200, 130)
        a = QVBoxLayout()
        self.daily_bar = QProgressBar()
        self.daily_bar.setStyleSheet("QProgressBar::chunk { background-color: #756AB6; }""QProgressBar { text-align: center; }")
        a.addWidget(self.daily_bar)
        self.cheat_bar = QProgressBar()
        self.cheat_bar.setStyleSheet("QProgressBar::chunk { background-color: #B06161; }""QProgressBar { text-align: center; }")
        a.addWidget(self.cheat_bar)
        self.month_bar = QProgressBar()
        self.month_bar.setStyleSheet("QProgressBar::chunk { background-color: #618264; }""QProgressBar { text-align: center; }")
        a.addWidget(self.month_bar)
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
        self.holiday_bar.setValue(int(min(holidays_earned, target_holidays) * 100 / target_holidays))
        
        holiday_start_date = suffrage_calc(job_start_date, holidays_enjoyed + target_holidays)
        self.holiday_bar.setFormat(
            '{0:.2f}'.format(holidays_earned) + " days" + "  |  " + str(holiday_start_date.day) + " " + month_name[holiday_start_date.month] + " " + str(
                holiday_start_date.year))
    
    def update_bars(self):
        curr_time = datetime.now()
        start_today = datetime(curr_time.year, curr_time.month, curr_time.day, start_time[0], start_time[1])
        end_today = datetime(curr_time.year, curr_time.month, curr_time.day, end_time[0], end_time[1])
        day_tot_secs = (end_today - start_today).total_seconds()
        day_secs = (curr_time - start_today).total_seconds()
        self.daily_bar.setValue(max(1, int(day_secs * 100 / day_tot_secs)))
        self.daily_bar.setFormat(str(timedelta(seconds=int((end_today - curr_time).total_seconds()))))
        
        cheat_dur = (curr_time - cheat_time).total_seconds()
        cheat_progress = max(1, int(cheat_dur * 100 / cheat_target.total_seconds()))
        self.cheat_bar.setValue(cheat_progress)
        self.cheat_bar.setFormat(str(timedelta(seconds=int(cheat_dur))))
        
        month_tot_secs = monthrange(curr_time.year, curr_time.month)[1] * 86400
        month_secs = (curr_time - datetime(curr_time.year, curr_time.month, 1)).total_seconds()
        month_progress = month_secs * 100 / month_tot_secs
        self.month_bar.setValue(int(month_progress))
        self.month_bar.setFormat('{0:.2f}'.format(month_progress) + "% | " + str(round(calc_amount(month_progress), 3)))
        
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


def calc_amount(current_month_percent):
    month_counter = date.today().month + 12 * (date.today().year - salary_paid_till.year) - salary_paid_till.month - 1
    previous_month_percent = (monthrange(salary_paid_till.year, salary_paid_till.month)[1] - salary_paid_till.day) / monthrange(salary_paid_till.year, salary_paid_till.month)[1]
    return (month_counter + current_month_percent / 100 + previous_month_percent) * salary + other_funds


app = QApplication()
style = QStyleFactory.create("Fusion")
QApplication.setStyle(style)
window = Dialog()
window.show()
exit(app.exec())
