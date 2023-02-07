from PySide6.QtCore import QThread, Signal

from yt_dlp import YoutubeDL
import re


class Logger:
    def __init__(self, status_updated: Signal, progress_updated: Signal) -> None:
        self.status_updated = status_updated
        self.progress_updated = progress_updated

    def debug(self, message):
        # both debug and info are passed into debug,
        # distinguish them by the prefix "[debug] "
        if message.startswith("[debug] "):
            self.status_updated.emit(message)
        else:
            self.info(message)

    def info(self, message):
        if re.match("^\[download\] *+(\d*%|\d*.\d*%)", message):
            progress_ratio = round(float(message.split()[1][:-1]))
            self.progress_updated.emit(progress_ratio)
            self.status_updated.emit(message)
        else:
            self.status_updated.emit(message)

    def warning(self, message):
        self.status_updated.emit(message)

    def error(self, message):
        self.status_updated.emit(message)


class Downloader(QThread):
    started = Signal()
    status_updated = Signal(str)
    progress_updated = Signal(int)
    finished = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.url = ""

    def run(self):
        self.started.emit()

        download_options = {
            "format": "bestvideo+bestaudio/best",
            "logger": Logger(self.status_updated, self.progress_updated),
        }
        with YoutubeDL(download_options) as ydl:
            ydl.download(self.url)

        self.finished.emit()


class Model:
    def __init__(self) -> None:
        self.downloader = Downloader()

    def download(self, url: str):
        self.downloader.url = url
        self.downloader.start()
