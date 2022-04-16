import board
import time
import digitalio
import pwmio
import sys
import time
from microcontroller import cpu
import busio
import math
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX


#Sound output setup
buzzer = pwmio.PWMOut(board.A0, duty_cycle = 0,
frequency = 2000, variable_frequency = True)

# Configure the internal GPIO connected to the LED as a digital output -- Proxy for electric shock
led = digitalio.DigitalInOut(board.A5)
led.direction = digitalio.Direction.OUTPUT
led.value = False

# Get wifi details and more from a secrets.py file
try:
    from secret import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Set up SPI pins
esp32_cs = digitalio.DigitalInOut(board.CS1)
esp32_ready = digitalio.DigitalInOut(board.ESP_BUSY)
esp32_reset = digitalio.DigitalInOut(board.ESP_RESET)

# Connect RP2040 to the WiFi module's ESP32 chip via SPI, then connect to WiFi
spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets)

# get signal strengths
#networks = esp.scan_networks()
#print(networks)

#for ap in esp.scan_networks():
#   if ap['ssid'] == "Sheep1":
#        print("\t%s\t\tRSSI: %d" % (str(ap['ssid'], 'utf-8'), ap['rssi']))
#        continue

#Connect to WiFi
print("Connecting to WiFi...")
wifi.connect()
print("Connected")

shock_count = 0
total_shock_count = 0
boundary = 10

inter = 1
n = 30

print("Start")

while True:
    values = []
    for i in range(n):
        #for ap in esp.scan_networks():
        #    if ap['ssid'] == "Sheep1":
        #        values.append(ap['rssi'])
        #        print(ap['rssi'])
        values.append(esp.rssi)
        time.sleep(inter/n)
    avg_rssi = sum(values)/n
    #fre = buzzer.frequency
    distance = 10**((-41 - avg_rssi)/(20)) #[m] Calibrate by holding transmitter 1m away and replace '-41' with measured RSSI
    print("Distance from signal:", distance, 'm')
    #print(avg_rssi)
    if (distance > boundary) and led.value == False:
        print("Out of bounds!")
        print("RSSI:", avg_rssi)
        print("Shock count:", shock_count, "Total shock count", total_shock_count, "f:", buzzer.frequency, "Hz")
        buzzer.duty_cycle = 10000
        if buzzer.frequency < 4200:
            buzzer.frequency = buzzer.frequency + 300
        #print(buzzer.frequency)
        if buzzer.frequency >= 4200 and ((shock_count >= 4) or (total_shock_count >= 5)):
            buzzer.duty_cycle = 0
            print("Too many signals for the sheep :( System disabled.")

        elif buzzer.frequency >= 4200 and (shock_count < 4) and (total_shock_count < 5):
            print("shock!")
            buzzer.duty_cycle = 0
            led.value = True


    elif led.value == True:
        time.sleep(1)
        shock_count += 1
        total_shock_count += 1
        led.value = False
        buzzer.frequency = 2000

    else:
        print("In the field :)")
        #print("RSSI:", avg_rssi)
        led.value = False
        time.sleep(0.1)
        buzzer.duty_cycle = 0
        shock_count = 0
        buzzer.frequency = 2000
