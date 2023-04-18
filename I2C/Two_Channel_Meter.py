from RPLCD.i2c import CharLCD
from time import sleep
import random
import numpy as np

lcd = CharLCD('PCF8574', 0x27)

char0 = (0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000)
char1 = (0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000)
char2 = (0b11000, 0b11000, 0b11000, 0b11000, 0b11000, 0b11000, 0b11000, 0b11000)
char3 = (0b11100, 0b11100, 0b11100, 0b11100, 0b11100, 0b11100, 0b11100, 0b11100)
char4 = (0b11110, 0b11110, 0b11110, 0b11110, 0b11110, 0b11110, 0b11110, 0b11110)

lcd.create_char(0,char0)
lcd.create_char(1,char1)
lcd.create_char(2,char2)
lcd.create_char(3,char3)
lcd.create_char(4,char4)            # 만든 Custom Character를 0 ~ 4번 으로 등록

t = np.linspace(0,2*np.pi,50)       # 0 ~ 2π를 50등분하여 1차원 배열로 저장

while True:
    for i in range(50):
        n = random.random()                         # 0 ~ 1 사이의 난수를 생성
        ch1 = 40 + (20 * np.cos(t)) + (30 * n)      # 채널 1 = 40 + 20 cos⁡𝑡 + 30𝑛 
        ch2 = 40 + (20 * np.sin(t)) + (30 * n)      # 채널 2 = 40 + 20 sin⁡𝑡 + 30𝑛

        ch1Box = ch1//5                             # 채널 1의 꽉찬 박스의 개수
        ch1Slice = ch1 % 5                          # 채널 1의 마지막 박스의 채널 데이터 값

        ch2Box = ch2//5                             # 채널 2의 꽉찬 박스의 개수
        ch2Slice = ch2 % 5                          # 채널 2의 마지막 박스의 채널 데이터 값

        lcd.home()
        for j in range(16):
            if ch1Box[i] > j: lcd.write(255)                    # 꽉찬 박스의 개수만큼 출력
            elif ch1Box[i] == j: lcd.write(int(ch1Slice[i]))    # 남은 값에 해당하는 비트맵을 출력
            else: lcd.write(254)                                # 그 이상은 빈칸을 출력
        lcd.crlf()
        for j in range(16):                                     # 위와 동일하게 2행에서 실행
            if ch2Box[i] > j: lcd.write(255)                    
            elif ch2Box[i] == j: lcd.write(int(ch2Slice[i]))
            else: lcd.write(254)
        sleep(0.01)                                             # 0.01초 간격으로 갱신
