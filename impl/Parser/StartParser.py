import xml.etree.ElementTree as ET
from Model.StartCondition import StartCondition
from Model.Event import EventType


def parse_currencies(currencies, symbol_table):
    counter = 0
    result = []
    for currency in currencies.iter('currency'):
        name_elem = currency.find('name')
        value_elem = currency.find('value')
        if name_elem is None:
            raise ValueError("Sir, I can not load this file, currency " + str(counter) + "is missing its name")
        elif value_elem is None:
            raise ValueError("Sir, I can not load this file, currency " + str(counter) + "is missing its value")
        elif name_elem.text == "" or value_elem.text == "":
            raise ValueError(
                "Sir, I can not load this file, currency " + str(counter) + "it can not have empty elements")
        else:
            currency_id = symbol_table.get_currency(name_elem.text)
            result.append(StartCondition(EventType.CURRENCY, currency_id, float(value_elem.text)))
        counter += 1
    return result


def parse_stocks(stocks, symbol_table):
    counter = 0
    result = []
    for stock in stocks.iter('stock'):
        name_elem = stock.find('name')
        amount_elem = stock.find('amount')
        if name_elem is None:
            raise ValueError("Sir, I can not load this file, stock " + str(counter) + "is missing its name")
        elif amount_elem is None:
            raise ValueError("Sir, I can not load this file, stock " + str(counter) + "is missing its currency")
        elif name_elem.text == "" or amount_elem.text == "":
            raise ValueError(
                "Sir, I can not load this file, currency " + str(counter) + "it can not have empty elements")
        else:
            stock_id = symbol_table.get_stock(name_elem.text)
            result.append(StartCondition(EventType.STOCK, stock_id, int(amount_elem.text)))
        counter += 1
    return result


def parse_file(file_name, symbol_table):
    currencies = []
    stocks = []
    tree = ET.parse(file_name)
    root = tree.getroot()
    for child in root:
        if child.tag == 'currencies':
            currencies_added = parse_currencies(child, symbol_table)
            currencies.extend(currencies_added)
        elif child.tag == 'stocks':
            stocks_added = parse_stocks(child, symbol_table)
            stocks.extend(stocks_added)
        else:
            print('I am warning you Sir: A second level tag ' + child.tag + ' is ignored in file ' + file_name)
    return {'currencies': currencies, 'stocks': stocks}
