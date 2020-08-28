import machine
import time
from network import WLAN
import network
from umqtt.robust import MQTTClient

  
#  Certificates, keys and MQTT variables
HOST = "a2ov7okpcx0rg1-ats.iot.ap-south-1.amazonaws.com"
certificate_file = "/certificate.pem.crt"
private_key_file = "/private.pem.key"
ca_certs_file = "/root.pem"
#  Open and read certificates and keys
with open(private_key_file, "r") as f:
     private_key = f.read()

with open(certificate_file, "r") as f:
     certificate = f.read()
     

class mqtt:
    
    def __init__(self):              

        # Connect to MQTT broker.
        self.mqtt = MQTTClient( client_id="esp32_Upython",
                           server=HOST,
                           port = 8883,
                           keepalive = 10000,
                           ssl = True,
                           ssl_params={"cert": certificate,
                                       "key": private_key,
                                       "server_side":False }
                           )
        time.sleep(4)
        self.mqtt.connect()
        print('Connected to AWS cloud')
        
    def mqtt_publish(self, message):   

        # Publish a MQTT message.
        self.mqtt.publish( topic = 'Attendance', msg = message , qos = 0 )

