import json
import os

class Config:
    DEFAULT_CONFIG = {
        'wifi': {
            'ssid': '',
            'password': '',
            'ap_ssid': 'ParkingPixels_AP',
            'ap_password': 'parkingpixels'
        },
        'parking': {
            'detection_distance': 120,  # inches
            'start_distance': 96,       # inches
            'perfect_parking_min': 24,  # inches
            'perfect_parking_max': 36,  # inches
            'too_close_distance': 18,   # inches
            'green_hold_time': 5        # seconds
        },
        'led': {
            'num_leds': 50,
            'colors': {
                'guide': (255, 255, 255),  # White
                'perfect': (0, 255, 0),    # Green
                'too_close': (255, 0, 0)   # Red
            }
        }
    }

    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return self.DEFAULT_CONFIG.copy()

    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f)

    def get(self, section, key=None):
        if key is None:
            return self.config.get(section, {})
        return self.config.get(section, {}).get(key)

    def set(self, section, key, value):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.save_config()

    def reset(self):
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()

    def is_configured(self):
        return bool(self.get('wifi', 'ssid') and self.get('wifi', 'password')) 