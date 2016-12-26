import Utils.DateConverter as dateConv
from Model.Currency import Currency
from Model.Stock import Stock


class World:
    def __init__(self):
        self.__currencies = {}  # key - id, value - currency
        self.__stocks = {}  # key - id , value - stock
        self.__current_day = None

    def set_start_date(self, start_date_str):
        self.__current_day = dateConv.to_date(start_date_str)

    def next_day(self):
        self.__current_day = dateConv.next_day(dateConv.to_str(self.__current_day))

    def add_currency(self, name, abbreviation, currency_id):
        self.__currencies[currency_id] = Currency(name, abbreviation, currency_id)

    def add_currency_rate(self, symbol_id, date_str, rate):
        currency_upgaded = self.__currencies.get(symbol_id)
        if currency_upgaded is None:
            raise ValueError("Trying to update a non existing currency, Sir")
        currency_upgaded.add_exchange_rate(date_str, rate)

    def get_currency_rate(self, symbol_id, date_str):
        currency_viewed = self.__currencies.get(symbol_id)
        if currency_viewed is None:
            raise ValueError("Trying to access rate for void currency is forbidden, Sir")
        return currency_viewed.get_exchange_rate(date_str)

    def get_currency_rate_now(self, symbol_id):
        return self.get_currency_rate(symbol_id, dateConv.to_str(self.__current_day))

    def add_stock(self, stock_name, curr_abbrev, stock_id):
        self.__stocks[stock_id] = Stock(stock_name, curr_abbrev, stock_id)

    def add_stock_price(self, symbol_id, date_str, price):
        stock_updated = self.__stocks.get(symbol_id)
        if stock_updated is None:
            raise ValueError("Trying to update a non existing stock, Sir")
        stock_updated.add_exchange_price(date_str, price)

    def get_stock_price(self, symbol_id, date_str):
        stock_viewed = self.__stocks.get(symbol_id)
        if stock_viewed is None:
            raise ValueError("Trying to view a void stock is forbidden, Sir")
        return stock_viewed.get_exchange_price(date_str)

    def get_stock_price_now(self, symbol_id):
        return self.get_stock_price(symbol_id, dateConv.to_str(self.__current_day))

