from machine import Pin, I2C
import network
import urequests
import time
from time import sleep
import bme280
import constants

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000) 

ssid = constants.INTERNET_NAME
password = constants.INTERNET_PASSWORD
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while not wlan.isconnected():
    pass

api_key = 'your_API_KEY'
base_url = 'https://api.thingspeak.com/update'

def read_sensor():
    bme = bme280.BME280(i2c=i2c)
    temperature, pressure, humidity = [float(i) for i in bme.values]
    return temperature, pressure, humidity

# Send data to ThingSpeak
while True:
    temperature, pressure, humidity = read_sensor()
    url = f"{base_url}?api_key={api_key}&field1={temperature}&field2={pressure}&field3={humidity}"
    response = urequests.get(url)
    print(response.text)
    time.sleep(15)
