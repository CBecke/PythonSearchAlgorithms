import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget, QVBoxLayout, \
    QSplitter

from Main.view.left_pane.DimensionChoiceWidget import DimensionChoiceWidget
from Main.view.left_pane.GridWidget import GridWidget
from Main.view.right_pane.AlgorithmDescriptionPane import AlgorithmDescriptionPane
from Main.view.right_pane.AlgorithmDropdownPane import AlgorithmDropdownPane
from Main.view.right_pane.DrawChoicePane import DrawChoicePane
from Main.view.right_pane.OptionsPane import OptionsPane
from Main.view.right_pane.SpeedSliderPane import SpeedSliderPane
from Main.view.right_pane.StatisticsPane import StatisticsPane

WINDOW_HEIGHT = 750
WINDOW_WIDTH = 1100
LEFT_PANE_WIDTH = int(WINDOW_WIDTH * 0.6)
RIGHT_PANE_WIDTH = WINDOW_WIDTH - LEFT_PANE_WIDTH

SLIDER_SPEED_RANGE = (0,100)

class SearchWindow(QMainWindow):
    def __init__(self, publisher):
        super().__init__()
        self.publisher = publisher
        self.setWindowTitle("Search Algorithm Illustrator")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.generalLayout = QHBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)

        # splitter ensures the wanted size ratio between leftPane and rightPane
        self.horizontal_splitter = QSplitter()
        self.createLeftPane()
        self.createRightPane()
        self.horizontal_splitter.setSizes([LEFT_PANE_WIDTH, RIGHT_PANE_WIDTH])

        self.generalLayout.addWidget(self.horizontal_splitter)




    def createLeftPane(self):
        leftPaneWidget = QWidget()
        self.leftPane = QVBoxLayout(leftPaneWidget)

        self.createGrid()
        self.createDimensionChoicePane()

        self.horizontal_splitter.addWidget(leftPaneWidget)

    def createGrid(self):
        self.grid = GridWidget(LEFT_PANE_WIDTH, LEFT_PANE_WIDTH, 15, 15)
        self.leftPane.addWidget(self.grid)

    def createDimensionChoicePane(self):
        self.dimensionChoicePane = DimensionChoiceWidget(self.publisher)
        self.leftPane.addWidget(self.dimensionChoicePane)

    def createRightPane(self):
        rightPaneWidget = QWidget()
        self.rightPane = QVBoxLayout(rightPaneWidget)

        self.createDrawChoicePane()
        self.createAlgorithmDropdownPane()
        self.createAlgorithmDescriptionPane()
        self.createSpeedSliderPane()
        self.createOptionsPane()
        self.createStatisticsPane()

        self.horizontal_splitter.addWidget(rightPaneWidget)

    def createDrawChoicePane(self):
        self.drawChoicePane = DrawChoicePane()
        self.rightPane.addWidget(self.drawChoicePane)

    def createAlgorithmDropdownPane(self):
        self.algorithmDropdown = AlgorithmDropdownPane()
        self.rightPane.addWidget(self.algorithmDropdown)

    def createAlgorithmDescriptionPane(self):
        self.algorithmDescription = AlgorithmDescriptionPane()
        self.rightPane.addWidget(self.algorithmDescription)

    def createSpeedSliderPane(self):
        self.speedSlider = SpeedSliderPane(SLIDER_SPEED_RANGE[0], SLIDER_SPEED_RANGE[1])
        self.rightPane.addWidget(self.speedSlider)

    def createOptionsPane(self):
        self.optionsPane = OptionsPane()
        self.rightPane.addWidget(self.optionsPane)

    def createStatisticsPane(self):
        self.statisticsPane = StatisticsPane()
        self.rightPane.addWidget(self.statisticsPane)


def main():
    app = QApplication([])
    searchWindow = SearchWindow()
    searchWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()