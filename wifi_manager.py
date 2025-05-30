import network
import time
from config import Config

class WiFiManager:
    def __init__(self):
        self.config = Config()
        self.wlan = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)
        self.wlan.active(True)
        self.ap.active(True)

    def connect(self):
        if not self.config.is_configured():
            self.start_ap()
            return False

        ssid = self.config.get('wifi', 'ssid')
        password = self.config.get('wifi', 'password')

        if not self.wlan.isconnected():
            print(f'Connecting to {ssid}...')
            self.wlan.connect(ssid, password)
            
            # Wait for connection with timeout
            max_wait = 10
            while max_wait > 0:
                if self.wlan.isconnected():
                    break
                max_wait -= 1
                print('Waiting for connection...')
                time.sleep(1)

        if self.wlan.isconnected():
            print('Connected to WiFi')
            print('Network config:', self.wlan.ifconfig())
            return True
        else:
            print('Failed to connect to WiFi')
            self.start_ap()
            return False

    def start_ap(self):
        ap_ssid = self.config.get('wifi', 'ap_ssid')
        ap_password = self.config.get('wifi', 'ap_password')
        
        self.ap.config(essid=ap_ssid, password=ap_password)
        self.ap.active(True)
        print(f'Access point started: {ap_ssid}')
        print('Network config:', self.ap.ifconfig())

    def stop_ap(self):
        self.ap.active(False)
        print('Access point stopped')

    def get_ip(self):
        if self.wlan.isconnected():
            return self.wlan.ifconfig()[0]
        return self.ap.ifconfig()[0]

    def is_connected(self):
        return self.wlan.isconnected() 