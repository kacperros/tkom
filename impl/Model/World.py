import Utils.DateConverter as dateConv
from Model.Currency import Currency
from Model.Stock import Stock


class World:
    def __init__(self, start_date_str):
        self.__currencies = {}
        self.__stocks = {}
        self.__current_day = dateConv.to_date(start_date_str)

    def add_currency(self, name, abbreviation):
        current_currency = self.__currencies.get(abbreviation)
        if current_currency is not None:
            raise ValueError("Trying to redefine, an already existing currency is forbidden, Sir")
        self.__currencies[abbreviation] = Currency(name, abbreviation)

    def add_currency_rate(self, curr_abbrev, date_str, rate):
        currency_upgaded = self.__currencies.get(curr_abbrev)
        if currency_upgaded is None:
            raise ValueError("Trying to update a non existing currency, Sir")
        currency_upgaded.add_exchange_rate(date_str, rate)

    def get_currency_rate(self, curr_abbrev, date_str):
        currency_viewed = self.__currencies.get(curr_abbrev)
        if currency_viewed is None:
            raise ValueError("Trying to access rate for void currency is forbidden, Sir")
        return currency_viewed.get_exchange_rate(date_str)

    def get_currency_rate_now(self, curr_abbrev):
        return self.get_currency_rate(curr_abbrev, self.__current_day)

    def add_stock(self, stock_name, stock_abbrev, curr_abbrev):
        stock_added = self.__stocks.get(stock_name)
        if stock_added is not None:
            raise ValueError("Trying to redefine an already existing stock is forbidden, Sir")
        self.__stocks[stock_name] = Stock(stock_name, stock_abbrev, curr_abbrev)

    def add_stock_price(self, stock_name, date_str, price):
        stock_updated = self.__stocks.get(stock_name)
        if stock_updated is None:
            raise ValueError("Trying to update a non existing stock, Sir")
        stock_updated.add_exchange_price(date_str, price)

    def get_stock_price(self, stock_name, date_str):
        stock_viewed = self.__stocks.get(stock_name)
        if stock_viewed is None:
            raise ValueError("Trying to view a void stock is forbidden, Sir")
        return stock_viewed.get_exchange_price(date_str)

    def get_stock_price_now(self, stock_name):
        return self.get_stock_price(stock_name, self.__current_day)

