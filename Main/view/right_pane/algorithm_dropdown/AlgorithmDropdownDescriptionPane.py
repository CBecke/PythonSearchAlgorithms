from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QVBoxLayout, QPushButton

from Main.communication.event.event import Event
from Main.communication.event.event_type import EventType
from Main.communication.event.impl.heuristic_update_event import HeuristicUpdateEvent
from Main.model.searcher import algorithm_registry
from Main.model.searcher.informed.impl.a_star import manhattan_distance, AStarSearcher
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

        self.create_title()

        self.description = QLabel(self.get_description_text(self.dropdown.currentText()))
        self.description.setWordWrap(True)
        self.description_layout.addWidget(self.description)

        self.create_heuristic_button()

    def create_title(self):
        self.description_title = QLabel("\nDescription")
        self.description_layout.addWidget(self.description_title)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        self.description_title.setFont(title_font)

    def create_heuristic_button(self):
        self.heuristic_popup_button = QPushButton("Custom Heuristic Function")
        self.heuristic_popup_button.clicked.connect(self.open_heuristic_popup)
        self.description_layout.addWidget(self.heuristic_popup_button)
        self.maybe_show_heuristic_button()


    def on_dropdown_change(self, text):
        self.description.setText(self.get_description_text(text))
        self.publisher.notify(HeuristicUpdateEvent(manhattan_distance))
        self.maybe_show_heuristic_button()


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

    def maybe_show_heuristic_button(self):
        if isinstance(self.get_toggled(), AStarSearcher):
            self.heuristic_popup_button.show()
        else:
            self.heuristic_popup_button.hide()