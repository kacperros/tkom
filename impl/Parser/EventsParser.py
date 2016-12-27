import xml.etree.ElementTree as ET
from Model.Event import Event
from Model.Event import EventType
import Utils.DateConverter as dateConv


def parse_file(file_name, symbol_table):
    events = []
    tree = ET.parse(file_name)
    root = tree.getroot()
    counter = 0
    for child in root:
        if child.tag == 'event':
            event = parse_event(child, symbol_table, file_name, counter)
            events.append(event)
            counter += 1
    return events


def parse_event(event_elem, symbol_table, file_name, counter):
    event_type = event_elem.find('type')
    event_name = event_elem.find('name')
    event_value = event_elem.find('value')
    event_date = event_elem.find('date')
    if event_type is None or event_name is None or event_value is None or event_date is None:
        raise ValueError(
            "An event must consist of name, type, value, date elements, one is missing in " + file_name + " at " + str(
                counter) + " , Sir")
    if event_type.text == "" or event_name.text == "" or event_value.text == "" or event_date.text == "":
        raise ValueError(
            "An event must consist of name, type, value, date elements, one is empty in " + file_name + " at " + str(
                counter) + " , Sir")
    symbol_id = None
    if event_type.text == EventType.CURRENCY.name:
        symbol_id = symbol_table.get_currency(event_name.text)
    elif event_type.text == EventType.STOCK.name:
        symbol_id = symbol_table.get_stock(event_name.text)
    else:
        raise ValueError("Terribly sorry Sir, but type must be CURRENCY or STOCK in " + file_name + " at " + str(
            counter))
    if not dateConv.is_date_str_valid_format(event_date.text):
        raise ValueError(
            "Terribly sorry Sir, but date format is incorrect. It should be yyyy.MM.dd in " + file_name + " at " + str(
                counter))
    return Event(event_type.text, event_date.text, symbol_id, event_value.text)
