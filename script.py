import paho.mqtt.client as paho
from paho import mqtt
from time import sleep
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

broker = "broker.hivemq.com"
port = 1883
timeout = 60

username = 'sunrise_team'
password = 'smkn4'
topic = "ubidots"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code"+str(rc))

def on_publish(client,userdata,result):
    print("data published \n")

client1 = paho.Client("",userdata=None,protocol=paho.MQTTv5)
client1.username_pw_set(username=sunrise_team,password=smkn4)
client1.on_connect = on_connect
client1.on_publish = on_publish
client1.connect(broker,port,timeout)

 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if _name_ == '_main_':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Dihentikan")
        GPIO.cleanup()