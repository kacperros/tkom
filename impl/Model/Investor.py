

class Investor:
    def __init__(self):
        self.__stocks = {}
        self.__currencies = {}

    def add_currency(self, curr_abbrev, amount):
        added = self.__currencies.get(curr_abbrev)
        if added is None:
            self.__currencies[curr_abbrev] = amount
        else:
            self.__currencies[curr_abbrev] += amount

    def has_currency(self, curr_abbrev):
        curr = self.__currencies.get(curr_abbrev)
        if curr is None:
            raise ValueError("No such currency, can't perform, Sir")
        else:
            return curr

    def rem_currency(self, curr_abbrev, amount):
        curr = self.__currencies.get(curr_abbrev)
        if curr is None:
            raise ValueError("No such currency, can't perform, Sir")
        else:
            self.__currencies[curr_abbrev] -= amount

    def add_stock(self, stock_name, amount):
        added = self.__stocks.get(stock_name)
        if added is None:
            self.__currencies[stock_name] = amount
        else:
            self.__currencies[stock_name] += amount

    def has_stock(self, stock_name):
        stock = self.__currencies.get(stock_name)
        if stock is None:
            raise ValueError("No such currency, can't perform, Sir")
        else:
            return stock

    def rem_stock(self, stock_name, amount):
        stock = self.__currencies.get(stock_name)
        if stock is None:
            raise ValueError("No such currency, can't perform, Sir")
        else:
            self.__stocks[stock_name] -= amount
