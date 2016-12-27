from Model.Event import EventType


class EventWorldAdapter:
    def __init__(self, world):
        self.world = world

    def add_event(self, event):
        if event.event_type == EventType.CURRENCY.name:
            self.__add_currency_event(event)
        elif event.event_type == EventType.STOCK.name:
            self.__add_stock_event(event)
        else:
            raise ValueError("Event type is not present in system, Sir")

    def __add_currency_event(self, event):
        self.world.add_currency_rate(event.symbol_id, event.date_str, event.value)

    def __add_stock_event(self, event):
        self.world.add_stock_price(event.symbol_id, event.date_str, event.value)
