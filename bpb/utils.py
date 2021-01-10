from datetime import datetime, timedelta

from dateutil import parser as dateutil_parser


def parse_date(date_args):
    if isinstance(date_args, (list, tuple)):
        date_args = " ".join(date_args)
    elif isinstance(date_args, datetime):
        date_args = str(date_args)
    datetime_obj = dateutil_parser.parse(date_args)
    parsed_date = datetime_obj.strftime("%A %Hh, %d %b %Y")
    return parsed_date, datetime_obj


def get_meeting_range(date_args):

    # Get message meeting and following ones
    parsed_date, datetime_obj = parse_date(date_args)
    next_meetings, interval = [
        (parsed_date, datetime_obj),
    ], 7
    for _ in range(3):
        next_meetings.append(parse_date(datetime_obj + timedelta(days=interval)))
        interval += interval

    return parsed_date, datetime_obj, next_meetings