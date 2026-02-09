import unittest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
from nuriCrawling.DataHandler import DataHandler

class TestDataHandler(unittest.TestCase):
    def setUp(self):
        """테스트 시작 전 Handler 인스턴스 초기화"""
        # 실제 디렉토리를 생성하지 않도록 patch 처리할 수 있으나,
        # 여기서는 테스트용 임시 디렉토리 이름을 사용합니다.
        self.test_dir = "test_results"
        self.handler = DataHandler(output_dir=self.test_dir)

    def test_add_data_valid(self):
        """유효한 딕셔너리 데이터 추가 테스트"""
        sample_data = {"목록_입찰공고번호": "2024-01", "입찰공고명": "테스트"}
        self.handler.add_data(sample_data)

        self.assertEqual(len(self.handler.final_data_list), 1)
        self.assertEqual(self.handler.final_data_list[0]["입찰공고명"], "테스트")

    def test_add_data_invalid(self):
        """잘못된 데이터 타입(리스트 등) 추가 시 무시되는지 테스트"""
        self.handler.add_data(["리스트데이터"]) # 딕셔너리가 아님
        self.handler.add_data(None)

        self.assertEqual(len(self.handler.final_data_list), 0)

    def test_prepare_dataframe_ordering(self):
        """데이터프레임 변환 시 컬럼 순서 정렬 테스트"""
        sample_data = {
            "기타컬럼": "ETC",
            "공고일시": "2024-01-01",
            "입찰공고명": "공고명",
            "목록_입찰공고번호": "ID-01"
        }
        self.handler.add_data(sample_data)
        df = self.handler._prepare_dataframe()

        # 정의된 main_columns 순서대로 정렬되었는지 확인
        expected_order = ['목록_입찰공고번호', '입찰공고명', '공고일시', '기타컬럼']
        self.assertEqual(list(df.columns), expected_order)

    @patch('pandas.DataFrame.to_csv')
    def test_save_csv(self, mock_to_csv):
        """CSV 저장 함수 호출 여부 테스트 (실제 파일 생성 없이)"""
        self.handler.add_data({"목록_입찰공고번호": "1", "입찰공고명": "A", "공고일시": "T"})

        # save 메서드 실행
        self.handler.save(file_format="csv", filename="test_output")

        # mock_to_csv가 호출되었는지 확인
        mock_to_csv.assert_called_once()
        # 호출된 파일 경로 인자 확인 (test_results/test_output.csv 형식)
        args, _ = mock_to_csv.call_args
        self.assertTrue("test_output.csv" in args[0])

    def test_clear_data(self):
        """메모리 비우기 기능 테스트"""
        self.handler.add_data({"key": "value"})
        self.handler.clear_data()
        self.assertEqual(len(self.handler.final_data_list), 0)

    def tearDown(self):
        """테스트 후 테스트용 디렉토리 삭제 (실제로 생성된 경우)"""
        if os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir)

if __name__ == "__main__":
    unittest.main()