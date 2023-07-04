import machine
from picozero import LED
import time
from mqtt import MQTTClient
import ubinascii
import micropython
from credentials import secrets

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = secrets['user']
AIO_KEY = secrets['key']
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_TEMPERATURE_FEED = secrets['temp_feed']

# Componet configuration
adc = machine.ADC(27)
green_LED = LED(2)
yellow_LED = LED(5)
red_LED = LED(9)

# Calculate constants
sf = 4095/65535 # Scale factor
volt_per_adc = (3.3 / 4095)

def temp_reading():
    millivolts = adc.read_u16()

    adc_12b = millivolts * sf

    volt = adc_12b *volt_per_adc

    # MCP9700 characteristics
    dx = abs(50 - 0)
    dy = abs(0 - 0.5)

    shift = volt - 0.5

    return round(shift / (dy / dx), 1)

def activate_LED(temp):
    #Activate green LED if temp is between 18 and 22 Celsius, yellow if 16-18 or 22-24 and otherwise red
    if temp >= 18.0 and temp <= 22.0:
        green_LED.blink(on_time=1,off_time=9, n=3, wait=True)
    elif temp >= 16.0 and  temp < 18.0 or temp > 22.0 and temp <= 24.0:
        yellow_LED.blink(on_time=1,off_time=9, n=3, wait=True)
    else:
        red_LED.blink(on_time=1,off_time=9, n=3, wait=True)


def main():
    # Use the MQTT protocol to connect to Adafruit IO
    client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY, keepalive = 60)
    client.connect()

    while True:
        #Sensor readings
        temp = temp_reading()

        #Sending data to AIO
        client.publish(AIO_TEMPERATURE_FEED, str(temp))

        #Turn on LED and wait 30 seconds
        activate_LED(temp)

if __name__ == "__main__":
    while True:
        try:
            main()
        except OSError as e:
            reset()
        time.sleep(1)