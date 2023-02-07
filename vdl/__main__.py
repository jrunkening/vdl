from pathlib import Path

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtWidgets import QStatusBar
from PySide6.QtGui import QCloseEvent

from vdl.view.main_widget import MainWidget
from vdl.model import Model


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.theme = "dark"
        self.main_widget = MainWidget()
        self.model = Model()
        self.status_bar = QStatusBar()

        self.setWindowTitle("Video Downloader")
        self.setFixedSize(QSize(600, 100))
        self.setStyleSheet(open(
            Path(__file__).parent.joinpath(f"themes/{self.theme}.qss"),
            "r"
        ).read())

        self.setCentralWidget(self.main_widget)
        self.setStatusBar(self.status_bar)

        self.init_components()
        self.register_delegation()

    def init_components(self):
        self.main_widget.progress_bar.setValue(0)
        self.status_bar.showMessage("Ready")

    def register_delegation(self):
        self.model.downloader.started.connect(
            lambda: self.main_widget.download_button.setDisabled(True)
        )
        self.model.downloader.status_updated.connect(
            lambda message: self.status_bar.showMessage(message)
        )
        self.model.downloader.progress_updated.connect(
            lambda progress: self.main_widget.progress_bar.setValue(progress)
        )
        self.model.downloader.finished.connect(
            lambda: self.main_widget.download_button.setDisabled(False)
        )
        self.main_widget.download_button.clicked.connect(
            lambda: self.model.download(self.main_widget.url_text_edit.text())
        )

    def closeEvent(self, event: QCloseEvent) -> None:
        return super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication()
    main = MainWindow()
    main.show()
    app.exec()
