#Native libs
import network
import time
import random
import tls

#Third Party
from umqtt.robust import MQTTClient

# Internal libs
import constants


def connectMQTT():
    '''Connects to Broker'''
    context = tls.SSLContext(tls.PROTOCOL_TLS_CLIENT)
    context.verify_mode = tls.CERT_NONE
    # Client ID can be anything
    client = MQTTClient(
        client_id=b"mahmood",
        server=<your server name>,
        port=0,
        user=<your user>,
        password='12345Abc',
        keepalive=7200,
        ssl=context
    )
    client.connect()
    return client



def connect_to_internet(ssid, password):
    # Pass in string arguments for ssid and password
    
    # Just making our internet connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
      if wlan.status() < 0 or wlan.status() >= 3:
        break
      max_wait -= 1
      print('waiting for connection...')
      time.sleep(1)
    # Handle connection error
    if wlan.status() != 3:
       print(wlan.status())
       raise RuntimeError('network connection failed')
    else:
      print('connected')
      print(wlan.status())
      status = wlan.ifconfig()

def make_connections():
    # Connect to internet and set MPU to start taking readings
    connect_to_internet(constants.INTERNET_NAME, constants.INTERNET_PASSWORD)
    return connectMQTT()


def publish(topic, value, client):
    '''Sends data to the broker'''
    print(topic)
    print(value)
    client.publish(topic, value)
    print("Publish Done")

    

client = make_connections()

while True:
    publish('Topic', 'test _message', client)
    time.sleep(1)
