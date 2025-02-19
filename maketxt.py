import os
import xml.etree.ElementTree as ET

# XML 파일 경로와 저장할 폴더 경로 설정
xml_file = "annotations.xml"  # 입력 XML 파일 경로
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
    image_id = image.get("id")
    
    # 관련 박스 정보 가져오기
    boxes = image.findall("box")
    if not boxes:
        continue

    # 해당 이미지에 대한 텍스트 파일 작성
    output_file = os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}.txt")
    with open(output_file, "w") as f:
        for box in boxes:
            label = box.get("label")
            xtl = box.get("xtl")
            ytl = box.get("ytl")
            xbr = box.get("xbr")
            ybr = box.get("ybr")
            
            # 라벨 정보와 좌표 저장
            f.write(f"{label} {xtl} {ytl} {xbr} {ybr}\n")

print(f"이미지 좌표 정보가 '{output_folder}' 폴더에 저장되었습니다.")
