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
