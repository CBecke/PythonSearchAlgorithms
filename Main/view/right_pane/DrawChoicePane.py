import sys

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication, QPushButton, QGridLayout


class DrawChoicePane(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.description = QLabel("Draw:")
        self.layout.addWidget(self.description)

        self.createButtons()

    def createButtons(self):
        button_texts = [["Agent", "Wall", "Goal"],
                             ["Empty", "Reset"]]
        self.buttonMap = dict()

        buttonsLayout = QGridLayout()

        for i, row in enumerate(button_texts):
            for j, text in enumerate(row):
                self.buttonMap[text] = QPushButton(text)
                buttonsLayout.addWidget(self.buttonMap[text], i, j)

        self.layout.addLayout(buttonsLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DrawChoicePane()
    window.show()
    sys.exit(app.exec())
