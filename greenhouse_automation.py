#!/usr/bin/python3
#  Greenhouse automation with python.
from time import sleep
import RPi.GPIO as GPIO
import Adafruit_DHT

print("Testing DHT22...")
sensor = Adafruit_DHT.DHT22
pin = 14
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
print(humidity, temperature)


print("\nTesting Relay...")
GPIO.setmode(GPIO.BCM)  # Setting GPIO mode

pinliste = [
    23,  # Channel 1
    18,  # Channel 2
    24,  # Channel 3
    25,  # Channel 4
]

print("Initializing relay board...")
for pin in pinliste:
    GPIO.setup(pin, GPIO.OUT)

print("Starting Knight Rider in a second...")

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
class DHT22():
    
    
    def __init__(self):
"""
