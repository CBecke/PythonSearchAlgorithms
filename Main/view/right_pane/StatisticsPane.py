from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFormLayout, QLineEdit


class StatisticsPane(QWidget):
    def __init__(self):
        super().__init__()

        layout = QFormLayout()
        self.setLayout(layout)

        generatedField = QLineEdit()
        generatedField.setReadOnly(True)
        layout.addRow("Generated Nodes:", generatedField)

