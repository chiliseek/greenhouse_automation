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
        self.datafile = 'dht22_data.json'
        self.sensor = Adafruit_DHT.DHT22
        self.pin = 14
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        self.temp_min = ''
        self.temp_max = ''
        self.humi_min = ''
        self.humi_max = ''

    def refresh(self):
        """Refresh the sensor data"""
        print("Refreshing DHT22 data...")
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)

    def get_temp(self):
        """return formatted temperature"""
        self.temperature = format(self.temperature, '.1f')
        return self.temperature

    def get_humi(self):
        """return formatted humidity"""
        self.humidity = format(self.humidity, '.1f')
        return self.humidity

    def save_data(self):
        """saves all data to a json file"""
        data = [
            self.temperature,  # 0 - Index
            self.humidity,     # 1
            self.temp_min,     # 2
            self.temp_max,     # 3
            self.humi_min,     # 4
            self.humi_max,     # 5
        ]
        with open(self.datafile, 'w') as file_object:
            json.dump(data, file_object)
        print("Saving data...")

    def load_data(self):
        """if there is data, load it"""
        try:
            with open(self.datafile) as file_object:
                data = json.load(file_object)
        except FileNotFoundError:
            self.save_data()
            print("There is no old data. Creating a new datafile...")

        else:
            data[0] = self.temperature
            data[1] = self.humidity
            data[2] = self.temp_min
            data[3] = self.temp_max
            data[4] = self.humi_min
            data[5] = self.humi_max


print("Testing DHT22... Initializing DHT22 Class")
dht22 = DHT22()
temp = dht22.get_temp()
humi = dht22.get_humi()
print("Temperature: " + str(temp) + " °C\nHumidity: " + str(humi) + " %")
dht22.save_data()





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
