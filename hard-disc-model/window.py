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
        self.avg_ink_distance_from_center = tk.Text(self.window, height=1)
        self.avg_ink_distance_from_center.pack()
        self.canvas = tk.Canvas(self.window, width=unit_box_size, height=unit_box_size, bg='#060606')
        self.canvas.pack()
        self.grid_lines = 5

    def create_circle(self, x, y, r, color):
        x0 = x - r
        x1 = x + r
        y0 = y - r
        y1 = y + r
        return self.canvas.create_oval(x0, y0, x1, y1, fill=color, outline=color)

    def draw_grid(self):
        size = int(self.unit_box_size)
        for i in range(0, size, int(size/self.grid_lines)):
            self.canvas.create_line(i, 0, i, size, width=1, fill='#363636')
            self.canvas.create_line(0, i, size, i, width=1, fill='#363636')

    def redraw(self):
        self.canvas.update()
        self.canvas.update_idletasks()
        self.canvas.delete("all") # clear
        avg = 0
        N = len(self.particles)
        ink_counter = [[0 for x in range(self.grid_lines)] for x in range(self.grid_lines)]
        water_counter = [[0 for x in range(self.grid_lines)] for x in range(self.grid_lines)]
        for particle in self.particles:
            x = particle.position.x * self.unit_box_size
            y = particle.position.y * self.unit_box_size
            r = particle.radius * self.unit_box_size
            self.create_circle(x, y, r, particle.color)
            
            if particle.kind == "ink":
                avg += particle.distance_from_center()

            for i in range(1, self.grid_lines + 1):
                if particle.position.x >= (i - 1) / self.grid_lines and particle.position.x < i / self.grid_lines:
                    for j in range(1, self.grid_lines + 1):
                        if particle.position.y >= (j - 1) / self.grid_lines and particle.position.y < j / self.grid_lines:
                            if particle.kind == "ink":
                                ink_counter[i-1][j-1] += 1
                            if particle.kind == "water":
                                water_counter[i-1][j-1] += 1
                            break
                    break
        
        mult = self.unit_box_size / self.grid_lines
        for i in range(0, self.grid_lines):
            for j in range(0, self.grid_lines):
                self.canvas.create_text((i * mult) + 10, (j * mult) + 10, fill="#FF1515", font="Times 8", text=str(ink_counter[i][j]))
                self.canvas.create_text((i * mult) + 18, (j * mult) + 10, fill="#636363", font="Times 8", text=":")
                self.canvas.create_text((i * mult) + 25, (j * mult) + 10, fill="#1515FF", font="Times 8", text=str(water_counter[i][j]))

        s = 'Avg. ink particle distance from center: {:f}'.format(avg/N)
        self.avg_ink_distance_from_center.delete("1.0", "end")
        self.avg_ink_distance_from_center.insert(tk.END, s)
        self.draw_grid()