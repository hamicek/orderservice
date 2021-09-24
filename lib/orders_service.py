import gzip
import json
import os
import time
import datetime
import uuid

from lib.entity import *
from lib.database import Database


class OrdersService():

    def __init__(self, filename, database: Database):
        self.filename = filename
        self.database = database

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
                
                self.database.save_order(order)

    def get_orders_for_date(self, date_from: str, date_to: str) -> Orders:
        return self.database.get_orders_for_date(date_from, date_to)

    def get_users_with_best_purchases(self, count=3) -> Users:
        return self.database.get_users_with_best_purchases(count)

    def _get_formated_time(self, timestamp: int):
        return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
