import machine
from machine import I2C, Pin
#Registers_Address
ADDRESS_WRITE = 0X34
ADDRESS_READ = 0X35
CONFIGURATION_REGISTER = 0x01
EVENT_COUNTER_REG = 0x03
KEY_EVENT_REG = 0x04
KP_MATRIX_REG1 = 0x1d
KP_MATRIX_REG2 = 0x1e
KP_MATRIX_REG3 = 0x1f


class TCA8418:
    num_to_key={2:1, 3:2, 4:3, 1:'A', 12:4, 13:5, 14:6, 11:'B', 22:7, 23:8, 24:9, 21:'C', 32:'*', 33:0, 34:'#', 31:'D'}
    key_to_num={'1':2, '2':3, '3':4, 'A':1, '4':12, '5':13, '6':14, 'B':11, '7':22, '8':23, '9':24, 'C':21, '*':32, '0':33, '#':34, 'D':31}
    
    def __init__(self):
        self.mI2c = I2C(scl=Pin(21), sda=Pin(22), freq=100000)
        self.WriteReg(CONFIGURATION_REGISTER, 0x91)  #configuring the confiure register
        self.WriteReg(KP_MATRIX_REG1, 0x0f)  #Setting the R0,R1,R2,R3 in keypad scan mode
        self.WriteReg(KP_MATRIX_REG2, 0x0f)  #Setting the C0,C1,C2,C3 in keypad scan mode
        self.WriteReg(KP_MATRIX_REG3, 0x00)
            
    def WriteReg(self,reg,data):      #Function to write values to the register
        buf=bytearray(2)
        buf[0] = reg
        buf[1] = data
        try:
            cnt = self.mI2c.writeto(ADDRESS_WRITE, buf, True)
            return cnt
        except Exception:
            return 0
            
    def ReadReg(self,reg):            #Function to read values from the register
        buf = bytearray(1)
        buf[0] = reg
        #buf[1] = ADDRESS_READ
        try:
            self.mI2c.writeto(ADDRESS_WRITE, buf, False)
            data = self.mI2c.readfrom(ADDRESS_WRITE, 1, True)
            return data
        except Exception:
            return 0
            
    def input_keypad(self):             #Function to scan the register
       
        try:
            key_cntr = self.ReadReg(EVENT_COUNTER_REG)   #Checking the Event count registers for key ever count
            key = int(key_cntr[0])
            key_counter = key & 0x0f
            
            if (key_counter != 0):
                key_values1 = self.ReadReg(KEY_EVENT_REG)         #Reading the Key event register to get the key values
                key_values = self.ReadReg(KEY_EVENT_REG)           #Reading twice the Key event registers for key press and release
                key_value = int(key_values[0]) & (0x7f)    #Getting the key values that stored from bit6 to bit0(KEA6-KAE0) in the key event register
                key_pressed = self.num_to_key[key_value]  
                return key_pressed 
        except KeyboardInterrupt:
            pass

            

            