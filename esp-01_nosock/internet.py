import network
import time

from data_parser import parser

parser = parser()

def wlan_activate():
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)       # activate the interface
    wlan_data = parser.get_connected_ssid_data()
    print(wlan_data, wlan.config('essid'))
    wlan.disconnect()
    time.sleep(1)
    if not wlan.isconnected() or wlan.config('essid') != wlan_data[0]:
        print('connecting to network...')
        wlan.connect(wlan_data[0], wlan_data[1])
        attempts = 0
        while not wlan.isconnected():
            if attempts >= 300:
                return 
            else:
                print('connecting...')
                attempts+= 1
                time.sleep(1)

    # wlan_data = wlan.ifconfig()
    # sub_addr = wlan_data[0].split('.')[-2]
    # wlan.ifconfig(('192.168.{}.55'.format(sub_addr), wlan_data[1], wlan_data[2], wlan_data[3]))
    
    # wlan.disconnect()
    # time.sleep_ms(500)

    # wlan.connect(data.get_connected_ssid_data()[0], data.get_connected_ssid_data()[1])
    # while not wlan.isconnected():
    #     print('second connecting...')
    #     time.sleep(1)
    
    return wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses

def point_activate():
    wlan_data = parser.get_created_ssid_data()
    ap = network.WLAN(network.AP_IF) # create access-point interface
    ap.active(True)         # activate the interface
    ap.config(essid=wlan_data[0], password=wlan_data[1]) # set the ESSID of the access point

def point_deactivate():
    ap = network.WLAN(network.AP_IF) # create access-point interface
    ap.active(False)         # deactivate the interface