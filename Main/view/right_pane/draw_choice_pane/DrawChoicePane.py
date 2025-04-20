from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from Main.communication.event.impl.reset_pressed_event import ResetPressedEvent
from Main.communication.event.impl.radio_toggled_event import RadioToggledEvent
from Main.view.right_pane.draw_choice_pane.draw_choice_button import DrawChoiceButton


class DrawChoicePane(QWidget):
    def __init__(self, publisher):
        super().__init__()
        self.publisher = publisher
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.description = QLabel("Draw:")
        self.description.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.description)

        self.create_buttons()

    def create_buttons(self):
        self.radioAgent = DrawChoiceButton("Agent", Qt.Key.Key_A)
        self.radioWall = DrawChoiceButton("Wall", Qt.Key.Key_W)
        self.radioGoal = DrawChoiceButton("Goal", Qt.Key.Key_G)
        self.radioEmpty = DrawChoiceButton("Empty", Qt.Key.Key_E)

        self.buttons = [self.radioAgent, self.radioWall, self.radioGoal, self.radioEmpty]
        self.radioAgent.setChecked(True)

        radio_layout = QHBoxLayout()
        for btn in self.buttons:
            btn.toggled.connect(self.onClicked)
            radio_layout.addWidget(btn)

        self.publisher.notify(RadioToggledEvent(self.radioAgent.text()))

        outer_layout = QVBoxLayout()
        reset_button = QPushButton("Clear Grid Completely")
        reset_button.clicked.connect(self.reset_grid)

        outer_layout.addLayout(radio_layout)
        outer_layout.addSpacing(30)
        outer_layout.addWidget(reset_button)

        self.layout.addLayout(outer_layout)

    def onClicked(self):
        button = self.sender()
        if button.isChecked():
            self.publisher.notify(RadioToggledEvent(button.text()))

    def reset_grid(self):
        self.publisher.notify(ResetPressedEvent())

    def keyPressEvent(self, event):
        for btn in self.buttons:
            if btn.connected_key == event.key():
                btn.setChecked(True)
                self.publisher.notify(RadioToggledEvent(btn.text()))
                break

