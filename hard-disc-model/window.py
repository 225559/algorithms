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
import tkinter as tk

class Window:
    def __init__(self, unit_box_size, particles):
        self.unit_box_size = unit_box_size
        self.particles = particles
        self.window = tk.Tk()
        self.window.title("Hard Disc Model - Particle Simulation")
        self.canvas = tk.Canvas(self.window, width=unit_box_size, height=unit_box_size, bg='#fcfcfc')
        self.canvas.pack()
    
    def create_circle(self, x, y, r, color):
        x0 = x - r
        x1 = x + r
        y0 = y - r
        y1 = y + r
        return self.canvas.create_oval(x0, y0, x1, y1, fill=color)

    def redraw(self):
        self.canvas.update()
        self.canvas.update_idletasks()
        self.canvas.delete("all") # clear
        for particle in self.particles:
            x = particle.position.x * self.unit_box_size
            y = particle.position.y * self.unit_box_size
            r = particle.radius * self.unit_box_size
            self.create_circle(x, y, r, particle.color)