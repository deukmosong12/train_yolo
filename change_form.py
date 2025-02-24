import os
from PIL import Image

# 추가적으로 탐지하고자 하는 객체 이름 리스트
target_classes = [
    'wheelchair',
    'truck',
    'tree_trunk',
    'traffic_sign',
    'traffic_light',
    'table',
    'stroller',
    'stop',
    'scooter',
    'potted_plant',
    'pole',
    'person',
    'parking_meter',
    'movable_signage',
    'motorcycle',
    'kiosk',
    'fire_hydrant',
    'dog',
    'chair',
    'cat',
    'carrier',
    'car',
    'bus',
    'bollard',
    'bicycle',
    'bench',
    'barricade',
    'manhole'
]

# 클래스 이름과 ID를 매핑하는 사전 정의
class_mapping = {name: idx for idx, name in enumerate(target_classes)}

# 경로 설정
labels_dir = 'labels'      # 레이블 파일들이 있는 폴더
images_dir = 'images'      # 이미지 파일들이 있는 폴더
output_dir = 'yolo_labels' # 변환된 YOLO 형식 레이블을 저장할 폴더

# 출력 폴더가 없으면 생성
os.makedirs(output_dir, exist_ok=True)

# 레이블 폴더 내의 모든 .txt 파일을 처리
for label_file in os.listdir(labels_dir):
    if not label_file.endswith('.txt'):
        continue  # .txt 파일만 처리

    label_path = os.path.join(labels_dir, label_file)

    # 대응되는 이미지 파일 찾기 (확장자는 .jpg, .png 등 다양할 수 있음)
    base_name = os.path.splitext(label_file)[0]
    possible_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_path = None
    for ext in possible_extensions:
        temp_path = os.path.join(images_dir, base_name + ext)
        if os.path.exists(temp_path):
            image_path = temp_path
            break
    if image_path is None:
        print(f"이미지 파일을 찾을 수 없습니다: {base_name}")
        continue

    # 이미지 크기 읽기
    with Image.open(image_path) as img:
        img_width, img_height = img.size

    # 변환된 라인을 저장할 리스트
    yolo_lines = []

    # 레이블 파일 읽기
    with open(label_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            print(f"잘못된 라인 형식: {line} in {label_file}")
            continue
        class_name, x1, y1, x2, y2 = parts
        if class_name not in target_classes:
            continue  # 대상 클래스가 아니면 스킵
        if class_name not in class_mapping:
            print(f"알 수 없는 클래스: {class_name} in {label_file}")
            continue
        class_id = class_mapping[class_name]
        x1 = float(x1)
        y1 = float(y1)
        x2 = float(x2)
        y2 = float(y2)

        # YOLO 형식으로 변환
        x_center = ((x1 + x2) / 2) / img_width
        y_center = ((y1 + y2) / 2) / img_height
        width = (x2 - x1) / img_width
        height = (y2 - y1) / img_height

        # 소수점 자리수 조정 (필요시)
        yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
        yolo_lines.append(yolo_line)

    # 변환된 레이블을 새로운 파일에 저장
    if yolo_lines:  # 변환된 내용이 있을 경우만 저장
        output_path = os.path.join(output_dir, label_file)
        with open(output_path, 'w') as f:
            f.writelines(yolo_lines)

        print(f"변환 완료: {label_file} -> {output_path}")
    else:
        print(f"대상 클래스가 없어 변환되지 않음: {label_file}")

print("모든 레이블 파일 변환이 완료되었습니다.")
