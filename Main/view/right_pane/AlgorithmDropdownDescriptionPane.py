import sys

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QApplication, QVBoxLayout

from Main.model.searcher import algorithm_registry


class AlgorithmDropdownDescriptionPane(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.create_dropdown()
        self.create_description()

        # TODO: implement that changing the dropdown value 1) updates the description, and 2) updates the searcher used for start

    def create_dropdown(self):
        self.dropdown_layout = QHBoxLayout()
        self.layout.addLayout(self.dropdown_layout)
        self.dropdown_label = QLabel("Algorithm")
        self.dropdown_layout.addWidget(self.dropdown_label)

        self.dropdown = QComboBox()
        self.dropdown_layout.addWidget(self.dropdown)

        for algorithm in algorithm_registry.algorithms:
            self.dropdown.addItem(algorithm.get_name())

        self.dropdown.currentTextChanged.connect(self.on_dropdown_change)

    def create_description(self):
        self.description_layout = QVBoxLayout()
        self.layout.addLayout(self.description_layout)

        self.description_title = QLabel("<h1>Description<h1>")
        self.description_layout.addWidget(self.description_title)

        self.description = QLabel(self.get_description_text(self.dropdown.currentText()))
        self.description.setWordWrap(True)
        self.description_layout.addWidget(self.description)

    def on_dropdown_change(self, text):
        self.description.setText(self.get_description_text(text))

    def get_description_text(self, dropdown_text):
        return algorithm_registry.name_to_algorithm[dropdown_text].get_description()

    def get_toggled(self) -> str:
        return algorithm_registry.name_to_algorithm[self.dropdown.currentText()]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AlgorithmDropdownDescriptionPane()
    window.show()
    sys.exit(app.exec())