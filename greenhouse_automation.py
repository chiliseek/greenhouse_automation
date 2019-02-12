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
        self.temp_min = format(self.temperature, '.1f')
        self.temp_max = format(self.temperature, '.1f')
        self.humi_min = format(self.humidity, '.1f')
        self.humi_max = format(self.humidity, '.1f')

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
            print("Loading data...")
            data[0] = self.temperature
            data[1] = self.humidity
            if data[2] < self.temp_min:  # checking if max/min value are correct
                print("New minimal temperature: " + str(data[2]) + " °C")
                data[2] = self.temp_min
            if data[3] > self.temp_max:
                print("New maximal temperature: " + str(data[3]) + " °C")
                data[3] = self.temp_max
            if data[4] < self.humi_min:
                print("New minimal humidity: " + str(data[4]) + " %")
                data[4] = self.humi_min
            if data[5] > self.humi_max:
                print("New maximal humidity: " + str(data[5]) + " %")
                data[5] = self.humi_max

    def set_minmax(self):
        """determine min and max temp/humi values"""
        if float(self.temperature) > float(self.temp_max):  # Set max temperature
            print("New maximal temperature: " + str(self.get_temp()) + " °C")
            self.temp_max = float(self.humidity)
        else:
            print(self.temperature, ">", self.temp_max)
        if float(self.temperature) < float(self.temp_min):  # Set min temperature
            print("New minimal temperature: " + str(self.get_temp()) + " °C")
            self.temp_min = float(self.temperature)

        if float(self.humidity) > float(self.humi_max):  # Set max humidity
            print("New maximal humidity: " + str(self.get_temp()) + " %")
            self.humi_max = float(self.humidity)
        if float(self.humidity) < float(self.humi_min):  # Set min humidity
            print("New minimal humidity: " + str(self.get_temp()) + " %")
            self.humi_min = float(self.humidity)


print("Testing DHT22... Initializing DHT22 Class")
dht22 = DHT22()
temp = dht22.get_temp()
humi = dht22.get_humi()
print("Temperature: " + str(temp) + " °C\nHumidity: " + str(humi) + " %")
dht22.load_data()
sleep(2)
dht22.set_minmax()


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
