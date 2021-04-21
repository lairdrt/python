# Adapted from:
# https://en.wikipedia.org/wiki/Sunrise_equation
# https://steemit.com/steemstem/@procrastilearner/killing-time-with-recreational-math-calculate-sunrise-and-sunset-times-using-python
# https://gist.github.com/jiffyclub/1294443

# See also:
# https://www.esrl.noaa.gov/gmd/grad/solcalc/
# https://www.esrl.noaa.gov/gmd/grad/solcalc/calcdetails.html

from datetime import datetime, timedelta
import math

def date_to_jd(year, month, day):
    """
    Converts a date (yyyy/mm/dd) to its equivalent Julian day.
    :param year: Year as integer. Years preceding 1 A.D. should be 0 or negative.
        The year before 1 A.D. is 0, 10 B.C. is year -9.
    :param month: Month as integer, Jan = 1, Feb. = 2, etc.
    :param day: Day, may contain fractional part.
    :return: Julian day as a decimal number
    """    
    if month == 1 or month == 2:
        yearp = year - 1
        monthp = month + 12
    else:
        yearp = year
        monthp = month
    if ((year < 1582) or
        (year == 1582 and month < 10) or
        (year == 1582 and month == 10 and day < 15)):
        B = 0
    else:
        A = math.trunc(yearp / 100.)
        B = 2 - A + math.trunc(A / 4.)
    if yearp < 0:
        C = math.trunc((365.25 * yearp) - 0.75)
    else:
        C = math.trunc(365.25 * yearp)
    D = math.trunc(30.6001 * (monthp + 1))
    jd = B + C + D + day + 1720994.5
    return jd    

class SunriseException(Exception):
    def __init__(self):
        super().__init__('The sun never rises on this location (on this date)')

class SunsetException(Exception):
    def __init__(self):
        super().__init__('The sun never sets on this location (on this date)')

def sunrise_sunset(lat_deg, lon_deg, dt, tzoffset):
    """
    Calculate sunrise and sunset for given date and timezone (offset).
    :param lat_deg: Latitude in decimal degrees
    :param lon_deg: Longitude in decimal degrees
    :param dt: Reference date (datetime object)
    :param tzoffset: Timezone offset (e.g., -7.0) associated with reference date
    :return: UTC sunrise,sunset datetime naive
    :raises: SunriseException when there is no sunrise on given location and date
    :raises: SunsetException when there is no sunset on given location and date
    """    
    lat = math.radians(lat_deg)

    jd2000 = 2451545 # the julian date for Jan 1 2000 at noon

    jd_now = date_to_jd(dt.year, dt.month, dt.day)

    n = jd_now - jd2000 + 0.0008

    jstar = n - lon_deg/360

    M_deg = math.fmod(357.5291 + 0.98560028 * jstar, 360)
    M = math.radians(M_deg)

    C = 1.9148 * math.sin(M) + 0.0200 * math.sin(2*M) + 0.0003 * math.sin(3*M)

    lamda_deg = math.fmod(M_deg + C + 180 + 102.9372, 360)
    lamda = math.radians(lamda_deg)

    Jtransit = 2451545.5 + jstar + 0.0053 * math.sin(M) - 0.0069 * math.sin(2*lamda)

    earth_tilt_deg = 23.44
    earth_tilt = math.radians(earth_tilt_deg)

    sin_delta = math.sin(lamda) * math.sin(earth_tilt)
    angle_delta = math.asin(sin_delta)

    sun_disc_deg = -0.83
    sun_disc = math.radians(sun_disc_deg)

    cos_omega = (math.sin(sun_disc) - math.sin(lat) * math.sin(angle_delta))/(math.cos(lat) * math.cos(angle_delta))

    if cos_omega > 1.0:
        raise SunriseException
    elif cos_omega < -1.0:
        raise SunsetException

    omega = math.acos(cos_omega)
    omega_degrees = math.degrees(omega)

    Jrise = Jtransit - omega_degrees/360
    numdays = Jrise - jd2000
    numdays = numdays + 0.5 # offset because Julian dates start at noon
    numdays = numdays + tzoffset/24 # offset for time zone
    sunrise = datetime(2000, 1, 1) + timedelta(numdays)

    Jset = Jtransit + omega_degrees/360
    numdays = Jset - jd2000
    numdays = numdays + 0.5 # offset because Julian dates start at noon
    numdays = numdays + tzoffset/24 # offset for time zone
    sunset = datetime(2000, 1, 1) + timedelta(numdays)

    return sunrise, sunset
