import network
import time
router = [("ssid", "password"), ("rraaghul", "password"), ("user4", "password")]

class Wifi:
        def __init__(self):
            self.wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True)
          
        def ConnectionStatus(self):
            data = self.wlan.isconnected()
            if data:
               print('WiFi is connected')
            else:
                print('WiFi is not connected!!')
        
        def wificonnection(self,ssid, password):
            data = self.wlan.connect(ssid, password)
            return data
        
        def wifiScan(self):
            data = self.wlan.scan()
            return data
        
        def wifiDisconnect(self):
            data = self.wlan.disconnect()
            return data
        
        def wifiInfo(self):
            data = self.wlan.ifconfig()
            return data
          
        def wifiAutoconnect(self):
            
            data = self.wlan.isconnected()
            if data:
               print('WiFi is connected')
            else:
              print('Wifi is not connected') 
              for i in router:
                 self.wlan.connect(*i)
                 time.sleep(3)
              if data:
                 print('WiFi is connected')
                 
                
        



