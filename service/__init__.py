from abc import ABC, abstractmethod


class Service(ABC):

    @abstractmethod
    def add(self, *args, **kwargs):
        pass

    @abstractmethod
    def exist_by_id(self, t_id):
        pass

    @abstractmethod
    def by_id(self, t_id):
        pass

    @abstractmethod
    def remove_by_id(self, t_id):
        pass
