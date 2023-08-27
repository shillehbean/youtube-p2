from machine import Pin, I2C, RTC
import json
import urequests as requests
import network
import ntptime
import time
import utime

import bme280

import constants


i2c = I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
URL = "<url>"
API_KEY = "<api key>"

def connect_to_wifi(ssid, psk):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, psk)

    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to Connect")
        time.sleep(10)
    if not wlan.isconnected():
        raise Exception("Wifi not available")
    print("Connected to WiFi")


def findOne(filter_dictionary):
    try:
        headers = { "api-key": API_KEY }
        searchPayload = {
            "dataSource": "Cluster0",
            "database": "BME280",
            "collection": "Readings",
            "filter": filter_dictionary,
        }
        response = requests.post(URL + "findOne", headers=headers, json=searchPayload)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)
        
        
def find(filter_dictionary):
    try:
        headers = { "api-key": API_KEY }
        searchPayload = {
            "dataSource": "Cluster0",
            "database": "BME280",
            "collection": "Readings",
            "filter": filter_dictionary,
        }
        response = requests.post(URL + "find", headers=headers, json=searchPayload)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)
        
        
def insertOne(temp, pressure, humidity, time):
    try:
        headers = { "api-key": API_KEY }
        documentToAdd = {"Device": "BME280",
                         "Temperature (C)": temp,
                         "Pressure": pressure,
                         "Humidity": humidity,
                         "Time": time}
        insertPayload = {
            "dataSource": "Cluster0",
            "database": "BME280",
            "collection": "Readings",
            "document": documentToAdd,
        }
        response = requests.post(URL + "insertOne", headers=headers, json=insertPayload)
        print(response)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)
        
        
def insertMany(document_list):
    try:
        headers = { "api-key": API_KEY }
        insertPayload = {
            "dataSource": "Cluster0",
            "database": "BME280",
            "collection": "Readings",
            "documents": document_list,
        }
        response = requests.post(URL + "insertMany", headers=headers, json=insertPayload)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)
        
        
def updateOne(filter_dictionary, update_dict):
    try:
        headers = { "api-key": API_KEY }
        update = {"set": update_dict}
        searchPayload = {
            "dataSource": "Cluster0",
            "database": "BME280",
            "collection": "Readings",
            "filter": filter_dictionary,
            "update": update_dict,
        }
        response = requests.post(URL + "updateOne", headers=headers, json=searchPayload)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)
        
        
def deleteOne(filter_dictionary):
    try:
        headers = { "api-key": API_KEY }
        searchPayload = {
            "dataSource": "Cluster0",
            "database": "BME280",
            "collection": "Readings",
            "filter": filter_dictionary,
        }
        response = requests.post(URL + "delete", headers=headers, json=searchPayload)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)


def main():
    connect_to_wifi(constants.INTERNET_NAME, constants.INTERNET_PASSWORD)
    #document_list = []
    while True:
        bme = bme280.BME280(i2c=i2c)
        temp, pressure, humidity = bme.values
        print(temp, pressure, humidity)
        rtc_time_tuple = RTC().datetime()
        formatted_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
            rtc_time_tuple[0], rtc_time_tuple[1], rtc_time_tuple[2], 
            rtc_time_tuple[4], rtc_time_tuple[5], rtc_time_tuple[6]
        )
        print(formatted_time)
        
        #insertOne(temp, pressure, humidity, formatted_time)
        
        #document_list.append({"Device": "BME280",
            #"Temperature (C)": temp,
            #"Pressure": pressure,
            #"Humidity": humidity,
            #"Time": formatted_time}
        #)
        #if len(document_list) == 10:
           #print(json.dumps(document_list))
           #insertMany(document_list)
           #document_list = []
        #findOne({"Temperature (C)": "23.26C", "Humidity": "53.69%"})
        #find({"Temperature (C)": "24.65C"})
        #updateOne({"Temperature (C)": "23.26C"}, {"Temperature (C)": "24.26C"})
        deleteOne({"Temperature (C)": "24.26C"})

main()
