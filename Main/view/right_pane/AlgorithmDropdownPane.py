import sys

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel, QComboBox, QApplication

from Main.model.search.searcher.AlgorithmDescription import AlgorithmDescription
from Main.model.search.searcher.informed.best_first_Searcher import BestFirstSearcher


class AlgorithmDropdownPane(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.description = QLabel("Algorithm")
        self.layout.addWidget(self.description)

        self.options = QComboBox()
        self.layout.addWidget(self.options)

        # TODO: Maybe the easiest ways to get descriptions will be to have a mapping from algorithm name to the algorithm class inside of this class?
        # TODO: If problems arise, try to iterate over only AlgorithmDescription (tree) leaf subclasses, i.e. not immediate children of AlgorithmDescription; By default, only immediate children are iterated over by __subclasses__.
        def get_leaf_subclasses(cls, accumulator):
            if len(cls.__subclasses__()) == 0: # is leaf node:
                accumulator.append(cls)
            else:
                for subclass in cls.__subclasses__():
                    get_leaf_subclasses(subclass, accumulator)
        acc = []
        get_leaf_subclasses(AlgorithmDescription, acc)
        for algorithm in acc:
            self.options.addItem(algorithm.get_name())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AlgorithmDropdownPane()
    window.show()
    sys.exit(app.exec())