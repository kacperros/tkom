from datetime import datetime


def to_str(date):
    return date.strftime("%Y.%m.%d")


def to_date(date_str):
    return datetime.strptime(date_str, "%Y.%m.%d").date()