from mqtt import MQTTClient

from network import WLAN
import machine
import time

import wifi_connect

mqtt_host = "*****"
mqtt_username = '*****'
mqtt_password = '*******'

def sub_cb(topic, msg):
   print(msg)

def publish(device_id):

    adc = machine.ADC()
    apin = adc.channel(pin='P16')

    wifi_connect.connect()
    client = MQTTClient(device_id, mqtt_host,user=mqtt_username, password=mqtt_password, port=1883)

    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic="rm222qf/feeds/temp")

    while True:
        millivolts = apin.voltage()
        degC = (millivolts - 500.0)/10.0
        defF = ((degC * 9.0)/5.0) + 32.0

        print("Sending ON")
        client.publish(topic="rm222qf/feeds/temp", msg=str(degC))
        time.sleep(1)

        client.check_msg()

        time.sleep(1)

if __name__ == "__main__":
    publish('10521c65d708')
