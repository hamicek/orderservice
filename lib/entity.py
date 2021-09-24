class User():
    def __init__(self, user_id: int, name: str, city: str):
        self.user_id = user_id
        self.name = name
        self.city = city
        self.total_sales = 0

    @classmethod
    def create_from_dict(cls, data: dict):
        user = User(data['id'], data['name'], data['city'])
        if 'total_sales' in data:
            user.total_sales = data['total_sales']
        return user


class Product():
    def __init__(self, product_id: int, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price

    @classmethod
    def create_from_dict(cls, data: dict):
        return Product(data["id"], data["name"], data["price"])


class Order():
    def __init__(self, order_id: int, created: str, user: User):
        self.order_id = order_id
        self.created = created
        self.user = user
        self.products = Products()

    def add_product(self, product: Product):
        self.products.add_product(product)

    @classmethod
    def create_from_dict(cls, data: dict):
        user = User.create_from_dict(data["user"])
        products = Products()
        order = Order(data['order']['id'], data['order']['created'], user)
        for p in data['products']:
            product = Product.create_from_dict(p)
            order.add_product(product)
        return order


class Users(list):
    def add_user(self, user: User):
        self.append(user)


class Products(list):
    def add_product(self, product: Product):
        self.append(product)


class Orders(list):
    def add_order(self, order: Order):
        self.append(order)
