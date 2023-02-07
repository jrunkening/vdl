from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtWidgets import QStatusBar
from PySide6.QtGui import QCloseEvent


from vdl.view.main_widget import MainWidget
from vdl.model import Model


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.main_widget = MainWidget()
        self.model = Model()
        self.status_bar = QStatusBar()

        self.setWindowTitle("Video Downloader")
        self.setMinimumSize(QSize(600, 100))
        self.setCentralWidget(self.main_widget)
        self.setStatusBar(self.status_bar)

        self.init_components()
        self.register_delegation()

    def init_components(self):
        self.main_widget.progress_bar.setValue(0)

    def register_delegation(self):
        self.main_widget.download_button.clicked.connect(
            lambda: self.model.download(
                self.main_widget.url_text_edit.text(),
                self.status_bar,
                self.main_widget.progress_bar
            )
        ) # type: ignore

    def closeEvent(self, event: QCloseEvent) -> None:
        return super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication()
    main = MainWindow()
    main.show()
    app.exec()
