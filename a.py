import os
import xml.etree.ElementTree as ET

# XML 파일 경로와 저장할 폴더 경로 설정
xml_file = R"C:\Users\HOME\Desktop\cvat train folder\job_826_dataset_2025_01_31_05_47_39_cvat for images 1.1\annotations.xml"  # 입력 XML 파일 경로
output_folder = "labels"  # 출력 폴더 이름

# 출력 폴더 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# XML 파일 파싱
try:
    tree = ET.parse(xml_file)
    root = tree.getroot()
except Exception as e:
    print(f"XML 파일을 파싱하는 동안 오류 발생: {e}")
    exit()

# 이미지 태그를 순회하며 처리
for image in root.findall("image"):
    image_name = image.get("name")
    
    # 해당 이미지에 대한 텍스트 파일 경로 설정
    output_file = os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}.txt")
    
    # 관련 박스 정보 가져오기
    boxes = image.findall("box")
    
    # txt 파일 생성 (라벨이 없더라도 빈 파일을 생성)
    with open(output_file, "w") as f:
        for box in boxes:
            label = box.get("label")
            xtl = box.get("xtl")
            ytl = box.get("ytl")
            xbr = box.get("xbr")
            ybr = box.get("ybr")
            
            # 라벨 정보와 좌표 저장
            f.write(f"{label} {xtl} {ytl} {xbr} {ybr}\n")

print(f"모든 이미지에 대한 txt 파일이 '{output_folder}' 폴더에 저장되었습니다.")
