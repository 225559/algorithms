import tkinter as tk

class Window:
    def __init__(self, unit_box_size_in_pixels, cb_next_event):
        self.cb_next_event = cb_next_event
        self.main_window = tk.Tk()
        self.main_window.title("Hard Disc Model - Particle Simulation")
        self.unit_box_size_in_pixels = unit_box_size_in_pixels
        self.next_button = tk.Button(self.main_window, text="next event", command=self.next_event)
        self.next_button.pack()
        self.canvas = tk.Canvas(self.main_window, width=self.unit_box_size_in_pixels, height=self.unit_box_size_in_pixels)
        self.canvas.pack()
        self.main_window.mainloop()
    
    def next_event(self):
        self.cb_next_event()
        self.canvas.delete("all")
        self.canvas.update()
        self.canvas.update_idletasks()