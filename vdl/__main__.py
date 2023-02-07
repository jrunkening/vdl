from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget
from PySide6.QtWidgets import QLineEdit, QPushButton, QProgressBar
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QCloseEvent

from yt_dlp import YoutubeDL
import re


class DownloadingLogger:
    def __init__(self, progress_bar) -> None:
        self.progress_bar = progress_bar

    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix "[debug] "
        if msg.startswith("[debug] "):
            print(msg)
        else:
            self.info(msg)

    def info(self, msg):
        if re.match("^\[download\] *+(\d*%|\d*.\d*%)", msg):
            progress_ratio = round(float(msg.split()[1][:-1]))
            self.progress_bar.setValue(progress_ratio)
            print(msg)
        else:
            print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


class MainWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.url_text_edit = QLineEdit()
        self.url_text_edit.setText("https://www.youtube.com/watch?v=BaW_jenozKc")

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download) # type: ignore

        self.progress_bar = QProgressBar()

        layout = QVBoxLayout()
        layout.addWidget(self.url_text_edit)
        layout.addWidget(self.download_button)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def download(self):
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "logger": DownloadingLogger(self.progress_bar),
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(self.url_text_edit.text())


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.main_widget = MainWidget()
        # self.model = Model()

        self.setWindowTitle("Video Downloader")
        self.setMinimumSize(QSize(400, 100))
        self.setCentralWidget(self.main_widget)

        self.init_components()
        self.register_side_bar_delegation()

    def init_components(self):
        ...

    def register_side_bar_delegation(self):
        ...

    def measure_and_plot(self):
        ...

    def closeEvent(self, event: QCloseEvent) -> None:
        return super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication()
    main = MainWindow()
    main.show()
    app.exec()
