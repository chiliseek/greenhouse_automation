#!/usr/bin/python3
# Greenhouse automation with python.
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
        self.temperature = float(format(self.temperature, '.1f'))
        self.humidity = float(format(self.humidity, '.1f'))
        self.temp_min = float(format(self.temperature, '.1f'))
        self.temp_max = float(format(self.temperature, '.1f'))
        self.humi_min = float(format(self.humidity, '.1f'))
        self.humi_max = float(format(self.humidity, '.1f'))

    def print_data(self):
        """Print temperature and humidity. later maybe min max values too"""
        print("\nTemperature: " + str(self.temperature) + " °C\nHumidity: " + str(self.humidity) + " %\n")

    def refresh(self):
        """Refresh the sensor data and print"""
        print("Refreshing DHT22 data...")
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        self.temperature = float(format(self.temperature, '.1f'))
        self.humidity = float(format(self.humidity, '.1f'))
        self.print_data()

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
                print("Setting minimal temperature (" + str(data[2]) + " °C) from datafile.")
                self.temp_min = data[2]
            if data[3] > self.temp_max:
                print("Setting maximal temperature (" + str(data[3]) + " °C) from datafile.")
                self.temp_max = data[3]
            if data[4] < self.humi_min:
                print("Setting minimal humidity (" + str(data[4]) + " %) from datafile.")
                self.humi_min = data[4]
            if data[5] > self.humi_max:
                print("Setting maximal humidity (" + str(data[5]) + " %) from datafile.")
                self.humi_max = data[5]

    def set_minmax(self):
        """determine min and max temp/humi values"""
        if self.temperature > self.temp_max:  # Set max temperature
            print("New maximal temperature: " + str(self.temperature) + " °C")
            self.temp_max = self.temperature
        if self.temperature < self.temp_min:  # Set min temperature
            print("New minimal temperature: " + str(self.temperature) + " °C")
            self.temp_min = self.temperature

        if self.humidity > self.humi_max:  # Set max humidity
            print("New maximal humidity: " + str(self.humidity) + " %")
            self.humi_max = self.humidity
        if self.humidity < self.humi_min:  # Set min humidity
            print("New minimal humidity: " + str(self.humidity) + " %")
            self.humi_min = self.humidity


class Relay():
    """Manage 4 channel relay board"""

    def __init__(self):
        """Initialize the relay board and its channels"""
        GPIO.setmode(GPIO.BCM)  # Setting GPIO mode
        GPIO.setwarnings(False)  # disable warnings
        self.channel = {
            '1': 23,
            '2': 18,
            '3': 24,
            '4': 25,
        }
        print("Initializing relay board...")
        for chan, pin_nr in self.channel.items():
            GPIO.setup(pin_nr, GPIO.OUT)

    def switch_status(self, status, chan):
        """Turn relay on"""
        while True:
            if chan == 1:
                if status == 1:
                    GPIO.output(self.channel[str(chan)], GPIO.LOW)
                    print("Relay channel " + str(chan) + " activated.")
                    break
                elif status == 0:
                    GPIO.output(self.channel[str(chan)], GPIO.HIGH)
                    print("Relay channel " + str(chan) + " deactivated.")
                    break
            if chan == 2:
                if status == 1:
                    GPIO.output(self.channel[str(chan)], GPIO.LOW)
                    print("Relay channel " + str(chan) + " activated.")
                    break
                elif status == 0:
                    GPIO.output(self.channel[str(chan)], GPIO.HIGH)
                    print("Relay channel " + str(chan) + " deactivated.")
                    break
            if chan == 3:
                if status == 1:
                    GPIO.output(self.channel[str(chan)], GPIO.LOW)
                    print("Relay channel " + str(chan) + " activated.")
                    break
                elif status == 0:
                    GPIO.output(self.channel[str(chan)], GPIO.HIGH)
                    print("Relay channel " + str(chan) + " deactivated.")
                    break
            if chan == 4:
                if status == 1:
                    GPIO.output(self.channel[str(chan)], GPIO.LOW)
                    print("Relay channel " + str(chan) + " activated.")
                    break
                elif status == 0:
                    GPIO.output(self.channel[str(chan)], GPIO.HIGH)
                    print("Relay channel " + str(chan) + " deactivated.")
                    break


print("Testing DHT22... Initializing DHT22 Class")
dht22 = DHT22()
dht22.print_data()
dht22.load_data()
print("\nWaiting 2 seconds, refreshing sensor data and setting min/max values...")
sleep(2)
dht22.refresh()
dht22.set_minmax()
dht22.save_data()

print("\nTesting Relay...")
relay = Relay()
relay.switch_status(1, 2)
sleep(1)
relay.switch_status(0, 2)

"""
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
"""