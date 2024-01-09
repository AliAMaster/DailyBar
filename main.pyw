from sys import exit
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QProgressBar, QStyleFactory
from PySide6.QtCore import Qt, QTimer
from time import localtime, time


class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowTitle("API")
        self.resize(1280, 50)
        a = QVBoxLayout()
        self.progressbar = QProgressBar()
        self.progressbar.setStyleSheet("QProgressBar::chunk { background-color: #756AB6; }""QProgressBar { text-align: center; }")
        a.addWidget(self.progressbar)
        self.update_bar()
        self.setLayout(a)
        timer = QTimer(self)
        timer.timeout.connect(self.update_bar)
        timer.start(30000)

    def update_bar(self):
        self.progressbar.setValue(day_progress(7.5, 17.66))


def day_progress(start: float, end: float):
    start = start * 3600
    end = end * 3600
    current = localtime(time()).tm_hour * 3600 + localtime(time()).tm_min * 60 + localtime(time()).tm_sec
    return int((current - start) * 100 / (end - start))


app = QApplication()
style = QStyleFactory.create("Fusion")
QApplication.setStyle(style)
window = Dialog()
window.show()
exit(app.exec())
