import serial
import time

# Configure the serial connection
port = "/dev/cu.usbmodem11201"
baudrate = 115200
serial_connection = serial.Serial(port, baudrate)

# Read and write data until the transfer is complete
for i in range(1, 1001):
    print(i)
    serial_connection.write((str(i) + ',').encode())
    time.sleep(0.01)

time.sleep(10)

serial_connection.close()
