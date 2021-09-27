import gzip
import json
import datetime

from lib.entity import *
from lib.storage import Storage


class OrdersService():

    def __init__(self, filename, storage: Storage):
        self.filename = filename
        self.storage = storage

    def load_data(self):
        with gzip.open(self.filename, 'rb') as f:
            for line in f:
                data = json.loads(line)
                user = User(
                    data['user']['id'], 
                    data['user']['name'],
                    data['user']['city']
                )
                order = Order(data['id'], self._get_formated_time(data['created']), user)
                for p in data['products']:
                    product = Product(p['id'], p['name'], p['price'])
                    order.add_product(product)
                
                self.storage.save_order(order)

    def get_orders_for_date(self, date_from: str, date_to: str) -> Orders:
        return self.storage.get_orders_for_date(date_from, date_to)

    def get_users_with_best_purchases(self, count: int=3) -> Users:
        return self.storage.get_users_with_best_purchases(count)

    def _get_formated_time(self, timestamp: int):
        return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
