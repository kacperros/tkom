from enum import Enum


class Event:
    def __init__(self, event_type, date_str, name, value):
        self.event_type = event_type
        self.date_str = date_str
        self.name = name
        self.value = value


class EventType(Enum):
    STOCK = 1
    CURRENCY = 2
