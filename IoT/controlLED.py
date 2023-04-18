import serial
from gpiozero import LED
from time import sleep
from RPLCD.i2c import CharLCD
import os

ser = serial.Serial('/dev/ttyS0', 115200)
lcd = CharLCD('PCF8574', 0x27)
led = [LED(6), LED(13), LED(19), LED(26)]
cur = 0
rs = ['OFF', 'OFF', 'OFF', 'OFF']
outString = 'R1: {}  R2: {} \r\nR3: {}  R4: {}'.format(rs[0], rs[1], rs[2], rs[3])
while True:
    lcd.write_string(outString)
    res=ser.readline()
    
    if res:
        if res == b'a\n':
            cur = 0
            print('1')
        
        if res == b'b\n':
            cur = 1
            print('2')

        if res == b'c\n':
            cur = 2
            print('3')

        if res == b'd\n':
            cur = 3
            print('4')
        if res == b'-1\n':
            led[cur].off()
            if rs[cur] == 'ON ':
                os.system(f'mpg321 /home/pi/Music/{cur+1}off.mp3')
            rs[cur] = 'OFF'
            print('off')
            
        if res == b'1\n':
            led[cur].on()
            if rs[cur] == 'OFF':
                os.system(f'mpg321 /home/pi/Music/{cur+1}on.mp3')
            rs[cur] = 'ON '
            print('on')
        outString = 'R1: {}  R2: {} \r\nR3: {}  R4: {}'.format(rs[0], rs[1], rs[2], rs[3])
        lcd.clear() 
