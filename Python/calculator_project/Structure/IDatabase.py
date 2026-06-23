from abc import ABC, abstractmethod


class InterfaceDatabase(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass
    
    @abstractmethod
    def execute(self, query: str) -> list[dict]:
        pass
    
    @abstractmethod
    def getData(self, query: str) -> list[dict]:
        pass