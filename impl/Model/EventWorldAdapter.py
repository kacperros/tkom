from Model.Event import EventType


class EventWorldAdapter:
    def __init__(self, world, symbols_table):
        self.world = world
        self.symbols_table = symbols_table

    def add_event(self, event):
        if event.event_type == EventType.CURRENCY:
            self.__add_currency_event(event)
        elif event.event_type == EventType.STOCK:
            self.__add_stock_event(event)
        else:
            raise ValueError("Event type is not present in system, Sir")

    def __add_currency_event(self, event):
        currency_id = self.symbols_table.get_currency(event.name)
        self.world.add_currency_rate(currency_id, event.date_str, event.value)

    def __add_stock_event(self, event):
        stock_id = self.symbols_table.get_stock(event.name)
        self.world.add_stock_price(stock_id, event.date_str, event.value)
