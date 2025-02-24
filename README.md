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


# YOLO 모델 학습을 위한 데이터셋 폴더 구조
![image](https://github.com/user-attachments/assets/9f624ad6-81b4-44fb-bfba-e36f5291eda4)
#
•	images: 학습 및 검증용 이미지 파일들이 저장되는 폴더
•	labels: 각 이미지에 해당하는 라벨링 정보(.txt 파일)가 저장되는 폴더
•	data.yaml: 데이터 경로 및 탐지 객체 정보를 정의한 파일

#data.yaml 형식
![image](https://github.com/user-attachments/assets/4cb4fd69-f49f-497b-a437-3a170dfb9fe3)
train: /dataset/train/images  # 학습 이미지 데이터 경로
val: /dataset/val/images      # 검증 이미지 데이터 경로
nc: <탐지 객체의 총 수>      # 탐지 객체 종류의 개수
names: ["객체1", "객체2", ...]  # 탐지 객체 이름
#실행파일 설명
1. maketxt.py
•	기능: 이미지의 바운딩 박스 정보를 기록한 annotations.xml 파일에서 각 이미지에 해당하는 바운딩 박스 좌표만 추출하여 .txt 파일로 저장한다.
•	출력:
o	.txt 파일 형식:
<객체 이름> <x_center> <y_center> <width> <height>
2. change_form.py
•	기능: maketxt.py로 생성된 .txt 파일을 YOLO 모델이 학습 가능한 형식으로 변환한다.
•	작업:
o	객체 이름을 번호로 변환
o	바운딩 박스 
•	추가 작업:
![image](https://github.com/user-attachments/assets/4ad74961-a5db-4ce0-a336-5d648758df85)
o	data.yaml 파일에 정의된 객체 번호 순서대로 change_form.py내의 target_classes내에 객체들을 정의한다.
•	YOLO 포맷:
<객체 번호> <x_center> <y_center> <width> <height>
3. split.py
•	기능:
o	데이터를 train과 val로 분리한다.
o	랜덤으로 이미지를 선택하여 각 이미지와 해당 라벨 파일을 적절한 폴더로 이동시킨다.
•	사용자 설정:
o	train:val 비율을 설정 가능 (예: 80:20)
4. train.py
•	기능: 준비된 데이터셋과 data.yaml 파일을 기반으로 YOLO 모델을 학습시킨다.
•	명령어 예시:
yolo task=detect mode=train model=yolov8n.pt data=/dataset/data.yaml epochs=50 imgsz=640
•	추가 작업: cpu 환경에서 작업하면 시간이 매우 오래 걸린다.따라서 gpu 환경에서 작업 진행 시 main내의 try 안에 device를 gpu로 바꿔 실행.

•	주요 파라미터:
o	model: 학습에 사용할 YOLO 모델 가중치 (예: yolov8n.pt)
o	data: data.yaml 파일 경로
o	epochs: 학습 반복 횟수
o	imgsz: 이미지 크기

#전체 워크 플로우 요약
1.	YOLO v8 모델 설치
2.	원시 이미지와 라벨링 데이터를 준비
3.	maketxt.py 실행: annotations.xml 파일을 .txt 파일로 변환
4.	change_form.py 실행: .txt 파일을 YOLO 형식으로 변환
5.	split.py 실행: 데이터를 train과 val 폴더로 분리
6.	data.yaml 작성: 데이터 경로와 객체 정보를 정의
7.	train.py 실행: YOLO 모델 학습

참고 사항
•	학습 성능을 높이기 위해 데이터 증강(Data Augmentation) 기법을 사용할 수 있음.
•	학습 완료 후, 모델을 테스트하여 새로운 객체 탐지 및 기존 객체 탐지 성능을 검증.
________________________________________
위 내용을 바탕으로 라벨링 데이터 학습 작업을 진행하면 YOLO v8 모델의 탐지 성능을 효과적으로 개선할 수 있습니다.


