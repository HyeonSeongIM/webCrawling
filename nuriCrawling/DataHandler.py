import pandas as pd
import datetime
import os

class DataHandler:
    def __init__(self, output_dir="results"):
        self.final_data_list = []
        self.output_dir = output_dir

        # 저장 폴더 자동 생성
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    """데이터 추가 시 유효성 검사 및 정제 로직 포함 가능"""

    def add_data(self, data):
        if data and isinstance(data, dict):
            # [확장성] 필요 시 여기서 특정 키를 제외하거나
            # 데이터 포맷을 강제로 맞추는 전처리를 수행할 수 있습니다.
            self.final_data_list.append(data)

    """데이터프레임 변환 및 컬럼 순서 정렬"""

    def _prepare_dataframe(self):
        if not self.final_data_list:
            return None

        df = pd.DataFrame(self.final_data_list)

        # 주요 컬럼을 맨 앞으로 배치
        main_columns = ['목록_입찰공고번호', '입찰공고명', '공고일시']
        existing_main = [col for col in main_columns if col in df.columns]
        other_columns = [col for col in df.columns if col not in existing_main]

        return df[existing_main + other_columns]

    """데이터 정해진 포맷으로 추출"""

    def save(self, file_format="csv", filename=None):
        df = self._prepare_dataframe()
        if df is None:
            print("[Handler] 저장할 데이터가 없습니다.")
            return

        # 파일명 생성
        if not filename:
            now = datetime.datetime.now().strftime('%Y%m%d_%H%M')
            filename = f"누리장터_수집결과_{now}"

        full_path = os.path.join(self.output_dir, f"{filename}.{file_format}")

        try:
            if file_format == "csv":
                df.to_csv(full_path, index=False, encoding="utf-8-sig")
            elif file_format == "excel":
                # openpyxl 라이브러리 필요
                df.to_excel(full_path, index=False)
            elif file_format == "json":
                df.to_json(full_path, orient="records", force_ascii=False, indent=4)

            self.print_success(full_path, len(df))

        except Exception as e:
            print(f"[Handler] {file_format} 저장 중 오류 발생: {e}")

    """성공 시 반환하는 응답"""

    def print_success(self, path, count):
        print("-" * 30)
        print(f"[Handler] 데이터 저장 성공!")
        print(f"경로: {path}")
        print(f"수집 건수: {count}건")
        print("-" * 30)

    """메모리 비우기 (대량 수집 시 필요)"""

    def clear_data(self):
        self.final_data_list = []