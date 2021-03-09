from window import Window

class Simulator:
    def __init__(self, particles, unit_box_size_in_pixels):
        self.window = Window(unit_box_size_in_pixels, self.next_event)
    
    def next_event(self):
        print("next_event")