# YOLO v8 모델을 통한 라벨링 데이터 학습 가이드
# 목적
YOLO v8 모델이 탐지하지 못하는 객체를 추가적으로 탐지하거나, 기존 탐지 대상을 더 효과적으로 탐지하도록 학습시킨다. 이를 통해 추가적인 객체 탐지 및 기존 탐지 성능 향상을 목표로 한다.
# 학습 전 준비
1.	YOLO v8 모델 설치
o	YOLO v8 모델 설치: pip install ultralytics
2.	라벨링 데이터 준비
o	원시 이미지 파일
o	각 이미지에 해당하는 라벨링 객체와 좌표가 포함된 .txt 파일 or annotaion
3.	데이터셋 폴더 구조 설정
o	YOLO 학습 구조에 맞춰 train 및 val 폴더를 준비하고, data.yaml 파일을 생성한다.

![image](https://github.com/user-attachments/assets/ff795397-9326-4055-a6ec-d94caea2bf49)
# data.yaml 파일 구조
![image](https://github.com/user-attachments/assets/8b55a5e1-f546-4aab-b1c7-46596907239c)
data.yaml파일에 객체수와 객체 이름을 정의해야함

