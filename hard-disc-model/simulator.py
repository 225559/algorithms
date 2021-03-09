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
from event import Event

class Simulator:
    def __init__(self, particles):
        self.event_queue = []
        self.particles = particles
        self.time = 0

        for particle in self.particles:
            self.predict(particle)

    def predict(self, i):
        if i is None:
            return
        for j in self.particles:
            if i == j:
                continue
            heapq.heappush(self.event_queue, Event(self.time + i.next_collision(j), i, j))
        heapq.heappush(self.event_queue, Event(self.time + i.next_collision_hwall(), i, None))
        heapq.heappush(self.event_queue, Event(self.time + i.next_collision_vwall(), None, i))

    def next_event(self):        
        event = heapq.heappop(self.event_queue)
        
        while event and event.invalid():
            event = heapq.heappop(self.event_queue)

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