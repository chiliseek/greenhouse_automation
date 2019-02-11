#!/usr/bin/python3
#  Greenhouse automation with python.
from time import sleep
import RPi.GPIO as GPIO
import Adafruit_DHT

print("Testing DHT22")
sensor = Adafruit_DHT.DHT22
pin = 14
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
print(humidity, temperature)


"""
class DHT22():
    
    
    def __init__(self):
"""
