# ParkingPixels - Smart Parking Assistant

A smart parking assistant system using ESP32, LED strip, and a TF-Luna LiDAR sensor to help drivers park their vehicles at the perfect distance from a wall.

<a href="https://www.buymeacoffee.com/that1prince" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## Features

- Real-time distance measurement using TF-Luna LiDAR sensor
- Visual feedback using LED strip
- WiFi configuration and management
- Customizable parking distances and thresholds
- Persistent configuration storage
- Web-based configuration interface

## Hardware Requirements

- ESP32 development board
- TF-Luna LiDAR sensor
- WS2812B LED strip (40-60 LEDs)
- Power supply (5V)
- Jumper wires

## Connections

### TF-Luna LiDAR
- VCC -> 5V
- GND -> GND
- TX -> GPIO16 (RX2)
- RX -> GPIO17 (TX2)

### LED Strip
- VCC -> 5V
- GND -> GND
- DIN -> GPIO5

## Initial Setup

1. Flash the ESP32 with the latest MicroPython firmware
2. Upload the project files to the ESP32
3. On first boot, the device will create an access point named "ParkingPixels_AP"
4. Connect to the access point using the default password: "parkingpixels"
5. Open a web browser and navigate to 192.168.4.1
6. Configure your WiFi settings and parking parameters
7. Save the configuration

## Configuration Parameters

- Detection Distance: Distance at which a vehicle is detected (inches)
- Start Distance: Distance at which LED guidance begins (inches)
- Perfect Parking Range: Range of distances considered perfect parking (inches)
- Too Close Distance: Distance at which vehicle is too close to wall (inches)
- LED Colors: Colors for different parking states
- LED Patterns: Lighting patterns for different states

## Future Features

- OTA updates
- Configuration import/export
- Real-time logging and monitoring
- Multiple LiDAR sensors for side detection
- Physical control buttons
- Parking event logging
- Motion notifications
- Power management

