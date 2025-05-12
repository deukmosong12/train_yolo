import os
import yaml
from ultralytics import YOLO

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'


def main():
    # 데이터셋 경로 설정
    data_path = r'dataset\data.yaml'
    print(f"데이터셋 설정 파일 경로: {data_path}")

    # data.yaml 파일 존재 여부 확인
    if not os.path.exists(data_path):
        print(f"오류: {data_path} 파일이 존재하지 않습니다.")
        return
    else:
        print(f"{data_path} 파일이 존재합니다.")
    
    # data.yaml 파일 내용 읽기 (utf-8 인코딩 지정)
    try:
        with open(data_path, 'r', encoding='utf-8') as file:
            data_content = file.read()
            print("data.yaml 파일 내용:")
            print(data_content)
    except UnicodeDecodeError as e:
        print(f"파일 인코딩 오류: {e}")
        return
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return

    # data.yaml 파일 파싱
    try:
        with open(data_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            train_path = os.path.join(os.path.dirname(data_path), data['train'])
            val_path = os.path.join(os.path.dirname(data_path), data['val'])
            print(f"Train 경로: {train_path}")
            print(f"Val 경로: {val_path}")
    
            # Train 경로 확인
            if not os.path.exists(train_path):
                print(f"오류: {train_path} 폴더가 존재하지 않습니다.")
                return
            else:
                print(f"{train_path} 폴더가 존재합니다.")
    
            # Val 경로 확인
            if not os.path.exists(val_path):
                print(f"오류: {val_path} 폴더가 존재하지 않습니다.")
                return
            else:
                print(f"{val_path} 폴더가 존재합니다.")
    except Exception as e:
        print(f"data.yaml 파일 파싱 중 오류가 발생했습니다: {e}")
        return

    # 모델 로드 시작
    print("모델을 로드 중입니다...")
    try:
        model = YOLO('yolov8s.pt')  # 사전 학습된 yolov8s.pt 사용
        print("모델 로드 완료.")
    except Exception as e:
        print(f"모델 로드 중 오류가 발생했습니다: {e}")
        return

    # 학습 시작 알림
    print("모델 학습을 시작합니다...")

    # 학습 실행 및 오류 처리
    try:
        results = model.train(
            data=data_path,             # 데이터 설정 파일 경로
            epochs=500,                 # 학습 에포크 수 (증가)
            imgsz=640,                  # 이미지 크기
            batch=16,                   # 배치 크기
            project='yolov8_project',   # 결과 저장 프로젝트 이름
            name='experiment1',         # 실험 이름
            optimizer='SGD',            # 옵티마이저 설정
            lr0=0.01,                   # 초기 학습률
            device='cpu',               # 사용할 디바이스
            verbose=True,               # 상세 로그 출력
            patience=50,                # 조기 종료 조건 (10 epoch 성능 개선 없을 시)
            early_stop=True            # early stopping 활성화
        )

        print("모델 학습이 완료되었습니다.")
    except Exception as e:
        print(f"학습 중 오류가 발생했습니다: {e}")
        return

    # 학습된 가중치 파일 존재 여부 확인
    weights_path = os.path.join('yolov8_project', 'experiment1', 'weights', 'best.pt')
    if os.path.exists(weights_path):
        print(f"학습된 모델 가중치가 성공적으로 저장되었습니다: {weights_path}")
    else:
        print(f"오류: {weights_path} 파일이 존재하지 않습니다.")

    # 추가: 학습 결과 요약 출력
    print("학습 결과 요약:")
    print(results)

if __name__ == "__main__":
    main()
