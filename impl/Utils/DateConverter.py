from datetime import datetime, timedelta


def to_str(date):
    return date.strftime("%Y.%m.%d")


def to_date(date_str):
    return datetime.strptime(date_str, "%Y.%m.%d").date()


def next_day(date_str):
    return datetime.strptime(date_str, "%Y.%m.%d").date() + timedelta(1)


def next_day_str(date_str):
    return to_str(next_day(date_str))
