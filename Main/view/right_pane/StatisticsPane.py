from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFormLayout, QLineEdit

from Main.communication.event.event import Event
from Main.communication.event.event_type import EventType


class StatisticsPane(QWidget):
    def __init__(self, publisher):
        super().__init__()
        self.publisher = publisher

        layout = QFormLayout()
        self.setLayout(layout)

        self.publisher.subscribe(EventType.SearchConcluded, self)
        self.generatedField = QLineEdit()
        self.generatedField.setReadOnly(True)
        layout.addRow("Generated Nodes:", self.generatedField)


    def update_subscriber(self, event: Event):
        self.generatedField.setText(str(event.data))


