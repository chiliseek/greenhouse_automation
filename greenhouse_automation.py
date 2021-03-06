#!/usr/bin/python3.7
# Greenhouse automation with python.
from time import sleep
from termcolor import colored
import json
import RPi.GPIO as GPIO
import Adafruit_DHT


class StatusLED:
    """Status LED indicating temperature changes"""

    def __init__(self):
        """Initializing status LED"""
        self.led_red = 26
        self.led_blue = 19
        self.led_green = 13
        self.pinlist = [
            self.led_red,
            self.led_blue,
            self.led_green,
        ]
        for pin in self.pinlist:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def green(self):
        """Switch LED to green"""
        for pin in self.pinlist:
            GPIO.output(pin, GPIO.LOW)
        GPIO.output(self.led_green, GPIO.HIGH)

    def red(self):
        """Switch LED to red"""
        for pin in self.pinlist:
            GPIO.output(pin, GPIO.LOW)
        GPIO.output(self.led_red, GPIO.HIGH)

    def blue(self):
        """Switch LED to blue .... TODO: add ONE proper color function"""
        for pin in self.pinlist:
            GPIO.output(pin, GPIO.LOW)
        GPIO.output(self.led_blue, GPIO.HIGH)

    def pulse(self):
        """Flash LED to indicate activity"""
        for pin in self.pinlist:
            GPIO.output(pin, GPIO.LOW)

        GPIO.output(self.led_blue, GPIO.HIGH)
        GPIO.output(self.led_red, GPIO.HIGH)
        sleep(0.2)
        GPIO.output(self.led_blue, GPIO.LOW)
        GPIO.output(self.led_red, GPIO.LOW)


class DHT22:
    """Initialize and access DHT22 sensor"""

    def __init__(self):
        """Initialize dht22 sensor: temperature, humidity & min/max values"""
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

        #self.led = StatusLED()

    def print_data(self):
        """Print temperature, humidity and min max values"""
        print(f"\nTemperature: {self.temperature} °C\t {colored(self.temp_min, 'cyan')} / "
              f"{colored(self.temp_max, 'red')}  °C")
        print(f"Humidity:    {self.humidity}  %\t {colored(self.humi_min, 'cyan')} / {colored(self.humi_max, 'red')}"
              f"   %\n")

    def refresh(self):
        """Refresh the sensor data and print"""
        print(f"Refreshing DHT22 data...")
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        self.temperature = float(format(self.temperature, '.1f'))
        self.humidity = float(format(self.humidity, '.1f'))
        self.print_data()

    def save_data(self):
        """Save all data to a json file - todo: add log functionality (log value and time to create a graph with
        matplotlib later on)"""
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
        print(f"Saving data ...\n")

    def load_data(self):
        """If there is data, load it"""
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
                print(f"Setting minimal temperature {colored(data[2], 'cyan')} °C) from datafile.")
                self.temp_min = data[2]
            if data[3] > self.temp_max:
                print(f"Setting maximal temperature {colored(data[3], 'red')} °C) from datafile.")
                self.temp_max = data[3]
            if data[4] < self.humi_min:
                print(f"Setting minimal humidity    {colored(data[4], 'cyan')}  %) from datafile.")
                self.humi_min = data[4]
            if data[5] > self.humi_max:
                print(f"Setting maximal humidity    {colored(data[5], 'red')}  %) from datafile.")
                self.humi_max = data[5]

    def set_minmax(self):
        """Determine min/max values"""
        if self.temperature > self.temp_max:  # Set max temperature
            print(f"{colored('  +++', 'yellow')} New maximal temperature: {colored(self.temperature, 'red')} °C")
            self.temp_max = self.temperature
        if self.temperature < self.temp_min:  # Set min temperature
            print(f"{colored('  +++', 'yellow')} New minimal temperature: {colored(self.temperature, 'cyan')} °C")
            self.temp_min = self.temperature

        if self.humidity > self.humi_max:  # Set max humidity
            print(f"{colored('  +++', 'yellow')} New maximal humidity:    {colored(self.humidity, 'red')}  %")
            self.humi_max = self.humidity
        if self.humidity < self.humi_min:  # Set min humidity
            print(f"{colored('  +++', 'yellow')} New minimal humidity:    {colored(self.humidity, 'cyan')}  %")
            self.humi_min = self.humidity


