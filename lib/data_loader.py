import gzip


class DataLoader():

    def load_from_file(self, filename: str) -> str:
        orders = []

        with gzip.open(filename, 'rb') as f:
            for line in f:
                orders.append(line)

        return orders
