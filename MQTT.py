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

# Setup WiFi connection.
wlan = network.WLAN( network.STA_IF )
wlan.active( True )
wlan.connect("SSID", "Password" )
time.sleep(3)
print('wifi Connected')
while not wlan.isconnected():
  machine.idle()

# Connect to MQTT broker.
mqtt = MQTTClient( client_id="esp32_Upython",
                   server=HOST,
                   port = 8883,
                   keepalive = 10000,
                   ssl = True,
                   ssl_params={"cert": certificate,
                               "key": private_key,
                               "server_side":False }
                   )
time.sleep(8)
mqtt.connect()

# Publish a test MQTT message.
mqtt.publish( topic = 'test', msg = 'Smart IoT', qos = 0 )


