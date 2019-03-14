# WIP: Greenhouse automation with the RPi and python
## : The following text is still riddled with spelling errors. I'm writing this on mobile in my work breaks so there will be a lot of mistakes until I have the time to revisit and proof read properly.
### Introduction
This is my first python project. Its an attempt to automate a greenhouse with python. Starting small, I'll automate a seedling heat mat and I'm going to expand the scope of the project as I'll progress. At the moment the script is running on a RPi Zero which it total overkill. The plan is to port the script to MicroPython and run it on an ESP8266/ESP32.

For now the script is measuring temperature and humidity every 30 seconds. It will then determine min and max values and saves it with the actual temperature and humidity in a json file. When the script is loaded it will check for the json file and load its values, if the actual values are not "greater". Depending on the temperature the script will en- disable the relay board to switch the heat mat on or off. Additionally I've added a status LED to indicate the temperature state.

### Components (+Versuchsaufbau)
List of parts:
* Raspberry Pi Zero (including the components to run it)
* 4 channel relay baord
* DHT22 sensor (resistor included)
* Heating mat for seedlings
* RGB LED + resistors
* Greenhouse

### Features
Implemented:
* Measuring temperature / humidity
* Determine min and max values
* Saving and loading data from json file
* Swtiching relay board status / switching heat mat on/off
* Indicate temperature state via status LED

Planned:
* Log Value + Date and Time
* OLED/e-ink display support
* Data visualization (matplotlib)
* Create "port" to MicroPython for ESP8266/ESP32
* Websocket LIVE graph server?
* MQTT support
