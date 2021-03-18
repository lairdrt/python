import time as ttime

# Timer that can be paused/resumed
class PausableTimer():
    def __init__(self):
        self.paused = False
        self.total = 0.0
        self.start = ttime.perf_counter()
        self.stop = self.start

    def elapsed(self):
        if self.paused:
            return self.total
        else:
            return self.total + (ttime.perf_counter()-self.start)

    def pause(self):
        if not self.paused:
            self.stop = ttime.perf_counter()
            self.total += (self.stop - self.start)
            self.paused = True
    
    def resume(self):
        if self.paused:
            self.start = ttime.perf_counter()
            self.stop = self.start
            self.paused = False
