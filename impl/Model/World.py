import Utils.DateConverter as dateConv
from Model.Currency import Currency
from Model.Stock import Stock
from Model.Event import EventType


class World:
    def __init__(self, symbols_table):
        self.__currencies = {}  # key - id, value - currency
        self.__stocks = {}  # key - id , value - stock
        self.__current_day = None
        self.symbols_table = symbols_table

    def set_start_date(self, start_date_str):
        self.__current_day = dateConv.to_date(start_date_str)

    def next_day(self):
        self.__current_day = dateConv.next_day(dateConv.to_str(self.__current_day))

    def add_currency(self, name, abbreviation):
        currency_id = self.symbols_table.add_currency(abbreviation)
        self.__currencies[currency_id] = Currency(name, abbreviation, currency_id)

    def add_currency_rate(self, curr_abbrev, date_str, rate):
        currency_upgaded = self.symbols_table.get_currency(curr_abbrev)
        if currency_upgaded == -1:
            raise ValueError("Trying to update a non existing currency, Sir")
        self.__currencies[currency_upgaded].add_exchange_rate(date_str, rate)

    def direct_add_currency_rate(self, symbol_id, date_str, rate):
        currency_upgaded = self.__currencies.get(symbol_id)
        if currency_upgaded is None:
            raise ValueError("Trying to update a non existing currency, Sir")
        currency_upgaded.add_exchange_rate(date_str, rate)

    def get_currency_rate(self, curr_abbrev, date_str):
        currency_viewed = self.symbols_table.get_currency(curr_abbrev)
        if currency_viewed == -1:
            raise ValueError("Trying to access rate for void currency is forbidden, Sir")
        return self.__currencies[currency_viewed].get_exchange_rate(date_str)

    def direct_get_currency_rate(self, symbol_id, date_str):
        currency_viewed = self.__currencies.get(symbol_id)
        if currency_viewed is None:
            raise ValueError("Trying to access rate for void currency is forbidden, Sir")
        return currency_viewed.get_exchange_rate(date_str)

    def get_currency_rate_now(self, curr_abbrev):
        return self.get_currency_rate(curr_abbrev, dateConv.to_str(self.__current_day))

    def direct_get_currency_rate_now(self, symbol_id):
        return self.direct_get_currency_rate(symbol_id, dateConv.to_str(self.__current_day))

    def add_stock(self, stock_name, curr_abbrev):
        stock_id = self.symbols_table.add_stock(stock_name)
        self.__stocks[stock_id] = Stock(stock_name, curr_abbrev, stock_id)

    def add_stock_price(self, stock_name, date_str, price):
        stock_updated_id = self.symbols_table.get_stock(stock_name)
        if stock_updated_id == -1:
            raise ValueError("Trying to update a non existing stock, Sir")
        self.__stocks[stock_updated_id].add_exchange_price(date_str, price)

    def direct_add_stock_price(self, symbol_id, date_str, price):
        stock_updated = self.__stocks.get(symbol_id)
        if stock_updated is None:
            raise ValueError("Trying to update a non existing stock, Sir")
        stock_updated.add_exchange_price(date_str, price)

    def get_stock_price(self, stock_name, date_str):
        stock_viewed_id = self.symbols_table.get_stock(stock_name)
        if stock_viewed_id == -1:
            raise ValueError("Trying to view a void stock is forbidden, Sir")
        return self.__stocks[stock_viewed_id].get_exchange_price(date_str)

    def direct_get_stock_price(self, symbol_id, date_str):
        stock_viewed = self.__stocks.get(symbol_id)
        if stock_viewed is None:
            raise ValueError("Trying to view a void stock is forbidden, Sir")
        return stock_viewed.get_exchange_price(date_str)

    def get_stock_price_now(self, stock_name):
        return self.get_stock_price(stock_name, dateConv.to_str(self.__current_day))

    def direct_get_stock_price_now(self, symbol_id):
        return self.direct_get_stock_price(symbol_id, dateConv.to_str(self.__current_day))

    def add_event(self, event):
        if event.event_type == EventType.CURRENCY:
            self.__add_currency_event(event)
        elif event.event_type == EventType.STOCK:
            self.__add_stock_event(event)
        else:
            raise ValueError("Event type is not present in system, Sir")

    def __add_currency_event(self, event):
        self.add_currency_rate(event.name, event.date_str, event.value)

    def __add_stock_event(self, event):
        self.add_stock_price(event.name, event.date_str, event.value)
