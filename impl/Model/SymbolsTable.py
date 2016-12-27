class SymbolsTable:
    def __init__(self):
        self.currencies = {}  # keys - abbreviations, values - id
        self.__currencies_counter = 0
        self.stocks = {}       # keys - names, values - id
        self.__stocks_counter = 0
        self.__rule_ids = {}

    def add_currency(self, abbrev):
        id_checked = self.currencies.get(abbrev)
        if id_checked is None:
            self.currencies[abbrev] = self.__currencies_counter
            self.__currencies_counter += 1
            return self.__currencies_counter - 1
        else:
            raise ValueError("You are trying to add an already existing element, Sir, " + abbrev)

    def get_currency(self, abbrev):
        id_ret = self.currencies.get(abbrev)
        if id_ret is None:
            raise ValueError("No currency was defined for " + abbrev + " ,Sir")
        else:
            return id_ret

    def add_stock(self, name):
        id_checked = self.stocks.get(name)
        if id_checked is None:
            self.stocks[name] = self.__stocks_counter
            self.__stocks_counter += 1
            return self.__stocks_counter - 1
        else:
            raise ValueError("You are trying to add an already existing element, Sir, " + name)

    def get_stock(self, name):
        id_ret = self.stocks.get(name)
        if id_ret is None:
            raise ValueError("No stock was defined for " + name + " ,Sir")
        else:
            return id_ret

    def is_rule_id_busy(self, rule_id):
        id_checked = self.__rule_ids.get(rule_id)
        if id_checked is None:
            return False
        else:
            return True

    def add_rule_id(self, rule_id):
        id_cheched = self.__rule_ids.get(rule_id)
        if id_cheched is not None:
            raise ValueError("Rule Id " + str(rule_id) + " is already taken, Sir")
        else:
            self.__rule_ids[id_cheched] = rule_id
