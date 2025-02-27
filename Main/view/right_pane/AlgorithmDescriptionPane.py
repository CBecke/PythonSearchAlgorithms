import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication

from Main.model.search.searcher.informed.best_first_Searcher import BestFirstSearcher


class AlgorithmDescriptionPane(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = QLabel("<h1>Description<h1>")
        self.layout.addWidget(self.title)

        self.description = QLabel(BestFirstSearcher.get_description())
        self.description.setWordWrap(True)
        self.layout.addWidget(self.description)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AlgorithmDescriptionPane()
    window.show()
    sys.exit(app.exec())