import machine
import dht
import time

dht_pin = machine.Pin(2)

dht_sensor = dht.DHT22(dht_pin)

while True:
    try:
        dht_sensor.measure()

        temperature_celsius = dht_sensor.temperature()
        humidity_percent = dht_sensor.humidity()

        print("Temperature: {:.2f} °C".format(temperature_celsius))
        print("Humidity: {:.2f} %".format(humidity_percent))

    except Exception as e:
        print("Error reading DHT22:", str(e))

    time.sleep(0.1)
