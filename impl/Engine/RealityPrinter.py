def print_reality(reality_controller, symbol_table):
    stocks = combine_maps(symbol_table.stocks, reality_controller.investor.get_stocks())
    currencies = combine_maps(symbol_table.currencies, reality_controller.investor.get_currencies())
    print_investor_map(stocks, 'Stocks owned')
    print_investor_map(currencies, 'Currencies owned')


def combine_maps(stocks_sym, stocks_inv):
    result = {}
    for k, v in stocks_sym.items():
        item = stocks_inv.get(v)
        if item is None:
            continue
        result[k] = round(item, 2)
    return result


def print_investor_map(map_printed, header):
    print(header)
    for k, v in map_printed.items():
        print("Owned " + str(k) + " " + str(v))

