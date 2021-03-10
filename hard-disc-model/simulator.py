# MIT License
# -----------

# Copyright (c) 2021 Sorn Zupanic Maksumic (https://www.usn.no)
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
import heapq
import time
from event import Event
from window import Window

class Simulator:

    def __init__(self, particles):
        self.event_queue = []
        self.particles = particles
        self.limit = 10000
        self.time = 0
        self.window = Window(500, particles)

    def redraw(self):
        self.window.redraw()
        time.sleep(0.02)
        if (self.time < self.limit):
            heapq.heappush(self.event_queue, Event(self.time + 1 / 0.5, None, None))

    def predict(self, i):
        if i is None:
            return
        for j in self.particles:
            dt = i.next_collision(j)
            if self.time + dt <= self.limit:
                heapq.heappush(self.event_queue, Event(self.time + dt, i, j))

        dt = i.next_collision_vwall()
        if self.time + dt <= self.limit:
            heapq.heappush(self.event_queue, Event(self.time + dt, i, None))
            
        dt = i.next_collision_hwall()
        if self.time + dt <= self.limit:
            heapq.heappush(self.event_queue, Event(self.time + dt, None, i))

    def simulate(self):
        for particle in self.particles:
            self.predict(particle)
        
        heapq.heappush(self.event_queue, Event(0, None, None))

        while True:
            event = heapq.heappop(self.event_queue)
            
            if event.invalid():
                continue

            for particle in self.particles:
                particle.move(event.time - self.time)
            
            self.time = event.time

            if (event.i is not None) and (event.j is not None):
                event.i.collide(event.j)
                self.predict(event.i)
                self.predict(event.j)
            elif event.i is not None:
                event.i.collide_vwall()
                self.predict(event.i)
            elif event.j is not None:
                event.j.collide_hwall()
                self.predict(event.j)
            else:
                self.redraw()