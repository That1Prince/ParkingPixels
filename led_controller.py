from machine import Pin
import neopixel
import time
from config import Config

class LEDController:
    def __init__(self):
        self.config = Config()
        self.num_leds = self.config.get('led', 'num_leds')
        self.pin = Pin(5, Pin.OUT)
        self.np = neopixel.NeoPixel(self.pin, self.num_leds)
        self.colors = self.config.get('led', 'colors')
        self.is_active = False
        self.last_update = 0
        self.green_start_time = 0

    def clear(self):
        self.np.fill((0, 0, 0))
        self.np.write()
        self.is_active = False

    def set_all(self, color):
        self.np.fill(color)
        self.np.write()

    def set_range(self, start, end, color):
        for i in range(start, end):
            self.np[i] = color
        self.np.write()

    def update_guide(self, distance):
        if not self.is_active:
            return

        current_time = time.time()
        if current_time - self.last_update < 0.1:  # Limit update rate
            return
        self.last_update = current_time

        detection_dist = self.config.get('parking', 'detection_distance')
        start_dist = self.config.get('parking', 'start_distance')
        perfect_min = self.config.get('parking', 'perfect_parking_min')
        perfect_max = self.config.get('parking', 'perfect_parking_max')
        too_close = self.config.get('parking', 'too_close_distance')
        green_hold = self.config.get('parking', 'green_hold_time')

        # Calculate LED positions based on distance
        if distance > detection_dist:
            self.clear()
            return

        if distance < too_close:
            # Flash red when too close
            if int(current_time * 2) % 2:
                self.set_all(self.colors['too_close'])
            else:
                self.clear()
            return

        if perfect_min <= distance <= perfect_max:
            # Perfect parking position
            if not self.green_start_time:
                self.green_start_time = current_time
            elif current_time - self.green_start_time >= green_hold:
                self.clear()
                self.is_active = False
                return
            self.set_all(self.colors['perfect'])
            return

        # Calculate guide position
        if distance <= start_dist:
            progress = (start_dist - distance) / (start_dist - too_close)
            led_position = int(progress * (self.num_leds // 2))
            
            # Clear all LEDs
            self.clear()
            
            # Set guide LEDs from both sides
            self.set_range(0, led_position, self.colors['guide'])
            self.set_range(self.num_leds - led_position, self.num_leds, self.colors['guide'])

    def activate(self):
        self.is_active = True
        self.green_start_time = 0 