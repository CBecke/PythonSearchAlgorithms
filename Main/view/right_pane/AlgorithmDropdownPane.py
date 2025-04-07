import sys

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel, QComboBox, QApplication

from Main.model.search.searcher import algorithm_registry
from Main.model.search.searcher.algorithm_description import AlgorithmDescription
from Main.model.search.searcher.informed.best_first_searcher import BestFirstSearcher


class AlgorithmDropdownPane(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.description = QLabel("Algorithm")
        self.layout.addWidget(self.description)

        self.options = QComboBox()
        self.layout.addWidget(self.options)

        for algorithm in algorithm_registry.algorithms:
            self.options.addItem(algorithm.get_name())

        # TODO: implement that changing the dropdown value 1) updates the description, and 2) updates the searcher used for start

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AlgorithmDropdownPane()
    window.show()
    sys.exit(app.exec())