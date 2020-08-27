from fingerprint import fingerprint
from MQTT import mqtt
from WiFi import WAVWireless
import machine
import time

#connecting to WiFi
w = WAVWireless()
w.scanAndConnect()

#enabling the Interrupt pin for Biometric module
p25 = machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_UP)
#connecting to AWS cloud through MQTT
m = mqtt()
#connecting to the fingerprint module
f = fingerprint()

interruptCounter = 0

def callback(pin):
      global interruptCounter
      interruptCounter = interruptCounter+1
      time.sleep(1)
      
      fingerid = f.search_fingerprint()

      m.mqtt_publish(message = 'ID is:{}'.format(fingerid)) #publishing the message to the AWS IoT

p25.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)
while True:
 
  if interruptCounter>0:
 
    state = machine.disable_irq()
    interruptCounter = interruptCounter-1
    machine.enable_irq(state)