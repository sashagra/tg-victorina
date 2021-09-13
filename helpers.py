import datetime
from typing import List, NamedTuple, Optional
import pytz

s = dict("ddd",)


def _get_now_formatted() -> str:
    """Возвращает текущую дату время строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_day_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны."""
    tz = pytz.timezone("Europe/Minsk")
    now = datetime.datetime.now(tz)
    return now


string_time = {
    "now": _get_now_formatted,
    "today": _get_day_formatted
}
