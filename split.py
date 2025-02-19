import os
import shutil
import random

# 입력 폴더 경로 설정
images_folder = "images"
labels_folder = "yolo_labels"

dataset_folder_images='dataset/images'
dataset_folder_label='dataset/labels'
# 출력 폴더 경로 설정
train_images_folder = os.path.join(dataset_folder_images, "train")
val_images_folder = os.path.join(dataset_folder_images, "val")
train_labels_folder = os.path.join(dataset_folder_label, "train")
val_labels_folder = os.path.join(dataset_folder_label, "val")

# 출력 폴더 생성
os.makedirs(train_images_folder, exist_ok=True)
os.makedirs(val_images_folder, exist_ok=True)
os.makedirs(train_labels_folder, exist_ok=True)
os.makedirs(val_labels_folder, exist_ok=True)

# 이미지 파일 목록 가져오기
image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# 파일 셔플
random.shuffle(image_files)

# 데이터 분할 비율
train_ratio = 0.8
train_count = int(len(image_files) * train_ratio)

# 학습 및 검증 데이터로 분리
train_files = image_files[:train_count]
val_files = image_files[train_count:]

# 파일 이동 함수 정의
def copy_files(file_list, src_images_folder, src_labels_folder, dest_images_folder, dest_labels_folder):
    for file in file_list:
        # 이미지 파일 복사
        src_image_path = os.path.join(src_images_folder, file)
        dest_image_path = os.path.join(dest_images_folder, file)
        shutil.copy(src_image_path, dest_image_path)

        # 라벨 파일 복사
        label_file = os.path.splitext(file)[0] + ".txt"
        src_label_path = os.path.join(src_labels_folder, label_file)
        dest_label_path = os.path.join(dest_labels_folder, label_file)

        if os.path.exists(src_label_path):
            shutil.copy(src_label_path, dest_label_path)

# 파일 이동 실행
copy_files(train_files, images_folder, labels_folder, train_images_folder, train_labels_folder)
copy_files(val_files, images_folder, labels_folder, val_images_folder, val_labels_folder)

print(f"Train images: {len(train_files)}\nValidation images: {len(val_files)}")
