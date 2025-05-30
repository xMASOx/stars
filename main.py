from skyfield.api import load
from skyfield.framelib import ecliptic_frame
import datetime

START_YEAR = 1851
END_YEAR = 2025
STEP_DAYS = 1  # Более точный шаг

ts = load.timescale()
eph = load('de440s.bsp')

earth = eph['earth']
moon = eph['moon']

def get_moon_ecliptic_lat(t):
    """Возвращает эклиптическую широту Луны (в градусах)"""
    lat, lon, distance = earth.at(t).observe(moon).apparent().frame_latlon(ecliptic_frame)
    return lat.degrees


def find_ascending_nodes():
    ascending_dates = []

    previous_lat = None
    previous_t = None

    for year in range(START_YEAR, END_YEAR + 1):
        for day_of_year in range(1, 366, STEP_DAYS):
            try:
                t = ts.utc(year, 1, day_of_year)
            except:
                continue

            lat = get_moon_ecliptic_lat(t)

            if previous_lat is not None and previous_lat < 0 and lat > 0:
                # Найден восходящий узел (пересечение эклиптики снизу вверх)
                date = t.utc_datetime().date()
                ascending_dates.append(date)

            previous_lat = lat
            previous_t = t

    return ascending_dates

# Найти восходящие узлы
ascending_nodes = find_ascending_nodes()

# Посчитать интервалы между узлами
intervals = []
for i in range(len(ascending_nodes) - 1):
    delta = (ascending_nodes[i + 1] - ascending_nodes[i]).days
    intervals.append((ascending_nodes[i].year, delta))

# Вывести последние 20 записей
print(f"Найдено узлов: {len(ascending_nodes)}")
for year, days_diff in intervals[-20:]:
    print(f"Год: {year}, Интервал между узлами: {days_diff} дней")

