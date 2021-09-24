from lib.entity import *
from lib.sqlite import Sqlite
from lib.orders_service import OrdersService


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
    #d.recreate_database()
    d.connect()
    order_service = OrdersService(DATA_FILE_NAME, d)
    #order_service.load_data()
    
    orders = order_service.database.get_orders_for_date('2018-10-01', '2018-10-31')
    print_orders(orders)

    users = order_service.database.get_users_with_best_purchases()
    print_users(users)
    d.close()


__main__()
