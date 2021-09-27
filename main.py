from lib.entity import *
from lib.sqlite import Sqlite
from lib.orders_service import OrdersService
from lib.data_loader import DataLoader
from datetime import datetime


DATA_FILE_NAME = "data.ndjson.gz"
DATABASE_NAME = "orders.db"


def print_orders(orders: Orders):
    print('ORDERS:')
    print('==================================')
    for o in orders:
        print('ORDER: %s, %s' % (o.order_id, o.created))
        print('USER: %s, %s, %s' % (o.user.user_id, o.user.name, o.user.city))
        print('PRODUCTS:')
        for p in o.products:
            print('  > %s, %s, %s' % (p.product_id, p.name, p.price))
    print('==================================')


def print_users(users: Users):
    print('USERS MAX SALES:')
    print('==================================')
    for u in users:
        print('%s, %s, %s, %s' % (u.user_id, u.name, u.city, u.total_sales))
    print('==================================')


def __main__():
    d = Sqlite(DATABASE_NAME)
    d.recreate_database()
    d.connect()

    data_loader = DataLoader()
    orders = data_loader.load_from_file(DATA_FILE_NAME)

    order_service = OrdersService(d)
    order_service.load_data(orders)
    
    date_from = datetime.strptime('2018-10-01', "%Y-%m-%d")
    date_to = datetime.strptime('2018-10-31', "%Y-%m-%d")
    orders = order_service.storage.get_orders_for_date(date_from, date_to)
    print_orders(orders)

    users = order_service.storage.get_users_with_best_purchases()
    print_users(users)
    d.close()


__main__()
