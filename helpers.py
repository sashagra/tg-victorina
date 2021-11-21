import datetime
import pytz


def _get_now_formatted() -> str:
    """Возвращает текущую дату время строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_day_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d")


def _get_tomorrow_day_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    tomorrow = _get_now_datetime() + datetime.timedelta(days=1)
    return tomorrow.strftime("%Y-%m-%d")


def shift_days_formatted(shift: int) -> str:
    tomorrow = _get_now_datetime() + datetime.timedelta(days=shift)
    return tomorrow.strftime("%Y-%m-%d")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны."""
    tz = pytz.timezone("Europe/Minsk")
    now = datetime.datetime.now(tz)
    return now


def compute_num_of_days(d: str) -> int:
    date_arr = d.split('-')
    aa = datetime.date(int(date_arr[0]), int(date_arr[1]), int(date_arr[2]))
    bb = datetime.date.today()
    cc = bb - aa
    if str(cc) == "0:00:00":
        return 0
    dd = str(cc).split()
    return int(dd[0])


string_time = {
    "now": _get_now_formatted,
    "today": _get_day_formatted,
    "tomorrow": _get_tomorrow_day_formatted,
}
