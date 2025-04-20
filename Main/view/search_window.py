from PyQt6.QtCore import QObject, QEvent
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, \
    QSplitter

from Main.model.searcher.search_log import SearchLog
from Main.model.searchproblem.search_problem import SearchProblem
from Main.communication.event.event import Event
from Main.communication.event.event_type import EventType
from Main.view.left_pane.DimensionChoiceWidget import DimensionChoiceWidget
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
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self.installEventFilter(self)

        self.toggledRadioButton = "agent"
        self.publisher.subscribe(EventType.RadioToggled, self)

        # splitter ensures the wanted size ratio between leftPane and rightPane
        self.horizontal_splitter = QSplitter()
        self.createLeftPane(state)
        self.createRightPane()
        self.grid.set_speed_slider(self.speedSlider)
        self.horizontal_splitter.setSizes([LEFT_PANE_WIDTH, RIGHT_PANE_WIDTH])

        self.generalLayout.addWidget(self.horizontal_splitter)


    def createLeftPane(self, state):
        leftPaneWidget = QWidget()
        self.leftPane = QVBoxLayout(leftPaneWidget)

        self.createGrid(state)
        self.createDimensionChoicePane()

        self.horizontal_splitter.addWidget(leftPaneWidget)

    def createGrid(self, state):
        self.grid = GridWidget(LEFT_PANE_WIDTH, LEFT_PANE_WIDTH, state, self.publisher)
        self.leftPane.addWidget(self.grid)

    def createDimensionChoicePane(self):
        self.dimensionChoicePane = DimensionChoiceWidget(self.publisher)
        self.leftPane.addWidget(self.dimensionChoicePane)

    def createRightPane(self):
        rightPaneWidget = QWidget()
        self.rightPane = QVBoxLayout(rightPaneWidget)

        self.createDrawChoicePane()
        self.createAlgorithmDropdownDescriptionPane()
        self.createSpeedSliderPane()
        self.createOptionsPane()
        self.createStatisticsPane()

        self.horizontal_splitter.addWidget(rightPaneWidget)

    def createDrawChoicePane(self):
        self.drawChoicePane = DrawChoicePane(self.publisher)
        self.rightPane.addWidget(self.drawChoicePane)

    def createAlgorithmDropdownDescriptionPane(self):
        self.algorithmDropdown = AlgorithmDropdownDescriptionPane()
        self.rightPane.addWidget(self.algorithmDropdown)

    def createSpeedSliderPane(self):
        self.speedSlider = SpeedSliderPane(SLIDER_SPEED_RANGE[0], SLIDER_SPEED_RANGE[1])
        self.rightPane.addWidget(self.speedSlider)

    def createOptionsPane(self):
        self.optionsPane = OptionsPane(self.publisher)
        self.rightPane.addWidget(self.optionsPane)

    def createStatisticsPane(self):
        self.statisticsPane = StatisticsPane(self.publisher)
        self.rightPane.addWidget(self.statisticsPane)

    def update_problem(self, problem: SearchProblem):
        grid = problem.get_state()
        self.leftPane.removeWidget(self.grid)
        self.grid.deleteLater()

        self.grid = GridWidget(LEFT_PANE_WIDTH, LEFT_PANE_WIDTH, grid, self.publisher)
        self.leftPane.insertWidget(0, self.grid)

    def update_subscriber(self, event: Event):
        if event.type == EventType.DimensionApplyPressed:
            grid_size = event.data
            dimensionedGrid = [[0 for j in range(grid_size)] for i in range(grid_size)]
            self.leftPane.removeWidget(self.grid)
            self.grid.deleteLater()
            self.grid = GridWidget(LEFT_PANE_WIDTH, LEFT_PANE_WIDTH, dimensionedGrid, self.publisher, self.toggledRadioButton)
            self.grid.set_speed_slider(self.speedSlider)
            self.leftPane.insertWidget(0, self.grid)
        elif event.type == EventType.RadioToggled:
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
        return self.algorithmDropdown.get_toggled()

    def keyPressEvent(self, event):
        self.drawChoicePane.keyPressEvent(event)

    def eventFilter(self, obj: QObject, event: QEvent):
        if event.type() == QEvent.Type.MouseButtonPress:
            self.dimensionChoicePane.unfocus_lineedit()
        return super().eventFilter(obj, event)




"""
def main():
    app = QApplication([])
    publisher = Publisher()
    searchWindow = SearchWindow(publisher)
    searchWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
"""
