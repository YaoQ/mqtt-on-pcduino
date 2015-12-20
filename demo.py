#!/usr/bin/env python
import paho.mqtt.client as mqtt
import json
import gpio
led_pin = "gpio13"

def setup():
    gpio.pinMode(led_pin, gpio.OUTPUT)
    gpio.digitalWrite(led_pin, gpio.LOW)

def destroy():
    gpio.digitalWrite(led_pin,gpio.LOW)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("gpio")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    gpio_msc = json.loads(str(msg.payload))
    
    if gpio_msc['value'] == 0:
        gpio.digitalWrite(led_pin, gpio.LOW)
    else:
        gpio.digitalWrite(led_pin, gpio.HIGH)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
setup()

try:
    client.connect("192.168.1.106", 1883, 60)
    client.loop_forever()

except KeyboardInterrupt:
    client.disconnect()
    destroy()

