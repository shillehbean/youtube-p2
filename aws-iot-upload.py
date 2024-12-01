import machine
import network
import ssl
import time
import ubinascii
import tls

from simple import MQTTClient
import config

SSID = config.SSID
WIFI_PASSWORD = config.WIFI_PASSWORD
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
### Replace with the names of the files from your certs and keys
MQTT_CLIENT_KEY = "46cc41c44191da56db300a8bce37e1c2ebafa2211becebde9dc6a778fd6c3829-private.pem.key"
MQTT_CLIENT_CERT = "46cc41c44191da56db300a8bce37e1c2ebafa2211becebde9dc6a778fd6c3829-certificate.pem.crt"
### You can find this URL by going into the AWS IoT Core Settings under "Endpoint"
MQTT_BROKER = config.IOT_CORE_ENDPOINT
MQTT_BROKER_CA = "AmazonRootCA1.pem"
led = machine.Pin("LED", machine.Pin.OUT)

# function that reads PEM file and return byte array of data
def read_pem(file):
    with open(file, "r") as input:
        text = input.read().strip()
        split_text = text.split("\n")
        base64_text = "".join(split_text[1:-1])
        return ubinascii.a2b_base64(base64_text)
def connect_internet():
    try:
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(SSID, WIFI_PASSWORD)
for i in range(0, 10):
            if not sta_if.isconnected():
                time.sleep(1)
        print("Connected to Wi-Fi")
    except Exception as e:
        print('There was an issue connecting to WIFI')
        print(e)
# callback function to handle received MQTT messages
def on_mqtt_msg(topic, msg):
    # convert topic and message from bytes to string
    topic_str = topic.decode()
    msg_str = msg.decode()
print(f"RX: {topic_str}\n\t{msg_str}")
# process message
    if topic_str is 'LED':
        if msg_str is "on":
            led.on()
        elif msg_str is "off":
            led.off()
        elif msg_str is "toggle":
            led.toggle()
connect_internet()
context = tls.SSLContext(tls.PROTOCOL_TLS_CLIENT)
context.load_cert_chain(read_pem(MQTT_CLIENT_CERT), read_pem(MQTT_CLIENT_KEY))
context.load_verify_locations(read_pem(MQTT_BROKER_CA))
context.verify_mode = tls.CERT_REQUIRED
# create MQTT client that use TLS/SSL for a secure connection
mqtt_client = MQTTClient(
    MQTT_CLIENT_ID,
    MQTT_BROKER,
    keepalive=60,
    ssl=context,
)
print(f"Connecting to MQTT broker")
# register callback to for MQTT messages, connect to broker and
# subscribe to LED topic
mqtt_client.set_callback(on_mqtt_msg)
mqtt_client.connect()
mqtt_client.subscribe('LED')
# main loop, continuously check for incoming MQTT messages
print("Connection established, awaiting messages")
while True:
    mqtt_client.check_msg()
