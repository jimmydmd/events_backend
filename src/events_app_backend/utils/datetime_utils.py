from datetime import datetime, time

DEFAULT_START_TIME = time(10, 0)
DEFAULT_END_TIME = time(18, 0)

def normalize_event_dates(start_date: datetime, end_date: datetime) -> tuple[datetime, datetime]:
    if start_date.time() == time(0, 0):
        start_date = datetime.combine(start_date.date(), DEFAULT_START_TIME)
    if end_date.time() == time(0, 0):
        end_date = datetime.combine(end_date.date(), DEFAULT_END_TIME)
    return start_date, end_date
