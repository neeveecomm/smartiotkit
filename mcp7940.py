import machine
from machine import I2C, Pin


class MCP7940:
        def __init__(self):
            self.mI2c = I2C(scl=Pin(21), sda=Pin(22), freq=100000)
            self.WriteReg(0x00, 0x80)
            #buf=bytearray(2)
            #buf[0]=0x00
            #buf[1]=0x80
            #self.mI2c.writeto(111, buf, True)
            
        def WriteReg(self,reg,data):
            buf=bytearray(2)
            buf[0] = reg
            buf[1] = data
            try:
                cnt = self.mI2c.writeto(111, buf, True)
                return cnt
            except Exception:
                return 0
            
        def ReadReg(self,reg):
            buf = bytearray(1)
            buf[0] = reg
            try:
                self.mI2c.writeto(111, buf, False)
                data = self.mI2c.readfrom(111, 1, True)
                return data
            except Exception:
                return 0
            
        def SetTime(self,hour,mins,sec):
            
            htn = hour//10
            hone = hour%10
            h = (htn<<4) | hone
                        
            mtn = mins//10
            mone = mins%10
            m = (mtn<<4) | mone
                       
            stn = sec//10
            sone = sec%10
            r = self.ReadReg(0x00)
            b7 = int(r[0]) & int(0x80)
            s = ((stn<<4) | b7) | sone
                                  
            bufh = bytearray(2)
            bufh[0] = 0x02
            bufh[1] = h
            self.mI2c.writeto(111, bufh, True)
            
            bufm = bytearray(2)
            bufm[0] = 0x01
            bufm[1] = m
            self.mI2c.writeto(111, bufm, True)
                
            bufs = bytearray(2)
            bufs[0] = 0x00
            bufs[1] = s
            self.mI2c.writeto(111, bufh, True)
            
        def SetDate(self,date,month,year):
            
            d10 = (date//10)
            d1 = (date%10)
            d = ((d10<<4) | d1)
            
            y10 = year//10
            y1 = year%10
            y = (y10<<4) | y1
            
            m10 = month//10
            m1 = month%10
            rm = self.ReadReg(0x05)
            b5 = int(rm[0]) & int(0x20)       
            mn = (m10<<4) | b5  | m1
            
            bufh = bytearray(2)
            bufh[0] = 0x04
            bufh[1] = d
            self.mI2c.writeto(111, bufh, True)
            
            bufs = bytearray(2)
            bufs[0] = 0x06
            bufs[1] = y
            self.mI2c.writeto(111, bufs, True)
            
            bufm = bytearray(2)
            bufm[0] = 0x05
            bufm[1] = mn
            self.mI2c.writeto(111, bufm, True)
                

                
        def GetTime(self):
            sec = self.ReadReg(0x00)
            sech = hex(sec[0]&~(1<<7))
            s0 = (int(sech) & 0xf0)
            s10 = (s0>>4)
            s1 = (int(sech) & 0x0f)
            s = ((s10 * 10) + s1)
            
            mins = self.ReadReg(0x01)
            mh = hex(mins[0])
            m0 = (int(mh) & 0xf0)
            m10 = (m0>>4)
            m1 = (int(mh) & 0x0f)
            m = ((m10 * 10) + m1)
            
            hours = self.ReadReg(0x02)
            hh = hex(hours[0])
            h0 = (int(hh) & 0xf0)
            h10 = (h0>>4)
            h1 = (int(hh) & 0x0f)
            h = ((h10 * 10) + h1)
            
            print("Time : {}h:{}m:{}s".format(h,m,s))
            
        def GetDate(self):
            
            date = self.ReadReg(0x04)
            dh = hex(date[0])
            d0 = (int(dh) & 0xf0)
            d10 = (d0>>4)
            d1 = (int(dh) & 0x0f)
            d = ((d10 * 10) + d1)
            
            month = self.ReadReg(0x05)
            mh = hex(month[0]&~(1<<5))
            m0 = (int(mh) & 0xf0)
            m10 = (m0>>4)
            m1 = (int(mh) & 0x0f)
            m = ((m10 * 10) + m1)
            
            year = self.ReadReg(0x06)
            yh = hex(year[0])
            y0 = (int(yh) & 0xf0)
            y10 = (y0>>4)
            y1 = (int(yh) & 0x0f)
            y = ((y10 * 10) + y1)
            print("Date : {}/{}/{}".format(d,m,y))
            

            
        def SetDay(self,days):
            
            day = hex(days)
            dayr0 = self.ReadReg(0x03)
            day0 = hex(dayr0[0])
            day1 = int(day0) & 0x38
            dayr = day1 | days
            
            bufda = bytearray(2)
            bufda[0] = 0x03
            bufda[1] = dayr
            self.mI2c.writeto(111, bufda, True)
            
        def GetDay(self):
            
            da = self.ReadReg(0x03)
            dayr = hex(da[0])
            days = int(dayr) & 0x07
            da = ["zero","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
            print("{}".format(da[days]))
            
        def SetAlarm0(self,hour,mins,sec,date,month,day):
            
            e = self.ReadReg(0x07)
            eh = hex(e[0])
            en0 = int(eh) | 0x10
            bufe0 = bytearray(2)
            bufe0[0] = 0x07
            bufe0[1] = en0
            self.mI2c.writeto(111, bufe0, True) #ENABLING ALM0EN to enable alarmo
            
            mk0 = 0x70       #setting alarm mask for all sec,h,m,date,month
            mk = mk0 & 0xf7  #make sure ALM0IF is disabled
            bufmk = bytearray(2)
            bufmk[0] = 0x0d
            bufmk[1] = mk
            self.mI2c.writeto(111, bufmk, True)
            
            htn = hour//10
            hone = hour%10
            h = (htn<<4) | hone
            bufh = bytearray(2)
            bufh[0] = 0x0c
            bufh[1] = h
            self.mI2c.writeto(111, bufh, True)
                        
            mtn = mins//10
            mone = mins%10
            m = (mtn<<4) | mone
            bufm = bytearray(2)
            bufm[0] = 0x0b
            bufm[1] = m
            self.mI2c.writeto(111, bufm, True)
            
            stn = sec//10
            sone = sec%10
            s = (stn<<4) | sone
            bufs = bytearray(2)
            bufs[0] = 0x0a
            bufs[1] = s
            self.mI2c.writeto(111, bufs, True)
            
            da = self.ReadReg(0x0d)
            da1 = hex(da[0])
            da2 = int(da1) & 0xf8
            d3 = int(da2) | day
            bufda = bytearray(2)
            bufda[0] = 0x0d
            bufda[1] = d3
            self.mI2c.writeto(111, bufda, True)
            
            dtn = date//10
            done = date%10
            d = (dtn<<4) | done
            bufd = bytearray(2)
            bufd[0] = 0x0e
            bufd[1] = d
            self.mI2c.writeto(111, bufd, True)
            
            mntn = month//10
            mnone = month%10
            mn = (mntn<<4) | mnone
            bufmn = bytearray(2)
            bufmn[0] = 0x0f
            bufmn[1] = mn
            self.mI2c.writeto(111, bufmn, True)
            
        def SetAlarm1(self,hour,mins,sec,date,month,day):
            
            e = self.ReadReg(0x07)
            eh = hex(e[0])
            en0 = int(eh) | 0x20
            bufe0 = bytearray(2)
            bufe0[0] = 0x07
            bufe0[1] = en0
            self.mI2c.writeto(111, bufe0, True) #ENABLING ALM0EN to enable alarm1
            
            mk0 = 0x70       #setting alarm mask for all sec,h,m,date,month
            mk = mk0 & 0xf7  #make sure ALM0IF is disabled
            bufmk = bytearray(2)
            bufmk[0] = 0x14
            bufmk[1] = mk
            self.mI2c.writeto(111, bufmk, True)
            
            htn = hour//10
            hone = hour%10
            h = (htn<<4) | hone
            bufh = bytearray(2)
            bufh[0] = 0x13
            bufh[1] = h
            self.mI2c.writeto(111, bufh, True)
                        
            mtn = mins//10
            mone = mins%10
            m = (mtn<<4) | mone
            bufm = bytearray(2)
            bufm[0] = 0x12
            bufm[1] = m
            self.mI2c.writeto(111, bufm, True)
            
            stn = sec//10
            sone = sec%10
            s = (stn<<4) | sone
            bufs = bytearray(2)
            bufs[0] = 0x11
            bufs[1] = s
            self.mI2c.writeto(111, bufs, True)
            
            da = self.ReadReg(0x14)
            da1 = hex(da[0])
            da2 = int(da1) & 0xf8
            d3 = int(da2) | day
            bufda = bytearray(2)
            bufda[0] = 0x14
            bufda[1] = d3
            self.mI2c.writeto(111, bufda, True)
            
            dtn = date//10
            done = date%10
            d = (dtn<<4) | done
            bufd = bytearray(2)
            bufd[0] = 0x15
            bufd[1] = d
            self.mI2c.writeto(111, bufd, True)
            
            mntn = month//10
            mnone = month%10
            mn = (mntn<<4) | mnone
            bufmn = bytearray(2)
            bufmn[0] = 0x16
            bufmn[1] = mn
            self.mI2c.writeto(111, bufmn, True)    
            
            
            
        def Binread(self):
            mins = self.ReadReg(0x07)
            print("Control Register value is {}".format(bin(mins[0])))
            
            hour = self.ReadReg(0x0d)
            print("Alarm0 Register value is {}".format(bin(hour[0])))
           
            sec = self.ReadReg(0x14)
            print("Alam1 Register value is {}".format(bin(sec[0])))
            
        
t = MCP7940()
t.GetTime()
t.GetDate()

         
         

    
    
         

         
