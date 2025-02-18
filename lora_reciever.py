import machine
import utime

uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))

def send_command(command):
    if isinstance(command, str):
        command = command.encode('ascii')
    uart.write(command + b"\r\n")
    utime.sleep(0.5)
    while uart.any():
        response = uart.read()
        print("Response:", response.decode('utf-8', 'ignore'))

def initialize_lora():
    send_command("AT")
    send_command("AT+ADDRESS=2")
    send_command("AT+NETWORKID=5")
    send_command("AT+BAND=915000000")

def listen_for_messages():
    buffer = b""
    while True:
        if uart.any():
            data = uart.read()
            buffer += data
            if b"\r\n" in buffer:
                lines = buffer.split(b"\r\n")
                buffer = lines.pop()
                for line in lines:
                    line_str = line.decode('utf-8', 'ignore').strip()
                    if line_str.startswith("+RCV="):
                        parts = line_str.split(",")
                        address = parts[0].split('=')[1]
                        message = parts[2]
                        print(f"Received message from address {address}: {message}")

initialize_lora()
listen_for_messages()

        
