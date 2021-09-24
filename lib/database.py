from abc import ABC, abstractmethod
from lib.entity import *


class Database(ABC):

    @abstractmethod
    def save_order(self, order: Order):
        pass

    @abstractmethod
    def get_orders_for_date(self, date_from: str, date_to: str, cnt=10) -> Orders:
        pass

    @abstractmethod
    def get_users_with_best_purchases(self, count=3) -> Users:
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_cursor(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def recreate_database(self):
        pass
