from machine import UART
import time

class LidarController:
    def __init__(self):
        self.uart = UART(2, baudrate=115200, tx=17, rx=16)
        self.last_distance = 0
        self.last_strength = 0
        self.last_temperature = 0
        self.last_update = 0

    def read_data(self):
        if self.uart.any():
            data = self.uart.read(9)
            if data and len(data) == 9:
                if data[0] == 0x59 and data[1] == 0x59:
                    distance = data[2] + data[3] * 256
                    strength = data[4] + data[5] * 256
                    temperature = data[6] + data[7] * 256
                    
                    # Convert to inches (TF-Luna provides distance in cm)
                    distance_inches = distance * 0.393701
                    
                    self.last_distance = distance_inches
                    self.last_strength = strength
                    self.last_temperature = temperature
                    self.last_update = time.time()
                    
                    return distance_inches, strength, temperature
        return None

    def get_distance(self):
        current_time = time.time()
        if current_time - self.last_update > 1.0:  # If no update in 1 second
            self.read_data()  # Try to read new data
        return self.last_distance

    def is_vehicle_detected(self, detection_distance):
        distance = self.get_distance()
        if distance is None:
            return False
        return distance <= detection_distance and self.last_strength > 100 