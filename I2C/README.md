# Raspberry Pi와 I2C LCD를 활용해보기
## 데모 영상
[Sweep YouTube 링크](https://www.youtube.com/shorts/SKrtslJeW9s)

[Two Channel Meter YouTube 링크](https://www.youtube.com/shorts/PMWgArgeWZw)

</br>

## 사용한 언어 및 하드웨어
#### 언어
- Python
#### 하드웨어
- Raspberry Pi
- I2C LCD

</br>

## Sweep
아래 동작을 계속 반복하여 0.1초마다 프린트하는 동작 구현
- 첫 줄에는 처음부터 차례대로  0 ~ F 글자를 출력
- 두번 째 줄에는 끝에서부터 앞으로 F ~ 0까지 출력

</br>

## Two Channel Meter
0 ~ 80의 범위를 갖는 두 채널 데이터를 다음과 같은 방법으로 출력
- 채널 1 데이터: 40+20 cos⁡𝑡+30𝑛 
- 채널 2 데이터: 40+20 sin⁡𝑡+30𝑛
- 이 때 시간 𝑡는 0 ~ 2𝜋를 50등분한 값이 반복 적용되며, 𝑛은 0 ~ 1사이의 랜덤 넘버를 냄
