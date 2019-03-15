# WIP: Greenhouse automation with the RPi and Python 3 
## Project overview
I have chosen to automate a greenhouse as my first python project. Starting small, I'll automate a 
Seedling heat mat and I am going to expand the scope of the project, as I will progress. For now the script is 
running on a RPi Zero which is total overkill. The plan is to port the script to MicroPython and run it on an 
ESP8266/ESP32.

For now it is measuring temperature and humidity every 30 seconds. It will then determine min and max values 
and saves it with the actual temperature and humidity in a json file. When the script is loaded it will check for the 
json file and load its values, if the actual values are not "greater". Depending on the temperature the script will 
en- & disable the relay board to switch the heat mat on or off. Additionally I've added a status LED to indicate the 
temperature state.
 
### Components and experimental setup
[![alt text](https://i.imgur.com/JkfmtkO.jpg)
](https://imgur.com/a/4u1EfFY)
*Click the image to check out some more pictures...*

List of parts:
* Raspberry Pi Zero (+SD card, power supply)
* 4 channel relay board
* DHT22 sensor (resistor included)
* Seedling Heat Mat
* RGB LED, resistors + jumper cable
* Greenhouse

### Features
Implemented:
* Measuring temperature / humidity
* Determine min and max values
* Saving and loading data from json file
* Switching relay board status to turn heat mat on/off
* Indicate temperature state via status LED

Planned:
* Log Value + Date and Time
* OLED/e-ink display support
* Data visualization (matplotlib)
* Create "port" to MicroPython for ESP8266/ESP32
* Add more devices to the relay board to improve climate control
  * Ultraschallvernebler
  * Ventilation
* Websocket LIVE graph server?
* MQTT support?
