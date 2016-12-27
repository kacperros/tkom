from Model.World import World
from Model.Investor import Investor
from Engine.EventWorldAdapter import EventWorldAdapter
from Engine.StartInvestorAdapter import StartInvestorAdapter


class RealityController:
    def __init__(self):
        self.world = World()
        self.investor = Investor()
        self.event_world_adapter = EventWorldAdapter(self.world)
        self.start_investor_adapter = StartInvestorAdapter(self.investor)

    def add_event(self, event):
        self.event_world_adapter.add_event(event)

    def add_start_condition(self, start_cond):
        self.start_investor_adapter.add_start_cond(start_cond)

    def add_currency(self, currency):
        self.world.add_currency(currency)

    def add_stock(self, stock):
        self.world.add_stock(stock)
