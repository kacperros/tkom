import xml.etree.ElementTree as ET
from Model.Currency import Currency
from Model.Stock import Stock


def parse_currencies(currencies, symbol_table):
    counter = 0
    result = []
    for currency in currencies.iter('currency'):
        name_elem = currency.find('name')
        abbrev_elem = currency.find('abbreviation')
        if name_elem is None:
            raise ValueError("Sir, I can not load this file, currency " + str(counter) + "is missing its name")
        elif abbrev_elem is None:
            raise ValueError("Sir, I can not load this file, currency " + str(counter) + "is missing its abbreviation")
        elif name_elem.text == "" or abbrev_elem.text == "":
            raise ValueError(
                "Sir, I can not load this file, currency " + str(counter) + "it can not have empty elements")
        else:
            currency_id = symbol_table.add_currency(abbrev_elem.text)
            result.append(Currency(name_elem.text, abbrev_elem.text, currency_id))
        counter += 1
    return result


def parse_stocks(stocks, symbol_table):
    counter = 0
    result = []
    for stock in stocks.iter('stock'):
        name_elem = stock.find('name')
        currency_elem = stock.find('currency')
        if name_elem is None:
            raise ValueError("Sir, I can not load this file, stock " + str(counter) + "is missing its name")
        elif currency_elem is None:
            raise ValueError("Sir, I can not load this file, stock " + str(counter) + "is missing its currency")
        elif name_elem.text == "" or currency_elem.text == "":
            raise ValueError(
                "Sir, I can not load this file, currency " + str(counter) + "it can not have empty elements")
        else:
            stock_id = symbol_table.add_stock(name_elem.text)
            currency_id = symbol_table.get_currency(currency_elem.text)
            result.append(Stock(name_elem.text, currency_id, stock_id))
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
            print('I am warning you Sir: A second level tag ' + child.tag + ' is forbidden in file ' + file_name)
    return {'currencies': currencies, 'stocks': stocks}
