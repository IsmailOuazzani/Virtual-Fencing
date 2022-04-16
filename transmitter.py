from machine import UART, Pin
import time
from esp8266 import ESP8266
esp01 = ESP8266()
esp8266_at_ver = None


#################
print("StartUP",esp01.startUP())
print("ReStart",esp01.reStart())
print("StartUP",esp01.startUP())
print("Echo-Off",esp01.echoING())
print("\r\n\r\n")
'''
Print ESP8266 AT command version and SDK details
'''
esp8266_at_var = esp01.getVersion()
if(esp8266_at_var != None):
    print(esp8266_at_var)
'''
set the current WiFi in SoftAP+STA
'''
esp01.setCurrentWiFiMode() # need to always put this for some reason

hotspot = esp01.makeHotspot("Sheep1", "password")
print(hotspot)

led = Pin(25, Pin.OUT)

while True:
    time.sleep(10)
