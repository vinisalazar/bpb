from datetime import datetime

from dateutil import parser as dateutil_parser


# Helper functions and variables
def parse_date(date_args):
    if isinstance(date_args, (list, tuple)):
        date_args = " ".join(date_args)
    elif isinstance(date_args, datetime):
        date_args = str(date_args)
    datetime_obj = dateutil_parser.parse(date_args)
    parsed_date = datetime_obj.strftime("%A %Hh, %d %b %Y")
    return parsed_date, datetime_obj
