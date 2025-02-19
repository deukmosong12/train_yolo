import os
import random

# 이미지와 라벨 폴더 경로
image_folder = "images"
label_folder = R"C:\Users\HOME\Desktop\cvat train folder\yolo_labels"

# 이미지 파일 목록 가져오기 (확장자가 jpg, png, jpeg인 파일)
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

# 삭제할 이미지 파일 50% 선택
num_to_delete = len(image_files) // 2
files_to_delete = random.sample(image_files, num_to_delete)

# 파일 삭제 실행
for image_file in files_to_delete:
    image_path = os.path.join(image_folder, image_file)
    label_path = os.path.join(label_folder, os.path.splitext(image_file)[0] + ".txt")  # 같은 이름의 txt 파일 찾기
    
    # 이미지 삭제
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Deleted image: {image_path}")

    # 라벨 삭제
    if os.path.exists(label_path):
        os.remove(label_path)
        print(f"Deleted label: {label_path}")
