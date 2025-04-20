from PyQt6.QtCore import QObject, QEvent
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, \
    QSplitter

from Main.model.searcher.search_log import SearchLog
from Main.model.searchproblem.search_problem import SearchProblem
from Main.communication.event.event import Event
from Main.communication.event.event_type import EventType
from Main.view.left_pane.dimension_choice_pane import DimensionChoicePane
from Main.view.left_pane.grid.GridWidget import GridWidget
from Main.view.right_pane.algorithm_dropdown.AlgorithmDropdownDescriptionPane import AlgorithmDropdownDescriptionPane
from Main.view.right_pane.draw_choice_pane.DrawChoicePane import DrawChoicePane
from Main.view.right_pane.OptionsPane import OptionsPane
from Main.view.right_pane.SpeedSliderPane import SpeedSliderPane
from Main.view.right_pane.StatisticsPane import StatisticsPane

WINDOW_HEIGHT = 750
WINDOW_WIDTH = 1100
LEFT_PANE_WIDTH = int(WINDOW_WIDTH * 0.6)
RIGHT_PANE_WIDTH = WINDOW_WIDTH - LEFT_PANE_WIDTH

SLIDER_SPEED_RANGE = (1, 500)

class SearchWindow(QMainWindow):
    def __init__(self, publisher, state):
        super().__init__()
        self.publisher = publisher
        self.publisher.subscribe(EventType.DimensionApplyPressed, self)
        self.setWindowTitle("Search Algorithm Illustrator")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.generalLayout = QHBoxLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(self.generalLayout)
        self.setCentralWidget(central_widget)
        self.installEventFilter(self)

        self.toggledRadioButton = "agent"
        self.publisher.subscribe(EventType.RadioToggled, self)

        # splitter ensures the wanted size ratio between leftPane and rightPane
        self.horizontal_splitter = QSplitter()
        self.create_left_pane(state)
        self.create_right_pane()
        self.grid.set_speed_slider(self.speedSlider)
        self.horizontal_splitter.setSizes([LEFT_PANE_WIDTH, RIGHT_PANE_WIDTH])

        self.generalLayout.addWidget(self.horizontal_splitter)


    def create_left_pane(self, state):
        left_pane_widget = QWidget()
        self.leftPane = QVBoxLayout(left_pane_widget)

        self.create_grid(state)
        self.create_dimension_choice_pane()

        self.horizontal_splitter.addWidget(left_pane_widget)

    def create_grid(self, state):
        self.grid = GridWidget(LEFT_PANE_WIDTH, LEFT_PANE_WIDTH, state, self.publisher)
        self.leftPane.addWidget(self.grid)

    def create_dimension_choice_pane(self):
        self.dimension_choice_pane = DimensionChoicePane(self.publisher)
        self.leftPane.addWidget(self.dimension_choice_pane)

    def create_right_pane(self):
        right_pane_widget = QWidget()
        self.rightPane = QVBoxLayout(right_pane_widget)

        self.create_draw_choice_pane()
        self.create_algorithm_dropdown_description_pane()
        self.create_speed_slider_pane()
        self.create_options_pane()
        self.create_statistics_pane()

        self.horizontal_splitter.addWidget(right_pane_widget)

    def create_draw_choice_pane(self):
        self.draw_choice_pane = DrawChoicePane(self.publisher)
        self.rightPane.addWidget(self.draw_choice_pane)

    def create_algorithm_dropdown_description_pane(self):
        self.algorithm_dropdown = AlgorithmDropdownDescriptionPane(self.publisher)
        self.rightPane.addWidget(self.algorithm_dropdown)

    def create_speed_slider_pane(self):
        self.speedSlider = SpeedSliderPane(SLIDER_SPEED_RANGE[0], SLIDER_SPEED_RANGE[1])
        self.rightPane.addWidget(self.speedSlider)

    def create_options_pane(self):
        self.options_pane = OptionsPane(self.publisher)
        self.rightPane.addWidget(self.options_pane)

    def create_statistics_pane(self):
        self.statistics_pane = StatisticsPane(self.publisher)
        self.rightPane.addWidget(self.statistics_pane)

    def update_problem(self, problem: SearchProblem):
        grid = problem.get_state()
        self.leftPane.removeWidget(self.grid)
        self.grid.deleteLater()

        self.grid = GridWidget(LEFT_PANE_WIDTH, LEFT_PANE_WIDTH, grid, self.publisher)
        self.leftPane.insertWidget(0, self.grid)

    def update_subscriber(self, event: Event):
        if event.event_type == EventType.DimensionApplyPressed:
            grid_size = event.data
            dimensioned_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
            self.leftPane.removeWidget(self.grid)
            self.grid.deleteLater()
            self.grid = GridWidget(LEFT_PANE_WIDTH, LEFT_PANE_WIDTH, dimensioned_grid, self.publisher, self.toggledRadioButton)
            self.grid.set_speed_slider(self.speedSlider)
            self.leftPane.insertWidget(0, self.grid)
        elif event.event_type == EventType.RadioToggled:
            self.toggledRadioButton = event.data

    def get_grid_representation(self):
        return self.grid.get_grid()

    def unlock_grid(self):
        self.grid.unlock()

    def render_search(self, log: SearchLog):
        self.grid.render_search(log)

    def update_color_map(self, problem):
        self.grid.update_color_map(problem)

    def get_searcher(self):
        return self.algorithm_dropdown.get_toggled()

    def keyPressEvent(self, event):
        self.draw_choice_pane.keyPressEvent(event)

    def eventFilter(self, obj: QObject, event: QEvent):
        if event.type() == QEvent.Type.MouseButtonPress:
            self.dimension_choice_pane.unfocus_lineedit()
        return super().eventFilter(obj, event)

