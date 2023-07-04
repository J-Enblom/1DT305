import machine
from picozero import LED
import utime

adc = machine.ADC(27)
green_LED = LED(2)
yellow_LED = LED(5)
red_LED = LED(9)

sf = 4095/65535 # Scale factor
volt_per_adc = (3.3 / 4095)
while True:
    millivolts = adc.read_u16()

    adc_12b = millivolts * sf

    volt = adc_12b *volt_per_adc

    # MCP9700 characteristics
    dx = abs(50 - 0)
    dy = abs(0 - 0.5)

    shift = volt - 0.5

    temp = round(shift / (dy / dx), 1) - 1 # for correct values
    print (temp)

    if temp >= 18.0 and temp <= 22.0:
        green_LED.blink(on_time=1,off_time=9, n=3, wait=True)
        print("finished blinking")
    elif temp >= 16.0 and  temp < 18.0 or temp > 22.0 and temp <= 24.0:
        yellow_LED.blink(on_time=1,off_time=9, n=3, wait=True)
        print("finished blinking")
    else:
        red_LED.blink(on_time=1,off_time=9, n=3, wait=True)
        print("finished blinking")
    