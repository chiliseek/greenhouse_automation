#!/usr/bin/python3
# Greenhouse automation with python.
from time import sleep
from termcolor import colored
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
        """Print temperature, humidity and min max values"""
        print("\nTemperature: " + str(self.temperature) + " °C\t" + colored(self.temp_min, 'cyan') + " / " +
              colored(self.temp_max, 'red') + " °C")
        print("Humidity:    " + str(self.humidity) + "  %\t" + colored(self.humi_min, 'cyan') + " / " +
              colored(self.humi_max, 'red') + "  %\n")

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
        print("Saving data ...")

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
                print("Setting minimal temperature (" + colored(data[2], 'cyan') + " °C) from datafile.")
                self.temp_min = data[2]
            if data[3] > self.temp_max:
                print("Setting maximal temperature (" + colored(data[3], 'red') + " °C) from datafile.")
                self.temp_max = data[3]
            if data[4] < self.humi_min:
                print("Setting minimal humidity    (" + colored(data[4], 'cyan') + "  %) from datafile.")
                self.humi_min = data[4]
            if data[5] > self.humi_max:
                print("Setting maximal humidity    (" + colored(data[5], 'red') + "  %) from datafile.")
                self.humi_max = data[5]

    def set_minmax(self):
        """determine min and max temp/humi values"""
        if self.temperature > self.temp_max:  # Set max temperature
            print(colored('  +++', 'yellow') + " New maximal temperature: " + colored(self.temperature, 'red') + " °C")
            self.temp_max = self.temperature
        if self.temperature < self.temp_min:  # Set min temperature
            print(colored('  +++', 'yellow') + " New minimal temperature: " + colored(self.temperature, 'cyan') + " °C")
            self.temp_min = self.temperature

        if self.humidity > self.humi_max:  # Set max humidity
            print(colored('  +++', 'yellow') + " New maximal humidity:    " + colored(self.humidity, 'red') + "  %")
            self.humi_max = self.humidity
        if self.humidity < self.humi_min:  # Set min humidity
            print(colored('  +++', 'yellow') + " New minimal humidity:    " + colored(self.humidity, 'cyan') + "  %")
            self.humi_min = self.humidity


class Relay(DHT22):
    """Manage 4 channel relay board"""

    def __init__(self):
        """Initialize the relay board and its channels"""
        super().__init__()
        GPIO.setmode(GPIO.BCM)  # Setting GPIO mode
        GPIO.setwarnings(False)  # disable warnings
        self.channel = {
            '1': 23,
            '2': 18,
            '3': 24,
            '4': 25,
        }
        for chan, pin_nr in self.channel.items():
            GPIO.setup(pin_nr, GPIO.OUT)

    def switch_status(self, status, chan):
        """Turn relay on"""
        if chan == 1:
            if status == 1:
                GPIO.output(self.channel[str(chan)], GPIO.LOW)
                print("Relay channel " + str(chan) + " activated.")
            elif status == 0:
                GPIO.output(self.channel[str(chan)], GPIO.HIGH)
                print("Relay channel " + str(chan) + " deactivated.")
        if chan == 2:
            if status == 1:
                GPIO.output(self.channel[str(chan)], GPIO.LOW)
                print("Relay channel " + str(chan) + " activated.")
            elif status == 0:
                GPIO.output(self.channel[str(chan)], GPIO.HIGH)
                print("Relay channel " + str(chan) + " deactivated.")
        if chan == 3:
            if status == 1:
                GPIO.output(self.channel[str(chan)], GPIO.LOW)
                print("Relay channel " + str(chan) + " activated.")
            elif status == 0:
                GPIO.output(self.channel[str(chan)], GPIO.HIGH)
                print("Relay channel " + str(chan) + " deactivated.")
        if chan == 4:
            if status == 1:
                GPIO.output(self.channel[str(chan)], GPIO.LOW)
                print("Relay channel " + str(chan) + " activated.")
            elif status == 0:
                GPIO.output(self.channel[str(chan)], GPIO.HIGH)
                print("Relay channel " + str(chan) + " deactivated.")

    def knight_rider(self, times='0'):
        """Test mode: switch all relays on and off in knight rider style"""
        counter = int(times)
        while counter < 1:  # Relay Knight Rider
            for chan in range(1, 5):
                self.switch_status(1, chan)
                sleep(0.1)
                self.switch_status(0, chan)
            for chan in reversed(range(1, 5)):
                self.switch_status(1, chan)
                sleep(0.1)
                self.switch_status(0, chan)
            counter += 1


print("Initializing DHT22 Class...")
dht22 = DHT22()
dht22.print_data()
dht22.load_data()

print("\nInitializing Relay...")
relay = Relay()
relay.knight_rider()  # Testing relay Knight Rider style

print("\nWaiting 2 seconds, refreshing sensor data and setting min/max values...")
sleep(2)
while True:
    print("\n")
    dht22.refresh()
    dht22.set_minmax()
    dht22.save_data()
    print("\n. . . Next measurement in 10 seconds . . .")
    sleep(10)
