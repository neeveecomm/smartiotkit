import ujson
import json
import network
from network import WLAN
import machine
import socket
import usocket as socket
import gc
gc.collect()

class NVWireless():
    def __init__(self):
        self.filename = "wifiap.json"
        self.wifiCfg = self.reload()
        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(True)
        self.wlan = WLAN(network.STA_IF)
        #self.led = machine.Pin(2, machine.Pin.OUT)
        
    def reloadCfg(self):
        self.wifiCfg = self.reload()
        
    def reload(self):
        list = []
        with open(self.filename) as fp:
            while True:
                res = []
                d = {}
                data = fp.readline()
                if data == '':
                    break
                apdata = ujson.dumps(data)
                data = data.replace("\r\n", "")
                for sub in data.split(', '):
                    if ':' in sub:
                        res = sub.split(': ', 1)
                        #print(res)
                        d[res[0]] = res[1]
                list.append(d)
            return list
        
    def scanAndConnect(self):
        self.conn = 0
        if not self.sta_if.isconnected():
            self.sta_if.active(True)
            nets = self.wlan.scan()
            for net in nets:
                #print(net)
                #print(net[0])
                for i in range(len(self.wifiCfg)):
                    ssid = net[0].decode('ASCII')
                    if ssid == self.wifiCfg[i]['wifiap']:
                        #print(ssid)
                        #print(self.wifiCfg[i]['password'])
                        password = (self.wifiCfg[i]['password'])
                        self.wlan.connect(ssid, password)
                        while not self.wlan.isconnected():
                         machine.idle()      
                        print('WLAN connection successful')
                        #print(self.wlan.ifconfig())
                        return True
            return False
