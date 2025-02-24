import cv2
import numpy as np
import smtplib, ssl
import serial

import BlynkLib
import RPi.GPIO as GPIO
from time import sleep
import time
import os #Import for file handling
import glob #Import for global
import urllib3
import Adafruit_DHT
from urllib.request import urlopen
import sys
import math
import string
import smtplib
import os.path
import requests, json
from email.mime.text import MIMEText#email.mime.text.MIMEText(_text[, _subtype[, _charset]])
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase#email.mime.base.MIMEBase(_maintype(e.g. text or image), _subtype(e.g. plain or gif), **_params(e.g.key/value dictionary))
from email import encoders

WRITE_API = "PTQF2P9NU32ML90B" # ThingSpeak API key 
BASE_URL = "https://api.thingspeak.com/update?api_key={}".format(WRITE_API)

BLYNK_AUTH = '4kJ8XNtfNnDVkvtY1w37x7j6eBtyF0YE'
blynk = BlynkLib.Blynk(BLYNK_AUTH,
#        insecure=True,          # disable SSL/TLS
server='blynk.cloud', # fra1.blynk.cloud or blynk.cloud
port=80,                # set server port
heartbeat=30,           # set heartbeat to 30 secs
log=print              # use print function for debug logging
)
motor_pin1=26
motor_pin2=19
motor_pin3=13
motor_pin4=6
moisture=2
dt=4
moisture=15
pump=17
servo=12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
GPIO.setup(motor_pin1, GPIO.OUT)  # E
GPIO.setup(motor_pin2, GPIO.OUT) # RS
GPIO.setup(motor_pin3, GPIO.OUT) # DB4
GPIO.setup(motor_pin4, GPIO.OUT) # DB5
GPIO.setup(moisture,GPIO.IN)
GPIO.setup(pump, GPIO.OUT)
GPIO.setup(servo, GPIO.OUT)


GPIO.setup(dt, GPIO.IN)
GPIO.setup(moisture, GPIO.IN)
sensor=Adafruit_DHT.DHT11

GPIO.output(motor_pin1,False)
GPIO.output(motor_pin2,False)
GPIO.output(motor_pin3,False)
GPIO.output(motor_pin4,False)
GPIO.output(pump, False)
m=GPIO.PWM(servo,50);
m.start(2.5)
email = 'akhiljeshwanth7@gmail.com'
password = 'Jeshwanth@23'
send_to_email = 'akhiljeshwanth7@gmail.com'
subject = 'msg from agribot'
message = 'Captured Image'
file_location = '/home/pi/Desktop/sourcecode/AGRI0.png'
msg = MIMEMultipart()#Create the container (outer) email message.
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject


msg.attach(MIMEText(message, 'plain'))#attach new  message by using the Message.

# Register Virtual Pins
@blynk.VIRTUAL_WRITE(0)
def my_write_handler(value):
    print('Value: {}'.format(value))
    #value={}
    #print('{}'.format(value))
    if value == ['1']:
      GPIO.output(motor_pin1,False);
      GPIO.output(motor_pin2,True);
      GPIO.output(motor_pin3,True); 
      GPIO.output(motor_pin4,False);
      print("Farward")  
    if value == ['0']:
        print(' no hellow')
# Register Virtual Pins
@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value):
    print('Value: {}'.format(value))
    #value={}
    #print('{}'.format(value))
    if value == ['1']:
      GPIO.output(motor_pin1,True);
      GPIO.output(motor_pin2,False);
      GPIO.output(motor_pin3,False); 
      GPIO.output(motor_pin4,True);
      print("Backward")  
    if value == ['0']:
        print(' no hellow')
# Register Virtual Pins
@blynk.VIRTUAL_WRITE(2)
def my_write_handler(value):
    print('Value: {}'.format(value))
    #value={}
    #print('{}'.format(value))
    if value == ['1']:
      GPIO.output(motor_pin1,False);
      GPIO.output(motor_pin2,False);
      GPIO.output(motor_pin3,True); 
      GPIO.output(motor_pin4,False);
      print("Right")  
    if value == ['0']:
        print(' no hellow')
