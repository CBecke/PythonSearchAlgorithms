from Main.observer_pattern.publisher import Publisher
from Main.view.search_window import SearchWindow


def main():

    publisher = Publisher()
    view = SearchWindow(publisher)
    model = Model() # TODO: figure out what model is

    controller = Controller(model, view, publisher)
    controller.run()
