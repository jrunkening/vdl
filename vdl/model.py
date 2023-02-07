from yt_dlp import YoutubeDL
import re


class Logger:
    def __init__(self, status_bar, progress_bar) -> None:
        self.status_bar = status_bar
        self.progress_bar = progress_bar

    def debug(self, message):
        # both debug and info are passed into debug,
        # distinguish them by the prefix "[debug] "
        if message.startswith("[debug] "):
            self.status_bar.showMessage(message)
        else:
            self.info(message)

    def info(self, message):
        if re.match("^\[download\] *+(\d*%|\d*.\d*%)", message):
            progress_ratio = round(float(message.split()[1][:-1]))
            self.progress_bar.setValue(progress_ratio)
            self.status_bar.showMessage(message)
        else:
            self.status_bar.showMessage(message)

    def warning(self, message):
        self.status_bar.showMessage(message)

    def error(self, message):
        self.status_bar.showMessage(message)


class Model:
    def download(self, url: str, status_bar, progress_bar):
        download_options = {
            "format": "bestvideo+bestaudio/best",
            "logger": Logger(status_bar, progress_bar),
        }
        with YoutubeDL(download_options) as ydl:
            ydl.download(url)
