from enum import Enum


class Event:
    def __init__(self, type, date_str, name, change):
        self.type = type
        self.date_str = date_str
        self.name = name
        self.change = change


class EventType(Enum):
    STOCK = 1
    CURRENCY = 2
