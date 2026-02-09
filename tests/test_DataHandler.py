import unittest
import os
import pandas as pd
from nuriCrawling.DataHandler import DataHandler

class TestDataHandler(unittest.TestCase):
    def setUp(self):
        self.handler = DataHandler()

    def test_add_data_empty(self):
        """엣지 케이스: None 데이터를 추가했을 때 리스트에 포함되지 않는지 확인"""
        self.handler.add_data(None)
        self.assertEqual(len(self.handler.final_data_list), 0)

    def test_save_to_csv_happy_case(self):
        """해피 케이스: 데이터가 있을 때 CSV 파일이 정상 생성되는지 확인"""
        test_data = {"번호": "1", "공고명": "테스트"}
        self.handler.add_data(test_data)
        test_filename = "test_output.csv"

        try:
            self.handler.save_to_csv(test_filename)
            self.assertTrue(os.path.exists(test_filename))
            # 내용 검증
            saved_df = pd.read_csv(test_filename)
            self.assertEqual(str(saved_df["번호"][0]), "1")
        finally:
            if os.path.exists(test_filename):
                os.remove(test_filename)