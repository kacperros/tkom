import Utils.DateConverter as dateConv
from datetime import timedelta


class Stock:
    def __init__(self, name, abbreviation, currency_abbreviation):
        self.name = name
        self.abbreviation = abbreviation
        self.currency_abbreviation = currency_abbreviation
        self.__exchange_prices = {}
        self.__earliest_date = None

    def add_exchange_price(self, date_str, price):
        present_rate = self.__exchange_prices.get(date_str)
        if present_rate is not None:
            raise ValueError("Sir you are trying to redefine " + self.name + "on the day of " + date_str)
        else:
            self.__exchange_prices[date_str] = price
            if self.__earliest_date is None or dateConv.to_date(date_str) < self.__earliest_date:
                self.__earliest_date = dateConv.to_date(date_str)

    def get_exchange_price(self, date_str):
        asked_rate = self.__exchange_prices.get(date_str)
        if dateConv.to_date(date_str) < self.__earliest_date:
            raise ValueError("Trying to obtain non existing data, Sir")
        if asked_rate is not None:
            return asked_rate
        else:
            new_date = dateConv.to_date(date_str) - timedelta(1)
            return self.get_exchange_price(dateConv.to_str(new_date))