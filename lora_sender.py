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
        if response:
            print("Response:", response.decode('utf-8', 'ignore'))

def initialize_lora():
    send_command("AT")
    send_command("AT+ADDRESS=1")
    send_command("AT+NETWORKID=5")
    send_command("AT+BAND=915000000")

def send_message():
    message = "Hello Receiver"
    command = f"AT+SEND=2,{len(message)},{message}"
    send_command(command)

initialize_lora()
while True:
    send_message()
    utime.sleep(5)
