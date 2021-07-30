from network import WLAN
import machine

wlan = WLAN(mode=WLAN.STA)

def isconnected():
    return wlan.isconnected()

def connect():

    networks = wlan.scan()
    for network in networks:
        if network.ssid == 'TP-Link_1A14':
            print('my network found')
            wlan.connect(network.ssid, auth=(network.sec, '08644350'), timeout=5000)
            while not wlan.isconnected():
                machine.idle()
            print('WLAN Connection successful.!')
            break

if __name__ == "__main__":
    connect()
