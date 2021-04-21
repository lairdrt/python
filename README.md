# python
Python snippets
## Pausable Timer
Use case:
```
import time
t = PausableTimer()
time.sleep(4.0)
print(t.elapsed())
t.pause()
time.sleep(3.0)
print(t.elapsed())
t.resume()
time.sleep(2.0)
print(t.elapsed())
```
## Sunrise/Sunset Calculation
Use case:
```
import dateutil.tz as tz

lon = 0.0
tzoffset = 0.0
tzone = tz.gettz('UTC')
dt = datetime(year=2021, month=6, day=1, hour=12, minute=00, second=00, tzinfo=tzone)
print("dt = " + str(dt))
for lat in range(-90, 91):
    try:
        sunrise, sunset = sunrise_sunset(lat, lon, dt, tzoffset)
        print("Sunrise is at " + sunrise.strftime("%m-%d-%Y %H:%M:%S"))
        print("Sunset is at  " + sunset.strftime("%m-%d-%Y %H:%M:%S"))
    except SunriseException:
        print("No sunrise at " + str(lat))
    except SunsetException:
        print("No sunset at " + str(lat))
dt = datetime(year=2021, month=12, day=31, hour=12, minute=00, second=00, tzinfo=tzone)
print("dt = " + str(dt))
for lat in range(-90, 91):
    try:
        sunrise, sunset = sunrise_sunset(lat, lon, dt, tzoffset)
        print("Sunrise is at " + sunrise.strftime("%m-%d-%Y %H:%M:%S"))
        print("Sunset is at  " + sunset.strftime("%m-%d-%Y %H:%M:%S"))
    except SunriseException:
        print("No sunrise at " + str(lat))
    except SunsetException:
        print("No sunset at " + str(lat))
```