## Register Virtual Pins
@blynk.VIRTUAL_WRITE(3)
def my_write_handler(value):
    print('Value: {}'.format(value))
    #value={}
    #print('{}'.format(value))
    if value == ['1']:
      GPIO.output(motor_pin1,True); 
      GPIO.output(motor_pin2,False);
      GPIO.output(motor_pin3,False);
      GPIO.output(motor_pin4,False);
    
      print("Left")  
    if value == ['0']:
        
        print(' no hellow')
## Register Virtual Pins
@blynk.VIRTUAL_WRITE(4)
def my_write_handler(value):
    print('Value: {}'.format(value))
    #value={}
    #print('{}'.format(value))
    if value == ['1']:
      GPIO.output(motor_pin1,False); 
      GPIO.output(motor_pin2,False);
      GPIO.output(motor_pin3,False);
      GPIO.output(motor_pin4,False);
    
      print("STOP")  
    if value == ['0']:
        print(' no hellow')
# Register Virtual Pins
@blynk.VIRTUAL_WRITE(5)
def my_write_handler(value):
    print('Value: {}'.format(value))
    #value={}
    #print('{}'.format(value))
    if value == ['1']:
        
        print("Data Upload")
        humidity, temperature = Adafruit_DHT.read_retry(sensor,dt )
        water=GPIO.input(moisture)
        soil=water
##        y = int(temperature)
##        x = int(humidity)
##        z = int(water)

        print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
            
        print("MOISTURE VALUE(I.E DRY=1,WET=0)=",water)
        soil=water
        thingspeakHttp = BASE_URL + "&field1={:.2f}&field2={:.2f}".format(temperature,soil)
        print(thingspeakHttp)
        
        conn = urlopen(thingspeakHttp)
        print("Response: {}".format(conn.read()))
        conn.close()
    
        print("Left")  
##    if value == ['0']:
##        print(' no hellow')
# Register Virtual Pins
@blynk.VIRTUAL_WRITE(6)
def my_write_handler(value):
    print('Value: {}'.format(value))
    #value={}
    #print('{}'.format(value))
    if value == ['1']:
        print("Image Upload")
        print("with in cemara")
        camera = cv2.VideoCapture(0)
        address="http://192.168.96.35.8080/video"
        #address="http://192.168.0.168:8080/video"
        camera .open(address) 
        #for i in range(10):
        return_value, image = camera.read()
        cv2.imwrite('AGRI0.png', image)
        print('AGRI IMG captured')
        
        time.sleep(2)
            #break
        del(camera)

        
        
        filename = os.path.basename(file_location)#function returns the tail of the path
        attachment = open(file_location, "rb") #“rb” (read binary)
        part = MIMEBase('application', 'octet-stream')#Content-Type: application/octet-stream , image/png, application/pdf
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)#Content-Disposition: attachment; filename="takeoff.png"
        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)# Send the message via local SMTP server.
        print("SENDING MAIL")
        server.starttls()# sendmail function takes 3 arguments: sender's address, recipient's address and message to send
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, send_to_email, text)
        print("mail sent")
        server.quit()
##    if value == ['0']:
##        print(' no hellow')
# Register Virtual Pins
@blynk.VIRTUAL_WRITE(7)
def my_write_handler(value):
    print('Value: {}'.format(value))
    #value={}
    #print('{}'.format(value))
    if value == ['1']:
        
        print("Pump on...watering")
        GPIO.output(pump , 1) 
    if value == ['0']:
        print("Pump off")
        GPIO.output(pump , 0)
# Register Virtual Pins
@blynk.VIRTUAL_WRITE(8)
def my_write_handler(value):
    s=0
    print('Value: {}'.format(value))
    #value={}
    #print('{}'.format(value))
    if value == ['1']:
        print("Servo on...seeding")
        while s<=5:
            s=s+1
            m.ChangeDutyCycle(6.5)
            time.sleep(0.5)
            m.ChangeDutyCycle(2.5)
            time.sleep(0.5)
    if value == ['0']:
        #s=1
        print("No seeding")
        
while True:
  blynk.run()
  
    
  
  
 
          
          
            
        
  

 
  
 


    

