import cv2
import mediapipe as mp
from serial import Serial
import math

ser = Serial('COM4', 115200)
cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

mpHands = mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
roomNum = None
prev = None
Onoff_X = 0
Onoff_Y = 0
Onoff_flag = 0
state = 0


def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2)) + math.sqrt(math.pow(y1 - y2, 2))


compareIndex = ([18, 4], [6, 8], [10, 12], [14, 16], [18, 20])
open = [False, False, False, False, False]
gesture = [[False, False, False, False, False, 'muk'],
           [True, False, False, False, False, 'muk'],
           [False, True, False, False, False, 'point'],
           [True, True, False, False, False, 'point'],
           [True, True, True, True, True, 'bba']]
room = 1

while True:
    success, img = cap.read()
    h, w, c = img.shape
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = my_hands.process(imgRGB)

    img = cv2.rectangle(img, (150, 90), (380, 320), (0, 255, 0), 2)
    img = cv2.rectangle(img, (60, 240), (150, 320), (0, 255, 0), 2)
    img = cv2.rectangle(img, (290, 320), (380, 400), (0, 255, 0), 2)
    img = cv2.rectangle(img, (380, 100), (530, 290), (0, 255, 0), 2)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for i in range(5):
                print(room)
                open[i] = dist(handLms.landmark[0].x, handLms.landmark[0].y, \
                               handLms.landmark[compareIndex[i][0]].x, handLms.landmark[compareIndex[i][0]].y) < \
                          dist(handLms.landmark[0].x, handLms.landmark[0].y, \
                               handLms.landmark[compareIndex[i][1]].x, handLms.landmark[compareIndex[i][1]].y)

            for i in range(0, len(gesture)):
                flag = True
                for j in range(0, 5):
                    if gesture[i][j] != open[j]:
                        flag = False

                if flag:
                    if gesture[i][5] == 'point':
                        if 150 < handLms.landmark[8].x * width < 380 and \
                                90 < handLms.landmark[8].y * height < 320:
                            img = cv2.rectangle(img, (150, 90), (380, 320), (255, 255, 0), 2)
                            room = 1

                        elif 60 < handLms.landmark[8].x * width < 150 and \
                                240 < handLms.landmark[8].y * height < 320:
                            img = cv2.rectangle(img, (60, 240), (150, 320), (255, 255, 0), 2)
                            room = 2

                        elif 290 < handLms.landmark[8].x * width < 380 and \
                                320 < handLms.landmark[8].y * height < 400:

                            img = cv2.rectangle(img, (290, 320), (380, 400), (255, 255, 0), 2)
                            room = 3

                        elif 380 < handLms.landmark[8].x * width < 530 and \
                                100 < handLms.landmark[8].y * height < 290:
                            img = cv2.rectangle(img, (380, 100), (530, 290), (255, 255, 0), 2)
                            room = 4

                    if room == 1 and (gesture[i][5] == 'muk'):
                        img = cv2.rectangle(img, (150, 90), (380, 320), (0, 0, 255), 2)
                        roomNum = b'a\n'
                    if room == 2 and (gesture[i][5] == 'muk'):
                        img = cv2.rectangle(img, (60, 240), (150, 320), (0, 0, 255), 2)
                        roomNum = b'b\n'
                    if room == 3 and (gesture[i][5] == 'muk'):
                        img = cv2.rectangle(img, (290, 320), (380, 400), (0, 0, 255), 2)
                        roomNum = b'c\n'
                    if room == 4 and (gesture[i][5] == 'muk'):
                        img = cv2.rectangle(img, (380, 100), (530, 290), (0, 0, 255), 2)
                        roomNum = b'd\n'
                    if prev != roomNum:
                        params = {'state': roomNum}
                        prev = roomNum
                        ser.write(roomNum)

                    if Onoff_flag == 0 and gesture[i][5] == 'muk':  # 버튼의 on off 여부를 가져다 둘 ui 생성
                        Onoff_flag = 1
                        Onoff_X = round(handLms.landmark[9].x * width)
                        Onoff_Y = round(handLms.landmark[9].y * height)
                        print(Onoff_X, Onoff_Y)

                    if Onoff_flag == 1 and gesture[i][5] == 'muk':
                        img = cv2.rectangle(img, (Onoff_X - 150, Onoff_Y), (Onoff_X + 150, Onoff_Y + 100),
                                            (255, 255, 255), 1)

                        if handLms.landmark[9].x * width >= Onoff_X - 100 and handLms.landmark[
                            9].x * width < Onoff_X + 100:
                            img = cv2.rectangle(img, (round(handLms.landmark[9].x * width) - 50, Onoff_Y),
                                                (round(handLms.landmark[9].x * width) + 50, Onoff_Y + 100),
                                                (255, 255, 0), -1)

                        if handLms.landmark[9].x * width <= Onoff_X - 100:  # 왼쪽으로 당김, off
                            img = cv2.rectangle(img, (Onoff_X - 150, Onoff_Y), (Onoff_X - 50, Onoff_Y + 100),
                                                (0, 0, 255), -1)
                            state = b'-1\n'

                            cv2.putText(img, 'OFF', (Onoff_X - 130, Onoff_Y + 60),
                                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4)

                        if handLms.landmark[9].x * width > Onoff_X + 100:  # 오른쪽으로 당김, on
                            img = cv2.rectangle(img, (Onoff_X + 50, Onoff_Y), (Onoff_X + 150, Onoff_Y + 100),
                                                (0, 255, 0), -1)

                            cv2.putText(img, 'ON', (Onoff_X + 80, Onoff_Y + 60),
                                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4)
                            state = b'1\n'

                    if Onoff_flag == 1 and gesture[i][5] != 'muk':
                        Onoff_flag = 0
                        ser.write(state)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Hand Tracking", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
