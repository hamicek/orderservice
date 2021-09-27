from abc import ABC, abstractmethod
from lib.entity import *
from datetime import datetime


class Storage(ABC):

    @abstractmethod
    def save_order(self, order: Order):
        pass

    @abstractmethod
    def get_orders_for_date(self, date_from: datetime, date_to: datetime, cnt: int=10) -> Orders:
        pass

    @abstractmethod
    def get_users_with_best_purchases(self, cnt: int=3) -> Users:
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def recreate_database(self):
        pass
