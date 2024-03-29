import os
import sqlite3
import uuid
from lib.entity import *
from lib.storage import Storage
from datetime import datetime


class Sqlite(Storage):
    def __init__(self, name: str):
        self.name = name
        self.connection = None

    def save_order(self, order: Order):
        cur = self._get_cursor()
        cur.execute('INSERT INTO orders VALUES (?, ?, ?)', (order.order_id, order.created, order.user.user_id))
        cur.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?)', (order.user.user_id, order.user.name, order.user.city))
        for p in order.products:
            cur.execute('INSERT OR IGNORE INTO products VALUES (?, ?, ?)', (p.product_id, p.name, p.price))
            cur.execute('INSERT OR IGNORE INTO order_products VALUES (?, ?)', 
                (order.order_id, p.product_id))

    def get_orders_for_date(self, date_from: datetime, date_to: datetime, cnt: int=10) -> Orders:
        cur = self._get_cursor()
        sql = '''SELECT
                    o.id,
                    o.created,
                    u.id,
                    u.name,
                    u.city,
                    p.id,
                    p.name,
                    p.price
                 FROM order_products as op
                    LEFT JOIN orders as o ON (op.order_id = o.id)
                    LEFT JOIN users as u ON (o.user_id = u.id)
                    LEFT JOIN products as p ON (op.product_id = p.id)
                 WHERE 
                    o.created>=? and o.created<=? and
                    o.id in (
                        select id
                        from orders
                        WHERE created>=? and created<=?
                        ORDER BY created
                        LIMIT ?
                    )
                 ORDER BY o.created
                ''' 
        
        orders = {}
        for row in cur.execute(sql, (date_from, date_to, date_from, date_to, cnt)):
            if row[0] not in orders:
                orders[row[0]] = {
                    "order": {"id": row[0], "created": row[1]},
                    "user": {"id": row[2], "name": row[3], "city": row[4]},
                    "products": []
                    }
            orders[row[0]]["products"].append({"id": row[5], "name": row[6], "price": row[7]})

        orders = self._map_to_orders(orders)
        return orders

    def _map_to_orders(self, orders_dict: dict) -> Orders:
        orders = Orders()
        for key, value in orders_dict.items():
            order = Order.create_from_dict(value)
            orders.add_order(order)
        return orders

    def get_users_with_best_purchases(self, cnt: int=3) -> Users:
        cur = self._get_cursor()
        sql = '''SELECT
                    min(u.id),
                    min(u.name),
                    min(u.city),
                    sum(p.price) as sp
                 FROM order_products as op
                    LEFT JOIN orders as o ON (op.order_id = o.id)
                    LEFT JOIN users as u ON (o.user_id = u.id)
                    LEFT JOIN products as p ON (op.product_id = p.id)
                 GROUP BY u.id
                 ORDER BY sp DESC
                 LIMIT ?
                '''

        user_list = []
        for row in cur.execute(sql, (cnt, )):
            user_list.append({"id": row[0], "name": row[1], "city": row[2], "total_sales": row[3]})
        
        users = self._map_to_users(user_list)
        return users

    def _map_to_users(self, users_dict: dict) -> Users:
        users = Users()
        for u in users_dict:
            user = User.create_from_dict(u)
            users.add_user(user)
        return users

    def connect(self):
        self.connection = sqlite3.connect(self.name)

    def _get_cursor(self):
        if not self.connection:
            self.connect()
        return self.connection.cursor()

    def close(self):
        try:
            self.__commit()
        finally:
            self.__close_database()

    def recreate_database(self):
        self.drop_database()
        self.create_database()

    def drop_database(self):
        if os.path.exists(self.name):
            os.remove(self.name)

    def create_database(self):
        cur = self._get_cursor()
        cur.execute('''CREATE TABLE users 
            (id integer NOT NULL PRIMARY KEY, name string, city text)
            ''')
        cur.execute('''CREATE TABLE products
            (id integer NOT NULL PRIMARY KEY, name string, price real)
            ''')
        cur.execute('''CREATE TABLE orders 
            (id integer NOT NULL PRIMARY KEY, created string, user_id integer,
            FOREIGN KEY(user_id) REFERENCES users(id))
            ''')
        cur.execute('''CREATE TABLE order_products
            (order_id integer NOT NULL, product_id NOT NULL,
            PRIMARY KEY(order_id, product_id),
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id))
            ''')
        self.__commit()

    def __commit(self):
        self.connection.commit()

    def __close_database(self):
        self.connection.close()
