from datetime import datetime, timedelta


def to_str(date):
    return date.strftime("%Y.%m.%d")


def to_date(date_str):
    return datetime.strptime(date_str, "%Y.%m.%d").date()


def next_day(date_str):
    return datetime.strptime(date_str, "%Y.%m.%d").date() + timedelta(1)


def next_day_str(date_str):
    return to_str(next_day(date_str))


def get_date_back_x(date_str, x):
    return datetime.strptime(date_str, "%Y.%m.%d").date() - timedelta(x)


def get_date_str_back_x(date_str, x):
    return to_str(get_date_back_x(date_str, x))


def is_date_str_valid_format(date_str):
    try:
        datetime.strptime(date_str, "%Y.%m.%d").date()
        return True
    except ValueError:
        return False


def after(date_str_first, date_str_second):
    return to_date(date_str_first) <  to_date(date_str_second)
