from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLineEdit, QPushButton, QProgressBar
from PySide6.QtWidgets import QVBoxLayout


class MainWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.url_text_edit = QLineEdit()
        self.download_button = QPushButton("Download")
        self.progress_bar = QProgressBar()

        layout = QVBoxLayout()
        layout.addWidget(self.url_text_edit)
        layout.addWidget(self.download_button)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
