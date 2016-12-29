from random import randint

import Utils.DateConverter as dateConv


class World:
    def __init__(self):
        self.__currencies = {}  # key - id, value - currency
        self.__stocks = {}  # key - id , value - stock
        self.current_day = None

    def set_start_date(self, start_date_str):
        self.current_day = dateConv.to_date(start_date_str)

    def next_day(self):
        self.current_day = dateConv.next_day(dateConv.to_str(self.current_day))

    def add_currency(self, currency):
        self.__currencies[currency.id] = currency

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
        return self.get_currency_rate(symbol_id, dateConv.to_str(self.current_day))

    def add_stock(self, stock):
        self.__stocks[stock.id] = stock

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
        return self.get_stock_price(symbol_id, dateConv.to_str(self.current_day))

    def get_stock_currency_id(self, stock_id):
        stock = self.__stocks.get(stock_id)
        if stock is None:
            raise ValueError("Trying to access currency for nonexistant stock, Sir")
        return stock.currency_id

    def get_random_currency_id(self):
        length = len(self.__currencies) - 1
        return randint(0, length)

    def get_random_stock_id(self):
        length = len(self.__stocks) - 1
        return randint(0, length)

    def get_currencies(self):
        return self.__currencies

    def get_stocks(self):
        return self.__stocks
