class Investor:
    def __init__(self):
        self.__stocks = {}
        self.__currencies = {}

    def add_currency(self, curr_id, amount):
        added = self.__currencies.get(curr_id)
        if added is None:
            self.__currencies[curr_id] = amount
        else:
            self.__currencies[curr_id] += amount

    def has_currency(self, curr_id):
        curr = self.__currencies.get(curr_id)
        if curr is None:
            return 0
        else:
            return curr

    def rem_currency(self, curr_id, amount):
        curr = self.__currencies.get(curr_id)
        if curr is None or curr < amount:
            return False
        else:
            self.__currencies[curr_id] -= amount
            return True

    def add_stock(self, stock_id, amount):
        added = self.__stocks.get(stock_id)
        if added is None:
            self.__stocks[stock_id] = amount
        else:
            self.__stocks[stock_id] += amount

    def has_stock(self, stock_id):
        stock = self.__stocks.get(stock_id)
        if stock is None:
            return 0
        else:
            return stock

    def rem_stock(self, stock_id, amount):
        stock = self.__stocks.get(stock_id)
        if stock is None or stock < amount:
            return False
        else:
            self.__stocks[stock_id] -= amount
            return True

    def get_currencies(self):
        return self.__currencies

    def get_stocks(self):
        return self.__stocks
