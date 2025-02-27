from abc import abstractmethod

from Main.model.search.searcher.search_log import SearchLog


class LoggedSearcher:

    @abstractmethod
    def logged_search(self, search_problem, log = None) -> SearchLog:
        pass