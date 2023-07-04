Author: John Enblom (je224by)
A project in the course 1DT305 - Introduction to Applied Internet of Things by LNU. 
This tutorial will demonstrate how to use sensors and collect data, how to store this data on the cloud and finally how to visualize it.

# Objective

The objective of this project is to get acquainted with how to work with the with sensors, and more precisley in this project, how to measure the temperature in a room. This can be used to see how different things in the room affects the temperature, say having the blinds in the windows down or not. It also helps gets a more accurate look at the exact temperature and how it changes throughout the day.
I estimate it will take you around 3 hours to set everything up if you are a beginner.

# Material

Listed below is the hardware used in the project. I have also listed the vendor that i used, but you can choose what works best for you.

|  | Material | Description | Price (SEK) | Vendor |
| -------- | -------- | -------- | -------- | -------- |
|![](https://hackmd.io/_uploads/H1iUpAWYh.jpg)| Raspberry Pi Pico W | A microcontroller that is the head of operations during this project. For more information read its [datasheet](https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf).  | 98 | [Elektrokit ](https://www.electrokit.com/produkt/raspberry-pi-pico-w/)|
| ![](https://hackmd.io/_uploads/SJ7U-yGF3.jpg)| MCP9700 TO-92 temperature sensor | Temperature sensor with analog output and has a measurement ranget of -40°C-125 °C. [Datasheet](https://www.electrokit.com/uploads/productfile/41011/21942e-2.pdf). | 10.75 | [Elektrokit](https://www.electrokit.com/en/product/mcp9700-e-to-to-92-temperature-sensor/) |
| ![](https://hackmd.io/_uploads/Sk5zfyfK3.jpg)| 5mm red LED | Datasheet for all LEDs in this project can be found [here](https://www.electrokit.com/uploads/productfile/40307/JSL-502-4030702x.pdf). | 5 | [Elektrokit](https://www.electrokit.com/en/product/led-5mm-rod-diffus-1500mcd/) |
| ![](https://hackmd.io/_uploads/SkmzmJGK3.jpg) | 5mm yellow LED | Information above. | 5 | [Elektrokit](https://www.electrokit.com/produkt/led-5mm-gul-diffus-1500mcd/) |
| ![](https://hackmd.io/_uploads/H1YQ71Mtn.jpg) | 5mm green LED | Information above. | 5 | [Elektrokit](https://www.electrokit.com/produkt/led-5mm-gron-diffus-80mcd/) |
| ![](https://hackmd.io/_uploads/HJQ37kGtn.jpg)| Breadboard  | The breadboard is used to connect everything. | 69     | [Elektrokit](https://www.electrokit.com/en/product/solderless-breadboard-840-tie-points-2/) |
| ![](https://hackmd.io/_uploads/SJQ7VJGY3.jpg)| Jumper Wires M-to-M | Wires with connectors in both ends, used on the breadboard between sensors and the Pico. | 29 | [Elektrokit](https://www.electrokit.com/en/product/jumper-wires-20-pin-30cm-male-male/) |
| ![](https://hackmd.io/_uploads/BkJqEkMt2.png)| 3x Resistor 0.25W 330ohm | The resistors are used to lower the flow of current, helping us from blowing up our LEDs. | 3 | [Elektrokit](https://www.electrokit.com/en/product/resistor-carbon-film-0-25w-330ohm-330r/) |
|![](https://hackmd.io/_uploads/rJPRVJfK2.jpg)| Micro-USB cable | Used to connect the Pico to a computer and to power it.  | 39     | [Elektrokit](https://www.electrokit.com/produkt/usb-kabel-a-hane-micro-b-5p-hane-1-8m/) |

# Computer Setup

For this project I choose [Visual Studio Code](https://code.visualstudio.com/download) as the IDE. To use with the IDE we also install [PyMakr](https://github.com/pycom/pymakr-vsc/blob/HEAD/GET_STARTED.md) and [NodeJS](https://nodejs.org/en).

I personally used Windows but any OS will work for this project, just make sure to follow the correct download and installation guides for your chosen OS.

### Step by Step guide on getting started:
1. Download and install VSC. Add the PyMakr Extension.
2. Download and install NodeJS.
3. Update your [firmware](https://micropython.org/download/rp2-pico-w/) on the Raspberry Pi Pico W.
4. Create a new project and choose your Pico as the device.

# Putting everything together

This image illustrates how to put the wires together. Blue wires are connected to GND, yellow and black to GPIO and the red cable to the 3v out connection. Make sure the resistor is connected to the LEDs longer part. 

![](https://hackmd.io/_uploads/r1C7IxfFn.png)
 
# Platform

The choosen platform is Adafruit IO (AIO). AIO is a very beginner friendly tool for getting started in IoT. It allows you to send information and visualise it in a simple way.

To get started you need to [create an account ](https://io.adafruit.com/Enblom/overview). When this is done you can [create a feed](https://learn.adafruit.com/adafruit-io-basics-feeds) which will take your temperature information.

# The code

This is the code structure for this project:
![](https://hackmd.io/_uploads/S1kilZfKn.png)

The lib folder is where we put all external libraries. For this project two 
external libraries were used, [MQTT](https://github.com/croos90/IoT_temperature_humidity_sensor/blob/main/src/lib/mqtt.py) and [PicoZero](https://github.com/RaspberryPiFoundation/picozero/blob/main/picozero/picozero.py). The MQTT library ofcourse is used to allow us to send data using the MQTT protocoll and the PicoZero library has useful funtctions for the LEDs.

We then want to create a credentials.py file. In this file we put constant values that are needed in the project but shouldn't be in the other files.
Since it consists of sensitive information I suggest to create a .gitignore file where you add 'credentials.py' in case you are creating this project in git so that you dont push it to the internet and only have the file locally.
Structure the file like this:
```python=
secrets = {
'ssid' : 'YOUR_WiFi_SSID',
'password' : 'YOUR_WiFi_PASSWORD'
'user' : 'AIO_USERNAME'
'key' : 'AIO_KEY'
'feed' : 'AIO_FEED_PATH'
}
```

We then create our boot.py. This file contains the code that is run on boot and need to happen before anything else. In this case we use the file to connect to the WiFi.

Finally we create the main.py. This is the file that contains all of the functionallity. We read sensor data and transmitt it to AIO. In this file are 3 main functions:

```python=
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
```

This code is used for our temperature sensor, we use the datasheet to read how to convert the readings from the sensor the values we want (degrees in celsius with one decimal).

```python=
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
```

In our main function we first connect AIO and then enter our loop were we gather and transmit data. First we read the temperature, then we transmit it using client.publish() before finally calling activate_LED()

```python=
def activate_LED(temp):
    #Activate green LED if temp is between 18 and 22 Celsius, yellow if 16-18 or 22-24 and otherwise red
    if temp >= 18.0 and temp <= 22.0:
        green_LED.blink(on_time=1,off_time=9, n=3, wait=True)
    elif temp >= 16.0 and  temp < 18.0 or temp > 22.0 and temp <= 24.0:
        yellow_LED.blink(on_time=1,off_time=9, n=3, wait=True)
    else:
        red_LED.blink(on_time=1,off_time=9, n=3, wait=True)

```

In this function we use the temp value to determine what LED to blink. I have choosen to make the LED to blink onces every 10 seconds for 30 seconds. We have enabled wait to True, this sleeps our entire thread by waiting until the blinking is done. This makes sure we transmit data at the desired rate. It is also here the temperature range is determined for what LED should blink. Since I measure the temperature in my bedroom I have choose that it should blink green for temps 18-22, yellow for 16-18 and 22-24 and red for all other values. This can be adjusted to fit your needs.

# Transmitting the data

To transmit data we use WiFi and MQTT protocol. The data is sent every 30 seconds to get accurate data for temperature changes.

# Presenting the data

Finally we will present the data in AIO using a [dashboard](https://learn.adafruit.com/adafruit-io-basics-dashboards). I personally have used 3 blocks, 1 gauge and 2 line charts. I use these to visualize the current exact temperature value, the values from the last 24 h and the values from the last 30 days. As noted above data is saved every 30 seconds.

![](https://hackmd.io/_uploads/HyAT1bzYn.png)

Note: since I have not had my project active for that long the duration of my charts are not yet showing what they will as described.

# Finalizing the design

My final thoughts on this project that it was a fun way to get introduced to IoT and very beginner friendly. Just creating this project and doing research made me get a lot of other ideas which I hopefully will go through with in the future.

![](https://hackmd.io/_uploads/HywC9bGF2.jpg)

Note: This is not setup exactly as described before, this is because I used parts I hade avaible, but the method described is the cheapest and there is no difference.












