import pycom
import urequests
import machine
import ubinascii

import wifi_connect
import ujson
import time

from mqtt import MQTTClient

pycom.heartbeat(False)

# API Information
base_url = 'https://iot.ebrinktech.com/'

# Register device with API
unique_id = machine.unique_id()
device_name = ubinascii.hexlify(unique_id).decode()

mqtt_host = "*****"
mqtt_username = '*****'
mqtt_password = '*******'


def sub_cb(topic, msg):
    print(msg)


def registerReading():
    print('about to register')
    wifi_connect.connect()
#MQTT
    client = MQTTClient(device_name, mqtt_host,user=mqtt_username, password=mqtt_password, port=1883)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic="topic/name")

# HTTP
    url = base_url+'v1/device/register/'+device_name
    register_headers = {"Authorization": "*******", "content-type":"application/json"}
    res = urequests.request('POST',url,None, None, register_headers, None,False)
    print(res.text)
    print('\n')
    headers = {"Authorization": "*******", "accept": "*/*", "content-type":"application/json"}

    adc = machine.ADC()
    apin = adc.channel(pin='P16')

    while True:
        millivolts = apin.voltage()
        degC = (millivolts - 500.0)/10.0
        defF = ((degC * 9.0)/5.0) + 32.0

        reading_endpoint = base_url + 'v1/reading/register/'+device_name
        data = '{"value":"' + str(degC) + '","typeOfReading":"Temperature","metric":"Celcius"}'
        reading_res = urequests.request('PUT',reading_endpoint,data, None, headers,None, False)
        print(reading_res.content)

        time.sleep(1)
        print("Sending ON")
        client.publish(topic="topic/name", msg=str(degC))

        time.sleep(1)

        client.check_msg()

        time.sleep(1)

if __name__ == "__main__":
    registerReading()
