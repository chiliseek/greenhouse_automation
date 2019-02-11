#!/usr/bin/python3
#  Greenhouse automation with python.
from time import sleep
import json
import RPi.GPIO as GPIO
import Adafruit_DHT


class DHT22():
    """Initialize and access DHT22 sensor"""

    def __init__(self):
        """Initialize dht22 sensor and the GPIO pin its connected to"""
        self.sensor = Adafruit_DHT.DHT22
        self.pin = 14
        self.temperature, self.humidity = Adafruit_DHT.read_retry(self.sensor, self.pin)

    def refresh(self):
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)

    def get_temp(self):
        """return temperature"""
        self.refresh()
        self.temperature = format(self.temperature, '.2f')
        return self.temperature

    def get_humi(self):
        """return humidity"""
        self.refresh()
        return self.humidity


print("Testing DHT22... Initializing DHT22 Class")
dht22 = DHT22()
sleep(2)
temp = dht22.get_temp()
humi = dht22.get_humi()
print("Temperature: " + str(temp) + " °C\nHumidity: " + str(humi) + " %")






print("\nTesting Relay...")
GPIO.setmode(GPIO.BCM)  # Setting GPIO mode
GPIO.setwarnings(False)  # disable warnings

pinliste = [
    23,  # Channel 1
    18,  # Channel 2
    24,  # Channel 3
    25,  # Channel 4
]

print("Initializing relay board...")
for pin in pinliste:
    GPIO.setup(pin, GPIO.OUT)

print("Starting Knight Rider...")

counter = 0
while counter < 1:  # Relay Knight Rider
    for pin in pinliste:
        GPIO.output(pin, GPIO.LOW)
        sleep(0.05)
        GPIO.output(pin, GPIO.HIGH)

    for pin in reversed(pinliste):
        GPIO.output(pin, GPIO.LOW)
        sleep(0.05)
        GPIO.output(pin, GPIO.HIGH)

    counter +=1

print("Stopped Knight Rider...")
