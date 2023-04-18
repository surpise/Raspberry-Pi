from RPLCD.i2c import CharLCD
from time import sleep

lcd = CharLCD('PCF8574', 0x27)
col = row = 0                           
while True:
    lcd.write_string(format(col, 'X'))  # 열에 해당하는 수를 16진수로 출력
    sleep(0.1)
    lcd.clear()

    if row == 0: col += 1               # 1행일 경우 점차 증가
    else: col -= 1                      # 2행일 경우 점차 감소

    if col > 15: col = 15; row = 1      # 1행 15열 이상일 경우 2행으로 이동
    elif col < 0: col = 0; row = 0      # 2행 1열 이하일 경우 1행으로 이동    

    lcd.cursor_pos=(row, col)           # 지정된 행, 열로 커서 이동
