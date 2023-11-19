import smbus2
import bme280
import time
import matplotlib.pyplot as plt
from datetime import datetime

# BME280 sensor address (default address)
address = 0x76

# Initialize I2C bus
bus = smbus2.SMBus(1)

# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

# Create lists to store historical sensor data
timestamps = []
temperature_celsius_values = []
humidity_values = []
pressure_values = []

# Create a variable to control the loop
running = True

# Set up the plot
plt.ion()  # Turn on interactive mode
fig, axs = plt.subplots(3, 1, sharex=True, figsize=(10, 8))
fig.suptitle('Real-time Sensor Readings')

# Labels for the subplots
axs[0].set_ylabel('Temperature (ºC)')
axs[1].set_ylabel('Humidity (%)')
axs[2].set_ylabel('Pressure (hPa)')

# Loop forever
while running:
    try:
        # Read sensor data
        print('Running')
        data = bme280.sample(bus, address, calibration_params)

        # Extract temperature, pressure, humidity, and corresponding timestamp
        temperature_celsius = data.temperature
        humidity = data.humidity
        pressure = data.pressure
        timestamp = data.timestamp

        # Append data to lists
        timestamps.append(timestamp)
        temperature_celsius_values.append(temperature_celsius)
        humidity_values.append(humidity)
        pressure_values.append(pressure)


        # Plot the data
        for i, (ax, values, label) in enumerate(zip(axs, [temperature_celsius_values, humidity_values, pressure_values], ['Temperature (ºC)', 'Humidity (%)', 'Pressure (hPa)'])):
            ax.clear()
            ax.plot(timestamps, values, label=label)
            ax.legend()
            ax.set_ylabel(label)

        axs[-1].set_xlabel('Time')

        fig.autofmt_xdate(rotation=45)
        plt.pause(1)  # Pause for 1 second to update the plot

        time.sleep(1)

    except KeyboardInterrupt:
        print('Program stopped')
        running = False
    except Exception as e:
        print('An unexpected error occurred:', str(e))
        running = False

# Close the plot at the end
plt.ioff()
plt.show()
