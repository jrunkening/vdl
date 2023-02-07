from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QCloseEvent

from yt_dlp import YoutubeDL


class DownloadingLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix "[debug] "
        if msg.startswith("[debug] "):
            print(msg)
        else:
            self.info(msg)

    def info(self, msg):
        if msg.startswith("[download] Destination"):
            print(msg)
        elif msg.startswith("[download] "):
            msg = msg.split()
            progress_ratio = msg[1]
            eta = msg[-1]
            print(f"{progress_ratio[:-1]}, {eta}")
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

        layout = QVBoxLayout()
        layout.addWidget(self.url_text_edit)
        layout.addWidget(self.download_button)
        self.setLayout(layout)

    def download(self):
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "logger": DownloadingLogger(),
        }
        with YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(self.url_text_edit.text())


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
