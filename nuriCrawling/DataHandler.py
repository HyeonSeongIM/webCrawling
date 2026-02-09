import pandas as pd
import datetime
import os

class DataHandler:
    def __init__(self):
        self.final_data_list = [] # 수집된 데이터(dict)들이 담길 리스트

    def add_data(self, data):
        """수집된 단일 데이터를 리스트에 추가"""
        if data:
            self.final_data_list.append(data)

    def save_to_csv(self, filename=None):
        """리스트에 쌓인 데이터를 CSV 파일로 저장"""
        if not self.final_data_list:
            print("[Handler] 저장할 데이터가 없습니다.")
            return

        try:
            # 1. 데이터프레임 변환
            df = pd.DataFrame(self.final_data_list)

            # 2. 파일명 생성 (입력값이 없으면 현재 시간 기준)
            if not filename:
                now = datetime.datetime.now().strftime('%Y%m%d_%H%M')
                filename = f"누리장터_수집결과_{now}.csv"

            # 3. CSV 저장 (utf-8-sig 사용으로 한글 깨짐 방지)
            df.to_csv(filename, index=False, encoding="utf-8-sig")

            print("-" * 30)
            print(f"[Handler] 데이터 저장 성공!")
            print(f"파일명: {filename}")
            print(f"수집 건수: {len(df)}건")
            print("-" * 30)

        except Exception as e:
            print(f"[Handler] 파일 저장 중 오류 발생: {e}")

    def get_summary(self):
        """수집 현황 요약 정보 출력 (디버깅용)"""
        return len(self.final_data_list)