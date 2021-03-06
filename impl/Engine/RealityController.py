import math
import Utils.DateConverter as dC
from Engine.EventWorldAdapter import EventWorldAdapter
from Engine.StartInvestorAdapter import StartInvestorAdapter
from Model.Investor import Investor
from Model.World import World


class RealityController:
    def __init__(self):
        self.world = World()
        self.investor = Investor()
        self.event_world_adapter = EventWorldAdapter(self.world)
        self.start_investor_adapter = StartInvestorAdapter(self.investor)
        self.rules = {}

    def next_day(self):
        self.world.next_day()
        for k, v in self.rules.items():
            v.executed = False

    def add_start_cond(self, start_cond):
        self.start_investor_adapter.add_start_cond(start_cond)

    def add_event(self, event):
        self.event_world_adapter.add_event(event)

    def add_start_condition(self, start_cond):
        self.start_investor_adapter.add_start_cond(start_cond)

    def add_currency(self, currency):
        self.world.add_currency(currency)

    def add_stock(self, stock):
        self.world.add_stock(stock)

    def sell_stock_for_currency(self, stock_id, curr_amount, currency_id=None):
        stock_amount = self.investor.has_stock(stock_id)
        stock_amount_min = math.ceil(curr_amount / self.world.get_stock_price_now(stock_id))
        if stock_amount < stock_amount_min:
            return False
        else:
            self.investor.rem_stock(stock_id, stock_amount_min)
            stock_currency_id = self.world.get_stock_currency_id(stock_id)
            currency_added = stock_amount_min * self.world.get_stock_price_now(stock_id)
            self.investor.add_currency(stock_currency_id, currency_added)
            return True

    def sell_stock_amount(self, stock_id, stock_amount, currency_id=None):
        stock_amount_owned = self.investor.has_stock(stock_id)
        if stock_amount == 'ALL':
            stock_amount = stock_amount_owned
        if stock_amount_owned < stock_amount:
            return False
        else:
            self.investor.rem_stock(stock_id, stock_amount)
            stock_currency_id = self.world.get_stock_currency_id(stock_id)
            currency_added = stock_amount * self.world.get_stock_price_now(stock_id)
            self.investor.add_currency(stock_currency_id, currency_added)
            return True

    def sell_stock_part(self, stock_id, stock_part, third_arg=None):
        stock_amount_owned = self.investor.has_stock(stock_id)
        stock_part = math.ceil(stock_amount_owned * (stock_part / 100))
        self.investor.rem_stock(stock_id, stock_part)
        stock_currency_id = self.world.get_stock_currency_id(stock_id)
        currency_added = stock_part * self.world.get_stock_price_now(stock_id)
        self.investor.add_currency(stock_currency_id, currency_added)
        return True

    def buy_currency_amount(self, currency_bought_id, amount_bought, currency_sold_id):
        if amount_bought == 'MAX' and currency_sold_id != 'ANY':
            amount_bought = self.max_currency_to_buy_for_currency(currency_bought_id, currency_sold_id)
        elif amount_bought == 'MAX' and currency_sold_id == 'ANY':
            currency_sold_id = self.world.get_random_currency_id()
            amount_bought = self.max_currency_to_buy_for_currency(currency_bought_id, currency_sold_id)
        elif amount_bought != 'MAX' and currency_sold_id == 'ANY':
            currency_sold_id = self.get_currency_id_to_buy_currency_amount(amount_bought, currency_bought_id)
        fictional_amount_bought = amount_bought / self.world.get_currency_rate_now(currency_bought_id)
        currency_sold_amount = round(fictional_amount_bought * self.world.get_currency_rate_now(currency_sold_id), 2)
        currency_sold_owned = self.investor.has_currency(currency_sold_id)
        if currency_sold_amount > currency_sold_owned:
            return False
        else:
            self.investor.rem_currency(currency_sold_id, currency_sold_amount)
            self.investor.add_currency(currency_bought_id, amount_bought)
            return True

    def buy_stock_amount(self, stock_id, stock_amount, currency_id):
        if currency_id == 'OWN':
            currency_id = self.world.get_stock_currency_id(stock_id)
        if stock_amount == 'MAX' and currency_id != 'ANY':
            stock_amount = self.max_stock_to_buy_for_currency(stock_id, currency_id)
        elif stock_amount == 'MAX' and currency_id == 'ANY':
            stock_amount = self.max_stock_to_buy_for_currency(stock_id, self.world.get_random_currency_id())
        elif stock_amount != 'MAX' and currency_id == 'ANY':
            currency_id = self.get_currency_id_to_buy_stock_amount(stock_id, stock_amount)
        currency_owned = self.investor.has_currency(currency_id)
        currency_needed = round(self.world.get_stock_price_now(stock_id) * stock_amount, 2)
        if currency_id != self.world.get_stock_currency_id(stock_id):
            stock_currency_id = self.world.get_stock_currency_id(stock_id)
            currency_needed = round((currency_needed / self.world.get_currency_rate_now(
                stock_currency_id)) * self.world.get_currency_rate_now(currency_id), 2)
        if currency_owned < currency_needed:
            return False
        else:
            self.investor.rem_currency(currency_id, currency_needed)
            self.investor.add_stock(stock_id, stock_amount)

    def max_stock_to_buy_for_currency(self, stock_bought_id, currency_id):
        if currency_id == -1:
            currency_id = self.world.get_random_currency_id()
        stock_currency_id = self.world.get_stock_currency_id(stock_bought_id)
        stock_price_in_owned_currency = (self.world.get_stock_price_now(
            stock_bought_id) / self.world.get_currency_rate_now(stock_currency_id)) * self.world.get_currency_rate_now(
            currency_id)
        owned_currency_amount = self.investor.has_currency(currency_id)
        return math.floor(owned_currency_amount / stock_price_in_owned_currency)

    def max_currency_to_buy_for_currency(self, currency_bought_id, currency_sold_id):
        if currency_sold_id == -1:
            currency_sold_id = self.world.get_random_currency_id()
        currency_owned_amount = self.investor.has_currency(currency_sold_id)
        return (currency_owned_amount / self.world.get_currency_rate_now(
            currency_sold_id)) * self.world.get_currency_rate_now(currency_bought_id)

    def get_currency_id_to_buy_stock_amount(self, stock_id, stock_amount):
        for k, v in self.world.get_currencies().items():
            stocks = self.max_stock_to_buy_for_currency(stock_id, k)
            if stocks > stock_amount:
                return k

    def get_currency_id_to_buy_currency_amount(self, currency_amount, currency_id):
        for k, v in self.world.get_currencies().items():
            if k == currency_id:
                continue
            currency_amount_buyable = self.max_currency_to_buy_for_currency(currency_id, k)
            if currency_amount_buyable > currency_amount:
                return k

    def run_reality(self, date_start, date_stop):
        rules_list = list(self.rules.values())
        rules_list.sort(key=lambda x: x.priority, reverse=True)
        self.world.set_start_date(date_start)
        while True:
            for rule in rules_list:
                rule.execute()
            if dC.to_str(self.world.current_day) == date_stop:
                break
            else:
                self.next_day()
