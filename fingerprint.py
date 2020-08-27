from machine import UART
import time

class fingerprint:


    def __init__(self, passwd=(0, 0, 0, 0)):

        self.uart = UART(2, 57600)
        self.uart.init(57600, bits=8, parity=None, stop=1)
        self.address = [0xFF, 0xFF, 0xFF, 0xFF]
        self.password = passwd
        self.FINGERPRINT_STARTCODE = 0xEF01
        self.FINGERPRINT_VERIFYPASSWORD = 0x13
        self.FINGERPRINT_COMMANDPACKET = 0x01
        self.FINGERPRINT_GETIMAGE = 0x01
        self.FINGERPRINT_IMAGE2TZ = 0x02
        self.FINGERPRINT_REGMODEL = 0x05
        self.FINGERPRINT_STORE = 0x06
        self.FINGERPRINT_SEARCH = 0x04
        #print('UART initialized')
        self.verify_password()
           
    def verify_password(self): #Verifying the passoword with the device password 
        
        self.send_packet([self.FINGERPRINT_VERIFYPASSWORD] + list(self.password))
        time.sleep(1)
        ret = self.uart.read()
        #print(ret)
        vpaswd = ret[9]
        if vpaswd == 0:
            print('Biometric is connected')
   
    def get_image(self): #Getting the fingerprint image
        
        self.send_packet([self.FINGERPRINT_GETIMAGE])
        print('Getting Fingerprint Image')
        time.sleep(1)
        ret = self.uart.read()
        #print(ret)
        if ret[9] == 0:
            print('Get Image Done')
            return True
        print('No Fingerprint found')
        return False
        
    def image_convert(self): #Converting the fingerprint image into a template
        
        self.send_packet([self.FINGERPRINT_IMAGE2TZ, 0x01])
        print('Converting Image buffer to Template')
        time.sleep(1)
        ret = self.uart.read()
        #print(ret)
        if ret[9] == 0:
            print('Image Convert Done')
            return True
        print('Errro while Converting image')
        return False
    
    def store_template(self, fingerid): #Storing the Fingerprint template in a PageID
       
        self.send_packet([self.FINGERPRINT_STORE, 0x01, fingerid >> 8, fingerid & 0xff])
        print('storing Template')
        time.sleep(1)
        ret = self.uart.read()
        if ret[9] == 0:
            print('Finger template stored successfully')
            return True
        print('Error while storing the finger image')
        return False
    
    def finger_search(self): # Function for searching for the fingerprint matches
        
        self.send_packet([self.FINGERPRINT_SEARCH, 0x01, 0x00, 0x00, 0x00, 0xA3])
        print('Searching Finger')
        time.sleep(1)
        ret = self.uart.read()
        #print(ret)
        if ret[9] == 0:    
            fingerid = ret[11]
            print('Fingerid :{}'.format(fingerid))
            return fingerid;
        print('No Match found!!')
        return False
        
    def search_fingerprint(self):#Searching for the finger print match in the library
        
        self.get_image()
        self.image_convert()
        fingerid = self.finger_search()
        return fingerid;
     
    def register_fingerprint(self, fingerid): #Registering the fingerprint
        
        self.get_image()
        self.image_convert()
        self.store_template(fingerid)
                
    def send_packet(self, data):
        
        packet = [self.FINGERPRINT_STARTCODE >> 8, self.FINGERPRINT_STARTCODE & 0xFF]
        packet = packet + self.address
        packet.append(self.FINGERPRINT_COMMANDPACKET)  # the packet type

        length = len(data) + 2
        packet.append(length >> 8)
        packet.append(length & 0xFF)

        packet = packet + data
        
        checksum = sum(packet[6:])
        packet.append(checksum >> 8)
        packet.append(checksum & 0xFF)
        
        #print(packet)

        self.uart.write(bytearray(packet))  
        
    def get_packet(self):
         
        ret = self.uart.read()
        print(ret)

        
        
        
        
    

    
  
  
        

