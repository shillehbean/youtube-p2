import time
import machine
from mlx90614 import MLX90614
# Initialize I2C bus
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0), freq=100000)
# Scan for I2C devices
devices = i2c.scan()
if devices:
    print("I2C devices found:", [hex(device) for device in devices])
else:
    print("No I2C devices found")
# Initialize the MLX90614 sensor
sensor = MLX90614(i2c)
while True:
    ambient_temp = sensor.ambient_temp
    object_temp = sensor.object_temp
print(f"Ambient Temperature: {ambient_temp:.2f}°C")
    print(f"Object Temperature: {object_temp:.2f}°C")
    time.sleep(1)
