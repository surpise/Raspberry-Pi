#!/usr/bin/env python3
from datetime import datetime
from time import sleep
import pifacecad
from pifacecad.tools.scanf import LCDScanf
from pifacecad.tools.question import LCDQuestion
from pyowm.owm import OWM
import os

cad = pifacecad.PiFaceCAD()
cad.lcd.backlight_on()
cad.lcd.cursor_off()
cad.lcd.blink_off()

but = switch = 0
time = [0, 0, 'AM']
backlight = True
selectMode = stopwatchMode = False
owm = OWM('f0bc9b5e67ea139dba286b4394359bed')
mgr = owm.weather_manager()
city = ['KR Seoul', 'US New York', 'UK London', 'JP Tokyo', 'EG Cairo']

def switch_clicked(event):
    global switch
    tmp = event.pin_num
    if not selectMode or (selectMode and tmp != 5):
        if tmp == 0: cad.lcd.clear()
        switch = tmp

def button_clicked(event):
    global but
    but = int(event.ir_code)

swlistener = pifacecad.SwitchEventListener(chip=cad)
for i in range(8):
    swlistener.register(i, pifacecad.IODIR_FALLING_EDGE, switch_clicked)
swlistener.activate()

irlistener = pifacecad.IREventListener(prog='clock', lircrc="/etc/lirc/.lircrc")
for k in range(1, 6):
    irlistener.register(str(k), button_clicked)
irlistener.activate()

# 알람 시계 구현
def clock():	
	now = datetime.now()
	cad.lcd.set_cursor(0,0)
	cad.lcd.write(now.strftime("%m/%d %a"))
	cad.lcd.set_cursor(0,1)
	cad.lcd.write(now.strftime("%I:%M:%S %p"))
	cad.lcd.cursor_off()
	if now.strftime("%I%M%p") == f'{time[0]:02d}{time[1]:02d}{time[2]}':
		if now.strftime("%S") == '00':
			cad.lcd.clear()
			cad.lcd.set_cursor(0,0)
			cad.lcd.write("Alarm!")
			cad.lcd.set_cursor(0,1)
			cad.lcd.write(now.strftime("%I:%M:%S %p"))
			cad.lcd.cursor_off()
			os.system("mplayer /home/pi/Music/Alarm.mp3")

	sleep(0.8)

# 알람 설정
def alarmSet():
    global scanner, time, selectMode
    selectMode = True
    cad.lcd.clear()
    cad.lcd.set_cursor(0,0)
    scanner = LCDScanf("Alarm %2i:%2i %m%r", custom_values=('AM', 'PM'))
    time = scanner.scan()
    cad.lcd.clear()
    cad.lcd.cursor_off()
    cad.lcd.write('Alarm Set')

# 알람 확인
def alarmCheck():
    global switch, but
    cad.lcd.clear()
    cad.lcd.set_cursor(0,0)
    cad.lcd.write("Your Alarm at")
    cad.lcd.set_cursor(0,1)
    cad.lcd.write(f'{time[0]:02d}:{time[1]:02d} {time[2]}')
    cad.lcd.cursor_off()
    sleep(2)
    cad.lcd.clear()
    switch = 0
    but = 0

# 종료
def shutDown():
    cad.lcd.clear()
    cad.lcd.backlight_off()
    swlistener.deactivate()
    irlistener.deactivate()

# 날씨 확인 구현
def weatherMode():
    global selectMode, switch
    selectMode = True
    q = LCDQuestion('Choose the City', answers = city, selector='> ')
    ans = q.ask()
    cad.lcd.clear()
    cad.lcd.set_cursor(0, 0)
    cad.lcd.write(f'{city[ans]}')
    cad.lcd.set_cursor(0, 1)
    place = city[ans].split()
    observation = mgr.weather_at_place(f'{place[1]},{place[0]}')
    weather = observation.weather
    cad.lcd.write(weather.detailed_status)
    switch = -1

def lcd_backlight():
    global backlight, but
    if backlight:
        cad.lcd.backlight_off()
        backlight = False
    else:
        cad.lcd.backlight_on()
        backlight = True
    but = 0

# 스톱 워치 구현
def stopwatch():
    global stopwatchMode, start, but
    if not stopwatchMode:
        if but == 3:
            cad.lcd.clear()
            cad.lcd.set_cursor(0,0)
            cad.lcd.write('Stop Watch')
            cad.lcd.set_cursor(0,1)
            cad.lcd.write('0:00:00:00')
            stopwatchMode = True
        elif but == 5:
            cad.lcd.clear()
            but = 0
    elif stopwatchMode:
        if but == 4:
            start = datetime.now()
            but = -1
            while but == -1:
                cad.lcd.set_cursor(0,1)
                now = str(datetime.now() - start).split(':')
                cad.lcd.write(f'{now[0]}:{now[1]}:{now[2][0:2]}:{now[2][3:5]}')
        if but == 5: stopwatchMode = False; but = -1


while True:
	if switch == 0 and but == 0: clock()
	elif switch == 2: alarmSet()
	elif switch == 3 or but == 1: alarmCheck()
	elif switch == 4: shutDown(); break
	elif switch == 5: weatherMode()
	elif but == 2: lcd_backlight()
	elif but == 3 or but == 4 or but == 5: stopwatch()
	selectMode = False
