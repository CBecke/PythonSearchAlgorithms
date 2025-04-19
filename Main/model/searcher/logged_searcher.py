from abc import abstractmethod

from Main.model.searcher.search_log import SearchLog


class LoggedSearcher:

    @abstractmethod
    def logged_search(self, search_problem, log = None) -> SearchLog:
        pass