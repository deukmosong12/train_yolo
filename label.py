import os
from PIL import Image, ImageDraw
from ultralytics import YOLO

# 디렉토리 설정
image_folder = 'images'
label_image_folder = 'label_image'
label_inform_folder = 'label_inform'
os.makedirs(label_image_folder, exist_ok=True)
os.makedirs(label_inform_folder, exist_ok=True)

# YOLOv8 커스텀 모델 로드
model = YOLO(r'C:\Users\HOME\Desktop\train yolo\weights\best (2).pt')  # 'best.pt'의 실제 경로로 변경


# 임계값 설정
confidence_threshold = 0.0  # 원하는 임계값으로 설정하세요

# 이미지 처리
for image_name in os.listdir(image_folder):
    if image_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
        image_path = os.path.join(image_folder, image_name)
        image = Image.open(image_path).convert('RGB')
        
        # 모델 예측
        results = model(image)

        # 바운딩 박스 정보 추출
        # YOLOv8의 경우, results는 리스트로 반환되며, 첫 번째 요소의 boxes 속성 사용
        boxes = results[0].boxes  # 각 박스는 Box 객체
        
        # 바운딩 박스 그리기
        draw = ImageDraw.Draw(image)
        label_data = []
        for box in boxes:
            # 클래스 ID와 신뢰도 확인
            cls_id = int(box.cls[0].item())  # 클래스 ID
            confidence = box.conf[0].item()  # 신뢰도

            if  confidence >= confidence_threshold:
                # 바운딩 박스 좌표 (왼쪽 상단 x, 왼쪽 상단 y, 오른쪽 하단 x, 오른쪽 하단 y)
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                draw.rectangle([x1, y1, x2, y2], outline='red', width=2)
                
                # YOLO 형식의 바운딩 박스 정보 계산
                img_width, img_height = image.size
                box_width = x2 - x1
                box_height = y2 - y1
                center_x = x1 + box_width / 2
                center_y = y1 + box_height / 2
                yolo_x = center_x / img_width
                yolo_y = center_y / img_height
                yolo_width = box_width / img_width
                yolo_height = box_height / img_height
                
                # 라벨 정보 저장 (클래스 ID는 0으로 설정)
                label_data.append(f"{cls_id} {yolo_x:.6f} {yolo_y:.6f} {yolo_width:.6f} {yolo_height:.6f}")

        # 라벨 이미지 저장
        label_image_path = os.path.join(label_image_folder, image_name)
        image.save(label_image_path)

        # 라벨 정보 저장
        label_inform_path = os.path.join(label_inform_folder, os.path.splitext(image_name)[0] + '.txt')
        with open(label_inform_path, 'w') as f:
            f.write('\n'.join(label_data))