class Relay(DHT22):
    """Manage 4 channel relay board"""

    def __init__(self):
        """Initialize the relay board and its channels"""
        super().__init__()
        GPIO.setmode(GPIO.BCM)  # Setting GPIO mode
        GPIO.setwarnings(False)  # disable warnings
        self.led = StatusLED()
        self.channel = {
            '1': 23,
            '2': 18,
            '3': 24,
            '4': 25,
        }
        for chan, pin_nr in self.channel.items():  # Initializing relay board
            GPIO.setup(pin_nr, GPIO.OUT)

    def switch_status(self, status, chan):
        """Turn relay channels on and off"""
        if chan == 1:
            if status == 1:
                GPIO.output(self.channel[str(chan)], GPIO.LOW)
                print(f"Relay channel {chan} is {colored('activated', 'green')}.")
            elif status == 0:
                GPIO.output(self.channel[str(chan)], GPIO.HIGH)
                print(f"Relay channel {chan} is {colored('deactivated', 'magenta')}.")
        if chan == 2:
            if status == 1:
                GPIO.output(self.channel[str(chan)], GPIO.LOW)
                print(f"Relay channel {chan} is {colored('activated', 'green')}.")
            elif status == 0:
                GPIO.output(self.channel[str(chan)], GPIO.HIGH)
                print(f"Relay channel {chan} is {colored('deactivated', 'magenta')}.")
        if chan == 3:
            if status == 1:
                GPIO.output(self.channel[str(chan)], GPIO.LOW)
                print(f"Relay channel {chan} is {colored('activated', 'green')}.")
            elif status == 0:
                GPIO.output(self.channel[str(chan)], GPIO.HIGH)
                print(f"Relay channel {chan} is {colored('deactivated', 'magenta')}.")
        if chan == 4:
            if status == 1:
                GPIO.output(self.channel[str(chan)], GPIO.LOW)
                print(f"Relay channel {chan} is {colored('activated', 'green')}.")
            elif status == 0:
                GPIO.output(self.channel[str(chan)], GPIO.HIGH)
                print(f"Relay channel {chan} is {colored('deactivated', 'magenta')}.")

    def knight_rider(self, times='1'):
        """Test mode: switch all relays on and off in knight rider style"""
        counter = 0
        while counter < int(times):  # Relay Knight Rider
            for chan in range(1, 5):
                self.switch_status(1, chan)
                sleep(0.1)
                self.switch_status(0, chan)
            for chan in reversed(range(1, 5)):
                self.switch_status(1, chan)
                sleep(0.1)
                self.switch_status(0, chan)
            counter += 1

    def check_temp(self):
        """Switch relay status based on temperature/humidity changes"""
        if self.temperature >= 25:  # Switch LED Status
            self.led.green()
        elif self.temperature < 25:  # ^^
            self.led.blue()

        if 25 > self.temperature < 30:  # Seedling heat mat control
            self.switch_status(1, 1)
        if self.temperature >= 30:
            self.switch_status(0, 1)
            self.led.red()


print("\nInitializing DHT22 & Relay Class...")
sensor = Relay()
sensor.knight_rider()  # Testing relay Knight Rider style
sensor.print_data()
sensor.load_data()

print("\nWaiting 2 seconds, refreshing sensor data and setting min/max values...")
sleep(2)
while True:
    print("\n")
    sensor.refresh()
    sensor.led.pulse()
    sensor.set_minmax()
    sensor.save_data()
    sensor.check_temp()
    print("\n. . . Next measurement in 30 seconds . . .")
    sleep(30)
