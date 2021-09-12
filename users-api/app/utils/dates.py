
from datetime import datetime, timezone, timedelta


def now():
    hours_diference = timedelta(hours=-3)
    time_zone = timezone(hours_diference)
    return datetime.now().astimezone(time_zone).strftime("%d/%m/%Y - %H:%M:%S")
