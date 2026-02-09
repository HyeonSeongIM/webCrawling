import unittest
import os
import shutil
from nuriCrawling.DataValidator import DataValidator

class TestDataValidator(unittest.TestCase):
    def setUp(self):
        """테스트를 위한 임시 디렉토리 및 파일 경로 설정"""
        self.test_dir = "test_results"
        self.test_file = os.path.join(self.test_dir, "test_ids.txt")

        # 테스트 시작 전 깨끗한 상태 유지
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_init_creates_directory(self):
        """초기화 시 저장 폴더가 자동으로 생성되는지 테스트"""
        _ = DataValidator(storage_path=self.test_file)
        self.assertTrue(os.path.exists(self.test_dir))

    def test_load_checkpoints_from_existing_file(self):
        """기존 파일에 저장된 ID들을 정확히 로드하는지 테스트"""
        # 임시 폴더 및 파일 생성
        os.makedirs(self.test_dir)
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("ID_001\nID_002\nID_003\n")

        validator = DataValidator(storage_path=self.test_file)

        self.assertEqual(validator.get_summary(), 3)
        self.assertTrue(validator.is_already_collected("ID_001"))
        self.assertTrue(validator.is_already_collected("ID_002"))
        self.assertTrue(validator.is_already_collected("ID_003"))
        self.assertFalse(validator.is_already_collected("ID_004"))

    def test_record_success_persistence(self):
        """성공 기록 시 메모리와 파일에 즉시 반영되는지 테스트"""
        validator = DataValidator(storage_path=self.test_file)
        test_id = "BID_2024_999"

        # 1. 메모리 기록 확인
        validator.record_success(test_id)
        self.assertTrue(validator.is_already_collected(test_id))

        # 2. 파일 물리적 저장 확인
        with open(self.test_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            self.assertEqual(content, test_id)

    def test_record_success_duplicate_prevention(self):
        """동일한 ID 기록 시 중복 저장되지 않는지 테스트"""
        validator = DataValidator(storage_path=self.test_file)
        test_id = "DUPLICATE_ID"

        validator.record_success(test_id)
        validator.record_success(test_id) # 중복 기록 시도

        self.assertEqual(validator.get_summary(), 1)

        # 파일 내 줄 수 확인
        with open(self.test_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)

    def tearDown(self):
        """테스트 종료 후 생성된 임시 데이터 삭제"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

if __name__ == "__main__":
    unittest.main()