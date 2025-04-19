
from abc import abstractmethod, ABC


class AlgorithmDescription(ABC):

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_description() -> str:
        pass