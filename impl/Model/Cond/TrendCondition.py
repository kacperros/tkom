from Model.Cond.Condition import Condition
import Utils.DateConverter as dateConv


class TrendCondition(Condition):
    def __init__(self, world):
        super().__init__()
        self.is_inc = False
        self.number_of_days = None
        self.growth_percent = None
        self.accessor_method = None
        self.symbol_id = None
        self.world = world
        self.is_negated = False

    def eval(self):
        result = False
        if self.is_inc is not None and self.number_of_days is not None \
                and self.growth_percent is not None and self.accessor_method is not None \
                and self.symbol_id is not None:
            current_day_str = dateConv.to_str(self.world.current_day)
            start_day_str = dateConv.get_date_str_back_x(current_day_str, self.number_of_days)
            curr_value = self.accessor_method(self.symbol_id, current_day_str)
            start_value = self.accessor_method(self.symbol_id, start_day_str)

            if self.is_inc:
                if curr_value > start_value:
                    change = (curr_value - start_value) * 100 / start_value
                    result = self.growth_percent < change
                else:
                    result = False
            elif not self.is_inc:
                if curr_value < start_value:
                    change = (start_value - curr_value) * 100 / start_value
                    result = self.growth_percent < change
                else:
                    result = False
        else:
            result = False
        if self.is_negated:
            return not result
        else:
            return result
