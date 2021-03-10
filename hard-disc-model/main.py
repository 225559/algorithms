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
import random
from particle import Particle
from simulator import Simulator
from vector2 import Vector2

if __name__ == '__main__':
    particles = []
    for _ in range(100):
        rx = random.random()
        ry = random.random()
        vx = random.uniform(-0.005, +0.005)
        vy = random.uniform(-0.005, +0.005)
        position = Vector2(rx, ry)
        velocity = Vector2(vx, vy)
        radius = random.uniform(0.01, 0.02)
        mass = 1
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        particles.append(Particle(position, velocity, radius, mass, color))
    
    simulator = Simulator(particles)
    simulator.simulate()