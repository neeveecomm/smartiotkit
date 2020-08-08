import machine
import time


class UserLED:
    
    def __init__(self):
        self.pin2 = machine.Pin(2, machine.Pin.OUT)
        self.pin32 = machine.Pin(32, machine.Pin.OUT)
                     
    def ledon(self, p):
        
     if (p == 2):    
        self.pin2.value(0)
        self.pin32.value(1)
        
     if (p == 32):
        self.pin2.value(1)
        self.pin32.value(0)
        
    def ledoff(self, p):
        
     if (p == 2):
        self.pin2.value(1)
        self.pin32.value(1)
  
     if (p == 32):   
        self.pin2.value(1)
        self.pin32.value(1)