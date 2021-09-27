from lib.entity import *
from lib.storage import Storage
from datetime import datetime
import json


class OrdersService():

    def __init__(self, storage: Storage):
        self.storage = storage
        self.orders = Orders()

    def load_data(self, data: str):
        self._map_to_orders(data)
        for order in self.orders:
            self.storage.save_order(order)

    def get_orders_for_date(self, date_from: datetime, date_to: datetime) -> Orders:
        return self.storage.get_orders_for_date(date_from, date_to)

    def get_users_with_best_purchases(self, count: int=3) -> Users:
        return self.storage.get_users_with_best_purchases(count)

    def _map_to_orders(self, data: str):
        for line in data:
            order = json.loads(line)
            user = User(
                order['user']['id'], 
                order['user']['name'],
                order['user']['city']
            )
            new_order = Order(order['id'], self._get_formated_time(order['created']), user)
            for p in order['products']:
                product = Product(p['id'], p['name'], p['price'])
                new_order.add_product(product)

            self.orders.add_order(new_order)

    def _get_formated_time(self, timestamp: int) -> str:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
