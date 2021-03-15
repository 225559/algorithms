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
class Particle:
    def __init__(self, position, velocity, radius, mass, color):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.mass = mass
        self.color = color
        self.cc = 0 # collision counter

    def move(self, time):
        self.position.x += self.velocity.x * time
        self.position.y += self.velocity.y * time

    def _overlaps(self, j):
        """Checks if this particle overlaps with particle j.
        If they overlap return true, otherwise return false."""
        i = self
        if i == j:
            return True
        dr = j.position - i.position
        drdr = dr.dot(dr)
        sigma = i.radius + j.radius
        if drdr < sigma * sigma:
            return True
        return False
    
    def overlaps(self, particles):
        i = self
        for j in particles:
            if i._overlaps(j):
                return True
        return False

    def next_collision(self, j):
        i = self
        if i == j:
            return float('inf')
        dr = j.position - i.position
        dv = j.velocity - i.velocity
        dvdr = dv.dot(dr)
        dvdv = dv.dot(dv)
        drdr = dr.dot(dr)
        sigma = i.radius + j.radius
        d = (dvdr * dvdr) - dvdv * (drdr - (sigma * sigma))
        if dvdr > 0 or dvdv == 0 or d < 0:
            return float('inf')
        return -(dvdr + pow(d, 0.5)) / dvdv

    def next_collision_hwall(self):
        if self.velocity.y > 0:
            return (1.0 - self.position.y - self.radius) / self.velocity.y
        if self.velocity.y < 0:
            return (self.radius - self.position.y) / self.velocity.y
        return float('inf')

    def next_collision_vwall(self):
        if self.velocity.x > 0:
            return (1.0 - self.position.x - self.radius) / self.velocity.x
        if self.velocity.x < 0:
            return (self.radius - self.position.x) / self.velocity.x
        return float('inf')

    def collide(self, j):
        i = self
        if i == j:
            return
        dr = j.position - i.position
        dv = j.velocity - i.velocity
        dvdr = dv.dot(dr)
        sigma = i.radius + j.radius
        J = (2 * i.mass * j.mass * dvdr) / (sigma * (i.mass + j.mass))
        Jx = J * dr.x / sigma
        Jy = J * dr.y / sigma
        i.velocity.x += Jx / i.mass
        i.velocity.y += Jy / i.mass
        j.velocity.x -= Jx / j.mass
        j.velocity.y -= Jy / j.mass
        i.cc += 1
        j.cc += 1

    def collide_hwall(self):
        self.velocity.y = -self.velocity.y
        self.cc += 1

    def collide_vwall(self):
        self.velocity.x = -self.velocity.x
        self.cc += 1