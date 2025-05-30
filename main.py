import time
import machine
from config import Config
from wifi_manager import WiFiManager
from led_controller import LEDController
from lidar_controller import LidarController

class ParkingPixels:
    def __init__(self):
        self.config = Config()
        self.wifi = WiFiManager()
        self.led = LEDController()
        self.lidar = LidarController()
        self.last_vehicle_detected = False
        self.last_vehicle_time = 0

    def setup(self):
        print("Starting ParkingPixels...")
        self.wifi.connect()
        self.led.clear()

    def run(self):
        while True:
            try:
                # Check for vehicle detection
                detection_distance = self.config.get('parking', 'detection_distance')
                vehicle_detected = self.lidar.is_vehicle_detected(detection_distance)
                
                current_time = time.time()
                
                # Handle vehicle detection state changes
                if vehicle_detected and not self.last_vehicle_detected:
                    print("Vehicle detected")
                    self.led.activate()
                    self.last_vehicle_time = current_time
                elif not vehicle_detected and self.last_vehicle_detected:
                    print("Vehicle left")
                    self.led.clear()
                
                self.last_vehicle_detected = vehicle_detected
                
                # Update LED guide if active
                if self.led.is_active:
                    distance = self.lidar.get_distance()
                    if distance is not None:
                        self.led.update_guide(distance)
                
                # Small delay to prevent CPU overload
                time.sleep(0.01)
                
            except Exception as e:
                print("Error in main loop:", e)
                time.sleep(1)

if __name__ == "__main__":
    # Create and run the application
    app = ParkingPixels()
    app.setup()
    app.run() 