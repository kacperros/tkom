import sys
from Engine.Engine import Engine
import Utils.DateConverter as dateConv

file_name = sys.argv[1]
start_date = sys.argv[2]
end_date = sys.argv[3]
if not dateConv.is_date_str_valid_format(start_date):
    raise ValueError('Date format for start date is not acceptable Sir. It should be yyyy.MM.dd')
if not dateConv.is_date_str_valid_format(end_date):
    raise ValueError('Date format for end date is not acceptable Sir. It should be yyyy.MM.dd')
if not dateConv.after(start_date, end_date):
    raise ValueError('Date of simulation start should be before date of simulation end, Sir')
parsed_file = open(file_name)
engine = Engine(start_date, end_date, parsed_file)
engine.invest()
