import sys

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QApplication, QVBoxLayout, QPushButton

from Main.communication.event.event import Event
from Main.communication.event.event_type import EventType
from Main.communication.event.heuristic_update_event import HeuristicUpdateEvent
from Main.model.searcher import algorithm_registry
from Main.model.searcher.algorithm_registry import algorithm
from Main.model.searcher.informed.a_star import manhattan_distance, AStarSearcher
from Main.view.right_pane.algorithm_dropdown.custom_heuristic_popup import CustomHeuristicPopup


class AlgorithmDropdownDescriptionPane(QWidget):
    def __init__(self, publisher):
        super().__init__()
        self.current_heuristic_function = manhattan_distance
        self.publisher = publisher
        self.publisher.subscribe(EventType.HeuristicUpdate, self)

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

        self.heuristic_popup_button = QPushButton("Custom Heuristic Function")
        self.heuristic_popup_button.clicked.connect(self.open_heuristic_popup)
        self.description_layout.addWidget(self.heuristic_popup_button)

    def on_dropdown_change(self, text):
        self.description.setText(self.get_description_text(text))
        self.publisher.notify(EventType.HeuristicUpdate, HeuristicUpdateEvent(manhattan_distance))


    def get_description_text(self, dropdown_text):
        return algorithm_registry.name_to_algorithm[dropdown_text].get_description()

    def get_toggled(self) -> str:
        return algorithm_registry.name_to_algorithm[self.dropdown.currentText()]

    def open_heuristic_popup(self):
        CustomHeuristicPopup(self.publisher).exec()

    def update_subscriber(self, event: Event):
        if event.get_type() == EventType.HeuristicUpdate:
            current_searcher = algorithm_registry.name_to_algorithm[self.dropdown.currentText()]
            if isinstance(current_searcher, AStarSearcher):
                current_searcher.set_heuristic(event.get_data())




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AlgorithmDropdownDescriptionPane()
    window.show()
    sys.exit(app.exec())