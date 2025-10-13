from abc import ABC, abstractmethod

class BaseChart(ABC):
    @abstractmethod
    def render(self, data):
        pass