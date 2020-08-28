# Smart IoT Kit

Micro Python based software implementation for NEEVEE Smart IoT Kit.

fingerprint.py

   This library contains the functions for the fingerprint module that are required to:

         *Connect to the fingerprint module through UART serial communication and verify the password with the fingerprint module and establish
          connection between the module and ESP32.

         *Functions to get the fingerprint image and convert it to template and store that template in the fingerprint module library and give an
          unique ID to all fingerprint template. 

         *Functions to search for matching fingerprint in the Fingerprint module library and retruns the unique ID of that matched fingerprint.

mcp7940.py
  
   MCP7940 is an external RTC used in the NEEVEE Smart IoT Kit. 

   This library contains the functions for MCP7940 that are required to:
   
         *Set the time and date for MCP7940.
        
         *Get the time and date from MCP7940.
 
         *Set the alarm for MCP7940.

mqtt.py

   This library contains the functions for MQTT protocol, that are required to:

         *Connect NEEVEE Smart IoT kit to the AWS IoT cloud

         *Publish message from NEEVEE Smart IoT kit to the AWS IoT cloud
wifi.py
  
   This library contains the function for inbuilt WLAN in the ESP32, that are required to:

         *Automatically scan and connect to the available WLAN ap stations based on signal strength

main_test.py
   
   This is the main application that will import functions from the libraries, that will execute following operations

         *Connect to the WLAN ap station

         *Establish connection between the NEEVEE Smart IoT Kit and AWS IoT cloud through the MQTT protocol

         *Automatically sense on finger press in the fingerprint module and search for the matching finger ID in the fingerprint module library

         *Send the found fingerprint ID to the AWS IoT cloud through MQTT protocol

wifiap.json
 
   This file contains the SSID and password for the WLAN ap stations

userled.py
   
   This library contains the functions to access and control the two inbuilt LEDs in NEEVEE Smart IoT Kit 